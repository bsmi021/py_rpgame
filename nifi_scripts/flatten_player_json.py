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

        if obj["equipped_items"] is not None:
            for o in obj["equipped_items"]:
                obj[str(o['slot_name']).lower() + '_slot'] = int(o['id'])

        del (obj["equipped_items"])
        outputStream.write(bytearray(json.dumps(obj).encode('utf-8')))


flowFile = session.get()

if flowFile is not None:
    flowFile = session.write(flowFile, ModJSON())
    flowFile = session.putAttribute(flowFile, "filename",
                                    flowFile.getAttribute('filename').split('.')[0] + '_translated.json')

    session.transfer(flowFile, REL_SUCCESS)
    session.commit()
