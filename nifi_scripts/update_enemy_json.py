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
            obj["enemy_id"] = obj["id"]
            del (obj["id"])

        outputStream.write(bytearray(json.dumps(obj).encode('utf-8')))


flowFile = session.get()

if flowFile is not None:
    flowFile = session.write(flowFile, ModJSON())
    flowFile = session.putAttribute(flowFile, "filename",
                                    flowFile.getAttribute('filename').split('.')[0] + '_translated.json')

    session.transfer(flowFile, REL_SUCCESS)
    session.commit()
