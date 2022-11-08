import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.definitions.ArtifactDefinition import artifact_definition_parser


class TestArtifact(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.artifact_definition_parser = artifact_definition_parser

    # Each test method starts with the keyword test_
    def test_short_notation(self):
        file = open('test_input/artifact/TestArtifactShort.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            artifact = artifact_definition_parser(name, value)
            self.assertEqual(artifact.name, 'test_artifact_name')
            self.assertEqual(artifact.vertex_type_system, 'ArtifactDefinition')
            self.assertEqual(artifact.artifact_file_URI, 'test_artifact_file_URI')
            self.assertEqual(artifact.description, None)
            self.assertEqual(artifact.type, None)
            self.assertEqual(artifact.file, None)
            self.assertEqual(artifact.repository, None)
            self.assertEqual(artifact.deploy_path, None)
            self.assertEqual(artifact.version, None)
            self.assertEqual(artifact.checksum, None)
            self.assertEqual(artifact.checksum_algorithm, None)
            self.assertEqual(artifact.properties, [])

    def test_set_property(self):
        file = open('test_input/artifact/TestArtifactSingleProperty.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            artifact = artifact_definition_parser(name, value)
            self.assertEqual(artifact.name, 'test_artifact_name')
            self.assertEqual(artifact.vertex_type_system, 'ArtifactDefinition')
            self.assertEqual(artifact.artifact_file_URI, None)
            self.assertEqual(artifact.description, 'test_description')
            self.assertEqual(artifact.type, 'test_type')
            self.assertEqual(artifact.file, 'test_file')
            self.assertEqual(artifact.repository, 'test_repository')
            self.assertEqual(artifact.deploy_path, 'test_deploy_path')
            self.assertEqual(artifact.version, 'test_version')
            self.assertEqual(artifact.checksum, 'test_checksum')
            self.assertEqual(artifact.checksum_algorithm, 'test_checksum_algorithm')
            for properties in artifact.properties:
                self.assertEqual(properties.value, 'property_value_test')

    def test_set_properties(self):
        file = open('test_input/artifact/TestArtifactMutualProperties.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            artifact = artifact_definition_parser(name, value)
            self.assertEqual(artifact.name, 'test_artifact_name')
            self.assertEqual(artifact.vertex_type_system, 'ArtifactDefinition')
            self.assertEqual(artifact.artifact_file_URI, None)
            self.assertEqual(artifact.description, 'test_description')
            self.assertEqual(artifact.type, 'test_type')
            self.assertEqual(artifact.file, 'test_file')
            self.assertEqual(artifact.repository, 'test_repository')
            self.assertEqual(artifact.deploy_path, 'test_deploy_path')
            self.assertEqual(artifact.version, 'test_version')
            self.assertEqual(artifact.checksum, 'test_checksum')
            self.assertEqual(artifact.checksum_algorithm, 'test_checksum_algorithm')
            for index, properties in enumerate(artifact.properties):
                self.assertEqual(properties.value, 'property_value_test_' + str(index))
