import unittest

import yaml

from parser.parser.tosca_v_1_3.types.ArtifactType import artifact_type_parser


class TestArtifact(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.artifact_type_parser = artifact_type_parser

    # Each test method starts with the keyword test_
    def test_template(self):
        file = open('test_input/artifact_type/artifact.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            artifact = artifact_type_parser(name, value)
            self.assertEqual(artifact.vertex_type_system, 'ArtifactType')
            self.assertEqual(artifact.name, 'test_artifact_type_name')
            self.assertEqual(artifact.derived_from, 'test_parent_artifact_type_name')
            self.assertEqual(artifact.version, 'test_version_number')
            for index, metadata in enumerate(artifact.metadata):
                self.assertEqual(metadata.name, 'metadata_key_' + str(index))
                self.assertEqual(metadata.value, 'metadata_value_' + str(index))
            self.assertEqual(artifact.description, 'test_artifact_description')
            self.assertEqual(artifact.mime_type, 'test_mime_type_string')
            for index, file_ext in enumerate(artifact.file_ext):
                self.assertEqual(file_ext, 'file_extensions_' + str(index))
            for index, properties in enumerate(artifact.properties):
                self.assertEqual(properties.type, 'test_property_name_' + str(index))
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.description, 'test_property_description_' + str(index))
