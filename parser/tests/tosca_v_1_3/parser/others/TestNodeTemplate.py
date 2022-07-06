import unittest

import yaml

from parser.parser.tosca_v_1_3.others.NodeTemplate import node_template_parser


class TestNodeTemplate(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.node_template_parser = node_template_parser

    # Each test method starts with the keyword test_
    def test_template(self):
        file = open('test_input/node_template/template.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            node = node_template_parser(name, value)
            self.assertEqual(node.description,'test_node_template_description')
            self.assertEqual(node.type, 'test_node_type_name')
            self.assertEqual(node.name, 'test_node_template_name')
            self.assertEqual(node.vertex_type_system,'NodeTemplate')
            for index, directive in enumerate(node.directives):
                self.assertEqual(directive.value, 'directive_' + str(index))
            for index, metadata in enumerate(node.metadata):
                self.assertEqual(metadata.name, 'metadata_key_' + str(index))
                self.assertEqual(metadata.value, 'metadata_value_' + str(index))
            for index, properties in enumerate(node.properties):
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.value, 'property_value_test_' + str(index))
            for index, attributes in enumerate(node.attributes):
                self.assertEqual(attributes.name, 'test_attribute_name_' + str(index))
                self.assertEqual(attributes.value, 'attribute_value_test_' + str(index))
            for index, requirement in enumerate(node.requirements):
                self.assertEqual(requirement.name, 'test_requirement_name_' + str(index))
                self.assertEqual(requirement.node, 'test_node_template_name_' + str(index))
            for index, capability in enumerate(node.capabilities):
                self.assertEqual(capability.name,'test_capability_name_' + str(index))
            for index, interface in enumerate(node.interfaces):
                self.assertEqual(interface.name, 'test_interface_definition_name_' + str(index))
                self.assertEqual(interface.type, 'test_interface_type_' + str(index))
            for index, artifact in enumerate(node.artifacts):
                self.assertEqual(artifact.name, 'test_artifact_name_' + str(index))
                self.assertEqual(artifact.artifact_file_URI, 'test_artifact_file_URI_' + str(index))
            self.assertEqual(node.copy, 'test_source_node_template_name')
