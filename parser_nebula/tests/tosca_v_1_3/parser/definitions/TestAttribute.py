import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.definitions.AttributeDefinition import attribute_definition_parser


class TestAttribute(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.attribute_definition_parser = attribute_definition_parser

    # Each test method starts with the keyword test_
    def test_short_notation(self):
        file = open('test_input/attribute/template.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            artifact = attribute_definition_parser(name, value)
            self.assertEqual(artifact.vertex_type_system, 'AttributeDefinition')
            self.assertEqual(artifact.name, 'test_attribute_name')
            self.assertEqual(artifact.type, 'test_attribute_type')
            self.assertEqual(artifact.description, 'test_attribute_description')
            self.assertEqual(artifact.default, 'test_default_value')
            self.assertEqual(artifact.status, 'test_status_value')

            self.assertEqual(artifact.key_schema.type, 'key_schema_type_test')
            self.assertEqual(artifact.key_schema.description, 'key_schema_description_test')
            for index, constraint in enumerate(artifact.key_schema.constraints):
                self.assertEqual(constraint.operator, 'key_equal_' + str(index))
                self.assertEqual(constraint.value, 'key_value_' + str(index))
            self.assertEqual(artifact.key_schema.key_schema, None)
            self.assertEqual(artifact.key_schema.entry_schema, None)

            self.assertEqual(artifact.entry_schema.type, 'entry_schema_type_test')
            self.assertEqual(artifact.entry_schema.description, 'entry_schema_description_test')
            for index, constraint in enumerate(artifact.entry_schema.constraints):
                self.assertEqual(constraint.operator, 'entry_equal_' + str(index))
                self.assertEqual(constraint.value, 'entry_value_' + str(index))
            self.assertEqual(artifact.entry_schema.key_schema, None)
            self.assertEqual(artifact.entry_schema.entry_schema, None)
