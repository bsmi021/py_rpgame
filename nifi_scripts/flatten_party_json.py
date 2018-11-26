import json

from java.nio.charset import StandardCharsets
from org.apache.commons.io import IOUtils
from org.apache.nifi.processor.io import StreamCallback


class ModJSON(StreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream, outputStream):
        json_string = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        obj = json.loads(json_string)

        if obj["id"] is not None:
            obj["party_id"] = obj["id"]
            del (obj["id"])

        if obj["members"] is not None:  # iterate members and add them to the dictionary
            for i in range(len(obj['members'])):
                o = obj['members'][i]
                i += 1
                obj['member_inst_id_{}'.format(i)] = int(o['instance_id'])
                obj['member_id_{}'.format(i)] = int(o['id'])

            del (obj['members'])  # remove the members array

        if obj["name"]:  # ensure that the name is a string
            obj["name"] = str(obj["name"])

        outputStream.write(bytearray(json.dumps(obj).encode('utf-8')))


flowFile = session.get()

if flowFile is not None:  # process only if there actually is a flowFile
    flowFile = session.write(flowFile, ModJSON())
    flowFile = session.putAttribute(flowFile, "filename",
                                    flowFile.getAttribute('filename').split('.')[0] + '_translated.json')

    session.transfer(flowFile, REL_SUCCESS)
    session.commit()
