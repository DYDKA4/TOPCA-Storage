import unittest

import yaml

from app.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import \
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
        self.assertEqual(operation.primary_artifact_name, 'test_primary_artifact_name')
        self.assertIsNone(operation.primary_definition)
        self.assertEqual(operation.list_of_dependent_artifact_names, [])
        self.assertEqual(operation.list_of_dependent_artifact_definitions, [])
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
        self.assertIsNone(operation.primary_artifact_name)
        self.assertEqual(operation.primary_definition.name, 'test_artifact_name')
        self.assertEqual(operation.list_of_dependent_artifact_names, [])
        self.assertEqual(operation.list_of_dependent_artifact_definitions, [])
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
        self.assertEqual(operation.primary_artifact_name, 'test_primary_artifact_name')
        self.assertIsNone(operation.primary_definition)
        for index, dependency in enumerate(operation.list_of_dependent_artifact_names):
            self.assertEqual(dependency, 'test_artifact_name_' + str(index))
        self.assertEqual(operation.list_of_dependent_artifact_definitions, [])
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
        self.assertIsNone(operation.primary_artifact_name)
        self.assertEqual(operation.primary_definition.name, 'test_artifact_name')
        self.assertEqual(operation.list_of_dependent_artifact_names, [])
        for index, dependency in enumerate(operation.list_of_dependent_artifact_definitions):
            self.assertEqual(dependency.name, 'test_artifact_name_' + str(index))
        self.assertEqual(operation.operation_host, 'SELF')
        self.assertEqual(operation.timeout, 60)


