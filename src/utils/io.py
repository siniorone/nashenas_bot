import json

def read_json(file):
# Opening JSON file
    with open(file, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    return json_object

def write_json(file, data, indent=4):
    # Dumping into the JSON file
    with open(file, "w") as outfile:
        json.dump(data, outfile, indent=indent)