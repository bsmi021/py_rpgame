import json

from java.nio.charset import StandardCharsets
from org.apache.commons.io import IOUtils
from org.apache.nifi.processor.io import StreamCallback


class ParseTweet(StreamCallback):
    def __init__(self):
        pass

    def process(selfs, inputStream, outputStream):
        json_string = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        tweet_d = json.loads(json_string)

        if 'created_at' in tweet_d:
            created_at = tweet_d['created_at']
        else:
            created_at = ''

        id = tweet_d['id']
        text = tweet_d['text']
        truncated = 0
        if tweet_d['truncated']:
            truncated = 1
        user_id = tweet_d['user']['id']
        user_name = tweet_d['user']['name']
        user_screen_name = tweet_d['user']['screen_name']
        if truncated == 1 and 'extended_tweet' in tweet_d:
            full_text = tweet_d['extended_tweet']['full_text']
        else:
            full_text = ''
        timestamp_ms = tweet_d['timestamp_ms']

        result_json = json.dumps(dict(id=id, timestamp_ms=int(timestamp_ms), created_at=created_at,
                                      truncated=truncated, text=text, full_text=full_text,
                                      user_id=user_id, screen_name=user_screen_name, name=user_name))

        outputStream.write(bytearray(result_json.encode('utf-8')))


flowFiles = session.get(1000)

for flowFile in flowFiles:
    if flowFile is not None:  # process only if there actually is a flowFile
        orig_flow_file = flowFile

        if flowFile.getSize() == 0:
            session.transfer(orig_flow_file, REL_FAILURE)

        flowFile = session.write(flowFile, ParseTweet())

        if flowFile.getSize() == 0:
            session.transfer(orig_flow_file, REL_FAILURE)

        flowFile = session.putAttribute(flowFile, "filename",
                                        flowFile.getAttribute('filename').split('.')[0] + '_translated.json')

        session.transfer(flowFile, REL_SUCCESS)
session.commit()