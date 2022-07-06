import unittest

import yaml

from parser.parser.tosca_v_1_3.definitions.ImportDefinition import import_definition_parser


class TestImport(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.import_definition_parser = import_definition_parser

    # Each test method starts with the keyword test_
    def test_single_line(self):
        file = open('test_input/import/single_line.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        import_definition = import_definition_parser(data)
        self.assertEqual(import_definition.vertex_type_system, 'ImportDefinition')
        self.assertEqual(import_definition.file, 'test_URI_1')
        self.assertEqual(import_definition.repository, None)
        self.assertEqual(import_definition.namespace_uri, None)
        self.assertEqual(import_definition.namespace_prefix, None)

    def test_multi_line(self):
        file = open('test_input/import/multi_line.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        import_definition = import_definition_parser(data)
        self.assertEqual(import_definition.vertex_type_system, 'ImportDefinition')
        self.assertEqual(import_definition.file, 'test_URI_0')
        self.assertEqual(import_definition.repository, 'test_repository_name_0')
        self.assertEqual(import_definition.namespace_uri, 'test_definition_namespace_uri_0')
        self.assertEqual(import_definition.namespace_prefix, 'test_definition_namespace_prefix_test_0')
