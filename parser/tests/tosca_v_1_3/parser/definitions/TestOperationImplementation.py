import unittest

import yaml

from parser.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import \
    operation_implementation_definition_parser


class TestOperationImplementation(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.operation_implementation_definition_parser = operation_implementation_definition_parser

    # Each test method starts with the keyword test_
    def test_short_notation(self):
        file = open('test_input/operation_implementation/short_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        data = data.get('implementation')
        operation = operation_implementation_definition_parser(data)
        self.assertEqual(operation.vertex_type_system, 'OperationImplementationDefinition')
        self.assertEqual(operation.primary, 'test_primary_artifact_name')
        self.assertEqual(operation.dependencies, [])
        self.assertIsNone(operation.operation_host)
        self.assertIsNone(operation.timeout)

    def test_short_notation_with_artifact_definition(self):
        file = open('test_input/operation_implementation/short_notation_with_artifact_definition.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        data = data.get('implementation')
        operation = operation_implementation_definition_parser(data)
        self.assertEqual(operation.vertex_type_system, 'OperationImplementationDefinition')
        self.assertEqual(operation.primary.name, 'test_artifact_name')
        self.assertEqual(operation.dependencies, [])
        self.assertIsNone(operation.operation_host)
        self.assertIsNone(operation.timeout)

    def test_short_notation_multiple_artifact(self):
        file = open('test_input/operation_implementation/short_notation_multiple_artifact.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        data = data.get('implementation')
        operation = operation_implementation_definition_parser(data)
        self.assertEqual(operation.vertex_type_system, 'OperationImplementationDefinition')
        self.assertEqual(operation.primary, 'test_primary_artifact_name')
        for index, dependency in enumerate(operation.dependencies):
            self.assertEqual(dependency, 'test_artifact_name_' + str(index))
        self.assertEqual(operation.operation_host, 'SELF')
        self.assertEqual(operation.timeout, 60)

    def test_extended_notation_with_multiple_artifact(self):
        file = open('test_input/operation_implementation/extended_notation_with_multiple_artifact.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        data = data.get('implementation')
        operation = operation_implementation_definition_parser(data)
        self.assertEqual(operation.vertex_type_system, 'OperationImplementationDefinition')
        self.assertEqual(operation.primary.name, 'test_artifact_name')
        for index, dependency in enumerate(operation.dependencies):
            self.assertEqual(dependency.name, 'test_artifact_name_' + str(index))
        self.assertEqual(operation.operation_host, 'SELF')
        self.assertEqual(operation.timeout, 60)


