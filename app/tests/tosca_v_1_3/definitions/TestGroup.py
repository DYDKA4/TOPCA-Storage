import unittest

import yaml

from app.parser.tosca_v_1_3.definitions.GroupDefinition import group_definition_parser


class TestGroup(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.group_definition_parser = group_definition_parser

    # Each test method starts with the keyword test_
    def test_notation(self):
        file = open('test_input/group/notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            group = group_definition_parser(name, value)
            self.assertEqual(group.name, 'test_group_name')
            self.assertEqual(group.vertex_type_system, 'GroupDefinition')
            self.assertEqual(group.type, 'test_group_type_name')
            self.assertEqual(group.description, 'test_group_description')
            self.assertNotEqual(group.metadata, [])
            for index, metadata in enumerate(group.metadata):
                self.assertEqual(metadata.name, 'metadata_key_' + str(index))
                self.assertEqual(metadata.value, 'metadata_value_' + str(index))
            self.assertNotEqual(group.properties, [])
            for index, properties in enumerate(group.properties):
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.value, 'property_value_test_' + str(index))
            self.assertNotEqual(group.attributes, [])
            for index, attributes in enumerate(group.attributes):
                self.assertEqual(attributes.name, 'test_attribute_name_' + str(index))
                self.assertEqual(attributes.value, 'attribute_value_test_' + str(index))
            self.assertNotEqual(group.members, [])
            for index, member in enumerate(group.members):
                self.assertEqual(member, 'node_template_' + str(index))
