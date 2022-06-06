import unittest

import yaml

from app.parser.tosca_v_1_3.definitions.PropertyDefinition import property_definition_parser


class TestProperty(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.property_definition_parser = property_definition_parser

    # Each test method starts with the keyword test_
    def test_property(self):
        file = open('test_input/property/property.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        property_def = property_definition_parser('test_property_name', data.get('test_property_name'))
        self.assertEqual(property_def.name, 'test_property_name')
        self.assertEqual(property_def.type, 'test_property_name')
        self.assertEqual(property_def.description, 'test_property_description')
        self.assertEqual(property_def.required, True)
        self.assertEqual(property_def.default, 'test_default_value')
        self.assertEqual(property_def.status, 'test_status')
        for index, constraint in enumerate(property_def.constraints):
            self.assertEqual(constraint.operator, 'equal_' + str(index))
            self.assertEqual(constraint.value, 'value_' + str(index))

        self.assertEqual(property_def.key_schema.type, 'key_schema_type_test')
        self.assertEqual(property_def.key_schema.description, 'key_schema_description_test')
        for index, constraint in enumerate(property_def.key_schema.constraints):
            self.assertEqual(constraint.operator, 'key_equal_' + str(index))
            self.assertEqual(constraint.value, 'key_value_' + str(index))
        self.assertEqual(property_def.key_schema.key_schema, None)
        self.assertEqual(property_def.key_schema.entry_schema, None)

        self.assertEqual(property_def.entry_schema.type, 'entry_schema_type_test')
        self.assertEqual(property_def.entry_schema.description, 'entry_schema_description_test')
        for index, constraint in enumerate(property_def.entry_schema.constraints):
            self.assertEqual(constraint.operator, 'entry_equal_' + str(index))
            self.assertEqual(constraint.value, 'entry_value_' + str(index))
        self.assertEqual(property_def.entry_schema.key_schema, None)
        self.assertEqual(property_def.entry_schema.entry_schema, None)

        for index, metadata in enumerate(property_def.metadata):
            self.assertEqual(metadata.name, 'metadata_key_' + str(index))
            self.assertEqual(metadata.value, 'metadata_value_' + str(index))

