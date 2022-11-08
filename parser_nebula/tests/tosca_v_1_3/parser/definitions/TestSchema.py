import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.definitions.SchemaDefinition import schema_definition_parser


class TestSchema(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.schema_definition_parser = schema_definition_parser

    # Each test method starts with the keyword test_
    def test_schema(self):
        file = open('test_input/schema/schema.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        schema = schema_definition_parser(data)
        self.assertEqual(schema.type, 'schema_type_test')
        self.assertEqual(schema.description, 'schema_description_test')
        for index, constraint in enumerate(schema.constraints):
            self.assertEqual(constraint.operator, 'equal_' + str(index))
            self.assertEqual(constraint.value, 'value_' + str(index))
        self.assertEqual(schema.key_schema, None)
        self.assertEqual(schema.entry_schema, None)

    def test_schema_complex(self):
        file = open('test_input/schema/schema_complex.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        schema = schema_definition_parser(data)
        self.assertEqual(schema.type, 'schema_type_test')
        self.assertEqual(schema.description, 'schema_description_test')
        for index, constraint in enumerate(schema.constraints):
            self.assertEqual(constraint.operator, 'equal_' + str(index))
            self.assertEqual(constraint.value, 'value_' + str(index))

        self.assertEqual(schema.key_schema.type, 'key_schema_type_test')
        self.assertEqual(schema.key_schema.description, 'key_schema_description_test')
        for index, constraint in enumerate(schema.key_schema.constraints):
            self.assertEqual(constraint.operator, 'key_equal_' + str(index))
            self.assertEqual(constraint.value, 'key_value_' + str(index))
        self.assertEqual(schema.key_schema.key_schema, None)
        self.assertEqual(schema.key_schema.entry_schema, None)

        self.assertEqual(schema.entry_schema.type, 'entry_schema_type_test')
        self.assertEqual(schema.entry_schema.description, 'entry_schema_description_test')
        for index, constraint in enumerate(schema.entry_schema.constraints):
            self.assertEqual(constraint.operator, 'entry_equal_' + str(index))
            self.assertEqual(constraint.value, 'entry_value_' + str(index))
        self.assertEqual(schema.entry_schema.key_schema, None)
        self.assertEqual(schema.entry_schema.entry_schema, None)


