import unittest

import yaml

from parser.parser.tosca_v_1_3.types.GroupType import group_type_parser


class TestGroup(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.group_type_parser = group_type_parser

    # Each test method starts with the keyword test_
    def test_data(self):
        file = open('test_input/group_type/group.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            group = group_type_parser(name, value)
            self.assertEqual(group.vertex_type_system, 'GroupType')
            self.assertEqual(group.name, 'test_group_type_name')
            self.assertEqual(group.derived_from, 'test_parent_group_type_name')
            self.assertEqual(group.version, 'test_version_number')
            for index, metadata in enumerate(group.metadata):
                self.assertEqual(metadata.name, 'metadata_key_' + str(index))
                self.assertEqual(metadata.value, 'metadata_value_' + str(index))
            self.assertEqual(group.description, 'test_group_description')

            for index, attribute in enumerate(group.attributes):
                self.assertEqual(attribute.name, 'attribute_name_' + str(index))
                self.assertEqual(attribute.type, 'attribute_type_' + str(index))

            for index, properties in enumerate(group.properties):
                self.assertEqual(properties.type, 'test_property_name_' + str(index))
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.description, 'test_property_description_' + str(index))
            for index, member in enumerate(group.members):
                self.assertEqual(member, 'valid_member_type_' + str(index))
