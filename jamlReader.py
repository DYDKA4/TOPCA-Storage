import yaml
import json


# convert jaml to json files

def list_dict(dicts):
    for key, value in dicts.items():
        try:
            print("key:\t" + key)
            list_dict(value)
        except AttributeError:
            print("value:\t" + str(value))


with open('jamlExamples/Server bound to a new network.yaml', encoding='utf-8') as f:
    templates = yaml.safe_load(f)

with open('jamlExamples/Server bound to a new network.json', 'w') as f:
    f.write(str(json.dumps(templates)))

print(list_dict(templates))
