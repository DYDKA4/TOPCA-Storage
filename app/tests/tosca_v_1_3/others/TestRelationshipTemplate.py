import unittest

import yaml

from app.parser.tosca_v_1_3.others.RelationshipTemplate import relationship_template_parser


class TestRelationshipTemplate(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.relationship_template_parser = relationship_template_parser

    # Each test method starts with the keyword test_
    def test_template(self):
        file = open('test_input/relationship_template/relationship.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            relationship = relationship_template_parser(name, value)
            self.assertEqual(relationship.name, 'test_relationship_template_name')
            self.assertEqual(relationship.vertex_type_system, 'RelationshipTemplate')
            self.assertEqual(relationship.type,'test_relationship_type_name')
            self.assertEqual(relationship.description,'test_relationship_type_description')
            for index, metadata in enumerate(relationship.metadata):
                self.assertEqual(metadata.name, 'metadata_key_' + str(index))
                self.assertEqual(metadata.value, 'metadata_value_' + str(index))
            for index, properties in enumerate(relationship.properties):
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.value, 'property_value_test_' + str(index))
            for index, attributes in enumerate(relationship.attributes):
                self.assertEqual(attributes.name, 'test_attribute_name_' + str(index))
                self.assertEqual(attributes.value, 'attribute_value_test_' + str(index))
            for index, interface in enumerate(relationship.interfaces):
                self.assertEqual(interface.name, 'test_interface_definition_name_' + str(index))
                self.assertEqual(interface.type, 'test_interface_type_' + str(index))
            self.assertEqual(relationship.copy, 'test_source_relationship_template_name')
