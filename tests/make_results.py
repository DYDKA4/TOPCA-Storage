import os
from app import json_parser
import json

"""
use to renew output results for unit tests 
"""


dir_name = "/home/tulin/PycharmProjects/pythonProject/jamlExamples/"
destination = "/home/tulin/PycharmProjects/pythonProject/tests/results/"
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".json"):
        with open(dir_name+item) as f:
            data = json.load(f)
            result = json_parser.parser(data)
            with open(destination+item[:-4]+'txt', 'w') as j:
                j.write(str(result))

