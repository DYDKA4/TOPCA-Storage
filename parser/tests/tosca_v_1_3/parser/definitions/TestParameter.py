import unittest

import yaml

from parser.parser.tosca_v_1_3.definitions.ParameterDefinition import parameter_definition_parser


class TestParameter(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.parameter_definition_parser = parameter_definition_parser

    # Each test method starts with the keyword test_
    def test_extended_notation(self):
        file = open('test_input/parameter/extended_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for key, value in data.items():
            parameter = parameter_definition_parser(key, value)
            self.assertEqual(parameter.type, 'test_type')
            self.assertEqual(parameter.vertex_type_system, 'ParameterDefinition')
            self.assertEqual(parameter.description, 'test_parameter_description')
            self.assertEqual(parameter.value, 'test_parameter_value')
            self.assertEqual(parameter.required, False)
            self.assertEqual(parameter.default, 'test_parameter_default_value')
            self.assertEqual(parameter.status, 'test_status_value')
            self.assertNotEqual(parameter.constraints, [])
            for index, constraint in enumerate(parameter.constraints):
                self.assertEqual(constraint.operator, 'equal_' + str(index))
                self.assertEqual(constraint.value, 'value_' + str(index))

            self.assertNotEqual(parameter.key_schema, None)
            self.assertEqual(parameter.key_schema.type, 'key_schema_type_test')
            self.assertEqual(parameter.key_schema.description, 'key_schema_description_test')
            for index, constraint in enumerate(parameter.key_schema.constraints):
                self.assertEqual(constraint.operator, 'key_equal_' + str(index))
                self.assertEqual(constraint.value, 'key_value_' + str(index))
            self.assertEqual(parameter.key_schema.key_schema, None)
            self.assertEqual(parameter.key_schema.entry_schema, None)

            self.assertNotEqual(parameter.entry_schema, None)
            self.assertEqual(parameter.entry_schema.type, 'entry_schema_type_test')
            self.assertEqual(parameter.entry_schema.description, 'entry_schema_description_test')
            for index, constraint in enumerate(parameter.entry_schema.constraints):
                self.assertEqual(constraint.operator, 'entry_equal_' + str(index))
                self.assertEqual(constraint.value, 'entry_value_' + str(index))
            self.assertEqual(parameter.entry_schema.key_schema, None)
            self.assertEqual(parameter.entry_schema.entry_schema, None)

    def test_short_notation(self):
        file = open('test_input/parameter/short_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for key, value in data.items():
            parameter = parameter_definition_parser(key, value)
            self.assertEqual(parameter.type, None)
            self.assertEqual(parameter.vertex_type_system, 'ParameterDefinition')
            self.assertEqual(parameter.description, None)
            self.assertEqual(parameter.value, 'test_parameter_value')
            self.assertEqual(parameter.required, None)
            self.assertEqual(parameter.default, None)
            self.assertEqual(parameter.status, None)
            self.assertEqual(parameter.constraints, [])
            self.assertEqual(parameter.key_schema, None)
            self.assertEqual(parameter.entry_schema, None)

    def test_single_line_notation(self):
        file = open('test_input/parameter/single_line_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for key, value in data.items():
            parameter = parameter_definition_parser(key, value)
            self.assertEqual(parameter.type, None)
            self.assertEqual(parameter.vertex_type_system, 'ParameterDefinition')
            self.assertEqual(parameter.description, None)
            self.assertEqual(parameter.value, 'test_parameter_value')
            self.assertEqual(parameter.required, None)
            self.assertEqual(parameter.default, None)
            self.assertEqual(parameter.status, None)
            self.assertEqual(parameter.constraints, [])
            self.assertEqual(parameter.key_schema, None)
            self.assertEqual(parameter.entry_schema, None)
