import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.definitions.OperationDefinition import operation_definition_parser


class TestOperation(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.operation_definition_parser = operation_definition_parser

    # Each test method starts with the keyword test_
    def test_short_notation(self):
        file = open('test_input/operation/short_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            operation = operation_definition_parser(name, value)
            self.assertEqual(operation.name, 'operation_test_name')
            self.assertEqual(operation.implementation, 'implementation_artifact_test_name')
            self.assertEqual(operation.vertex_type_system, 'OperationDefinition')
            self.assertIsNone(operation.description)
            self.assertEqual(operation.inputs, [])
            self.assertEqual(operation.outputs, [])

    def test_extended_notation_for_type(self):
        file = open('test_input/operation/extended_notation_for_type.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            operation = operation_definition_parser(name, value)
            self.assertEqual(operation.name, 'test_operation_name')
            self.assertEqual(operation.vertex_type_system, 'OperationDefinition')
            self.assertEqual(operation.description, 'test_operation_description')
            self.assertEqual(operation.implementation.primary, 'test_primary_artifact_name')
            for index, inputs in enumerate(operation.inputs):
                self.assertEqual(inputs.type, 'test_property_name_' + str(index))
                self.assertEqual(inputs.name, 'test_property_name_' + str(index))
                self.assertEqual(inputs.description, 'test_property_description_' + str(index))
            self.assertEqual(operation.outputs, 'test_value')

    def test_extended_notation_for_template(self):
        file = open('test_input/operation/extended_notation_for_template.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            operation = operation_definition_parser(name, value)
            self.assertEqual(operation.name, 'test_operation_name')
            self.assertEqual(operation.vertex_type_system, 'OperationDefinition')
            self.assertEqual(operation.description, 'test_operation_description')
            self.assertEqual(operation.implementation.primary, 'test_primary_artifact_name')
            for index, inputs in enumerate(operation.inputs):
                self.assertEqual(inputs.name, 'test_property_name_' + str(index))
                self.assertEqual(inputs.value, 'property_value_test_' + str(index))
            self.assertEqual(operation.outputs, [])
