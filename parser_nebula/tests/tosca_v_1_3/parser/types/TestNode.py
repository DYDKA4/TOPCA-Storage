import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.types.NodeType import node_type_parser


class TestNode(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.node_type_parser = node_type_parser

    # Each test method starts with the keyword test_
    def test_node(self):
        file = open('test_input/node_type/node.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            node = node_type_parser(name, value)
            self.assertEqual(node.vertex_type_system, 'NodeType')
            self.assertEqual(node.name, 'test_node_type_name')
            self.assertEqual(node.derived_from, 'test_parent_node_type_name')
            self.assertEqual(node.version, 'test_version_number')
            for index, metadata in enumerate(node.metadata):
                self.assertEqual(metadata.name, 'metadata_key_' + str(index))
                self.assertEqual(metadata.value, 'metadata_value_' + str(index))
            self.assertEqual(node.description, 'test_node_type_description')
            for index, properties in enumerate(node.properties):
                self.assertEqual(properties.type, 'test_property_name_' + str(index))
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.description, 'test_property_description_' + str(index))
            for index, attribute in enumerate(node.attributes):
                self.assertEqual(attribute.name, 'attribute_name_' + str(index))
                self.assertEqual(attribute.type, 'attribute_type_' + str(index))
            for index, requirement in enumerate(node.requirements):
                self.assertEqual(requirement.name, 'test_requirement_definition_name_' + str(index))
                self.assertEqual(requirement.capability, 'test_capability_type_name_' + str(index))
            for index, interface in enumerate(node.interfaces):
                self.assertEqual(interface.name, 'test_interface_definition_name_' + str(index))
                self.assertEqual(interface.type, 'test_interface_type_' + str(index))
            for index, capabilities in enumerate(node.capabilities):
                self.assertEqual(capabilities.name, 'test_capability_definition_name_' + str(index))
                self.assertEqual(capabilities.type, 'test_capability_type_' + str(index))
            for index, artifact in enumerate(node.artifacts):
                self.assertEqual(artifact.name, 'test_artifact_name_' + str(index))
                self.assertEqual(artifact.artifact_file_URI, 'test_artifact_file_URI_' + str(index))
