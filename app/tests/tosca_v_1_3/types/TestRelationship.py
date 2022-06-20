import unittest

import yaml

from app.parser.tosca_v_1_3.types.RelationshipType import relationship_type_parser


class TestRelationship(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.policy_type_parser = relationship_type_parser

    # Each test method starts with the keyword test_
    def test_relationship(self):
        file = open('test_input/relationship_type/relationship.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            relationship = relationship_type_parser(name, value)
            self.assertEqual(relationship.vertex_type_system, 'RelationshipType')
            self.assertEqual(relationship.name, 'test_relationship_type_name')
            self.assertEqual(relationship.derived_from, 'test_parent_relationship_type_name')
            self.assertEqual(relationship.version, 'test_version_number')
            for index, metadata in enumerate(relationship.metadata):
                self.assertEqual(metadata.name, 'metadata_key_' + str(index))
                self.assertEqual(metadata.value, 'metadata_value_' + str(index))
            self.assertEqual(relationship.description, 'test_relationship_description')
            for index, properties in enumerate(relationship.properties):
                self.assertEqual(properties.type, 'test_property_name_' + str(index))
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.description, 'test_property_description_' + str(index))
            for index, attribute in enumerate(relationship.attributes):
                self.assertEqual(attribute.name, 'attribute_name_' + str(index))
                self.assertEqual(attribute.type, 'attribute_type_' + str(index))
            for index, interface in enumerate(relationship.interfaces):
                self.assertEqual(interface.name, 'test_interface_definition_name_' + str(index))
                self.assertEqual(interface.type, 'test_interface_type_' + str(index))
            for index, valid_target_types in enumerate(relationship.valid_target_types):
                self.assertEqual(valid_target_types, 'capability_type_name_' + str(index))

