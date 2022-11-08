import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.types.CapabilityType import capability_type_parser


class TestCapability(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.capability_type_parser = capability_type_parser

    # Each test method starts with the keyword test_
    def test_capability(self):
        file = open('test_input/capability_type/capability.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            capability = capability_type_parser(name, value)
            self.assertEqual(capability.vertex_type_system, 'CapabilityType')
            self.assertEqual(capability.name, 'test_capability_type_name')
            self.assertEqual(capability.derived_from, 'test_parent_capability_type_name')
            self.assertEqual(capability.version, 'test_version_number')
            self.assertEqual(capability.description, 'test_capability_description')
            for index, properties in enumerate(capability.properties):
                self.assertEqual(properties.type, 'test_property_name_' + str(index))
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.description, 'test_property_description_' + str(index))
            for index, attribute in enumerate(capability.attributes):
                self.assertEqual(attribute.name, 'attribute_name_' + str(index))
                self.assertEqual(attribute.type, 'attribute_type_' + str(index))
            for index, valid_source in enumerate(capability.valid_source_types):
                self.assertEqual(valid_source, 'node_type_name_' + str(index))
