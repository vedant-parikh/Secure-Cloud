import json

def getFileMap() :
    with open('Serializer/JSONSerializerStorage.json', 'r') as f:
        try:
            return json.load(f)
        except:
            return {}

def saveFileMap(file_map) :
    with open('Serializer/JSONSerializerStorage.json', 'w') as f:
        json.dump(file_map, f)
