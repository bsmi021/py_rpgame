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
            obj["player_id"] = obj["id"]
            del (obj["id"])

        if obj["instance_id"] is not None:
            obj["player_instance_id"] = obj["instance_id"]
            del (obj["instance_id"])

        if obj["equipped_items"] is not None:
            for o in obj["equipped_items"]:
                obj[str(o['slot_name']).lower() + '_slot'] = int(o['id'])

        del (obj["equipped_items"])
        outputStream.write(bytearray(json.dumps(obj).encode('utf-8')))


flowFiles = session.get(1000)

for flowFile in flowFiles:
    if flowFile is not None:
        flowFile = session.write(flowFile, ModJSON())
        flowFile = session.putAttribute(flowFile, "filename",
                                        flowFile.getAttribute('filename').split('.')[0] + '_translated.json')

        session.transfer(flowFile, REL_SUCCESS)
session.commit()
