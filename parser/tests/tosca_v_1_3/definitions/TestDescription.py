import unittest

import yaml

from parser.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser


class TestDescription(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.description_parser = description_parser

    # Each test method starts with the keyword test_
    def test_parser(self):
        file = open('test_input/description/TestDescription.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        self.assertEqual(self.description_parser(data), 'Test description')
