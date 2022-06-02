import unittest
from app.parser.tosca_v_1_3 import ServiceTemplateDefinition
import yaml


class TestJsonParser(unittest.TestCase):

    def test_SBS(self):
        with open('jamlExamples/SBS.yaml') as f:
            data = yaml.safe_load(f)
            with open('tests/results/SBS.txt') as out:
                result = out.read()
                answer = str(vars(yaml_parser.parser(data, 'test')))
                self.assertEqual(result, answer)


if __name__ == "__main__":
    unittest.main()
