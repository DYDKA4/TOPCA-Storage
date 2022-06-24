import unittest

import yaml

from parser.parser.tosca_v_1_3.assignments.AttributeAssignment import attribute_assignments_parser


class TestAttribute(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.description_parser = attribute_assignments_parser

    # Each test method starts with the keyword test_
    def test_set_value_short(self):
        file = open('test_input/attribute/TestAttributeShort.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            attribute = self.description_parser(name, value)
            self.assertEqual(attribute.name, 'test_attribute_name')
            self.assertEqual(attribute.value, 'attribute_value_test')

    def test_set_set_value(self):
        file = open('test_input/attribute/TestAttribute.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            attribute = self.description_parser(name, value)
            self.assertEqual(attribute.name, 'test_attribute_name')
            self.assertEqual(attribute.value, 'attribute_value_test')
            self.assertEqual(attribute.vertex_type_system, 'AttributeAssignment')

    def test_set_description(self):
        file = open('test_input/attribute/TestAttributeDescription.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            attribute = self.description_parser(name, value)
            self.assertEqual(attribute.name, 'test_attribute_name')
            self.assertEqual(attribute.description, 'test_description')
            self.assertEqual(attribute.vertex_type_system, 'AttributeAssignment')

    def test_set_value_short_complex(self):
        file = open('test_input/attribute/TestAttributeShortComplex.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            attribute = self.description_parser(name, value)
            self.assertEqual(attribute.name, 'test_attribute_name')
            self.assertEqual(attribute.value, "{'get_input': 'test_value'}")
            self.assertEqual(attribute.vertex_type_system, 'AttributeAssignment')


if __name__ == '__main__':
    unittest.main()
