import unittest

import yaml

from parser.parser.tosca_v_1_3.types.DataType import data_type_parser


class TestData(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.data_type_parser = data_type_parser

    # Each test method starts with the keyword test_
    def test_data(self):
        file = open('test_input/data_type/data.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            data_type = data_type_parser(name, value)
            self.assertEqual(data_type.vertex_type_system, 'ArtifactType')
            self.assertEqual(data_type.name, 'test_data_type_name')
            self.assertEqual(data_type.derived_from, 'test_existing_type_name')
            self.assertEqual(data_type.version, 'test_version_number')
            for index, metadata in enumerate(data_type.metadata):
                self.assertEqual(metadata.name, 'metadata_key_' + str(index))
                self.assertEqual(metadata.value, 'metadata_value_' + str(index))
            self.assertEqual(data_type.description, 'test_datatype_description')
            for index, constraint in enumerate(data_type.constraints):
                self.assertEqual(constraint.operator, 'equal_' + str(index))
                self.assertEqual(constraint.value, 'value_' + str(index))
            for index, properties in enumerate(data_type.properties):
                self.assertEqual(properties.type, 'test_property_name_' + str(index))
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.description, 'test_property_description_' + str(index))

            self.assertEqual(data_type.key_schema.type, 'key_schema_type_test')
            self.assertEqual(data_type.key_schema.description, 'key_schema_description_test')
            for index, constraint in enumerate(data_type.key_schema.constraints):
                self.assertEqual(constraint.operator, 'key_equal_' + str(index))
                self.assertEqual(constraint.value, 'key_value_' + str(index))
            self.assertEqual(data_type.key_schema.key_schema, None)
            self.assertEqual(data_type.key_schema.entry_schema, None)

            self.assertEqual(data_type.entry_schema.type, 'entry_schema_type_test')
            self.assertEqual(data_type.entry_schema.description, 'entry_schema_description_test')
            for index, constraint in enumerate(data_type.entry_schema.constraints):
                self.assertEqual(constraint.operator, 'entry_equal_' + str(index))
                self.assertEqual(constraint.value, 'entry_value_' + str(index))
            self.assertEqual(data_type.entry_schema.key_schema, None)
            self.assertEqual(data_type.entry_schema.entry_schema, None)
