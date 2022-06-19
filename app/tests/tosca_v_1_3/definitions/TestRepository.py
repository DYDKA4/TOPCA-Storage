import unittest

import yaml

from app.parser.tosca_v_1_3.definitions.RepositoryDefinition import repository_definition_parser


class TestRepository(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.repository_definition_parser = repository_definition_parser

    # Each test method starts with the keyword test_
    def test_short_notation(self):
        file = open('test_input/repository/single_line.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            repository = repository_definition_parser(name, value)
            self.assertEqual(repository.name, 'test_repository_name')
            self.assertEqual(repository.vertex_type_system, 'RepositoryDefinition')
            self.assertEqual(repository.url, 'test_repository_address')
            self.assertEqual(repository.description, None)
            self.assertEqual(repository.credential, None)

    def test_extended_notation(self):
        file = open('test_input/repository/extended_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            repository = repository_definition_parser(name, value)
            self.assertEqual(repository.name, 'test_repository_name')
            self.assertEqual(repository.vertex_type_system, 'RepositoryDefinition')
            self.assertEqual(repository.url, 'test_repository_address')
            self.assertEqual(repository.description, 'test_repository_description')
            self.assertEqual(repository.credential, 'test_authorization_credential')
