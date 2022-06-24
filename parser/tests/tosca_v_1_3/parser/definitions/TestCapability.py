import unittest

import yaml

from parser.parser.tosca_v_1_3.definitions.CapabilityDefinition import capability_definition_parser


class TestCapability(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.capability_definition_parser = capability_definition_parser

    # Each test method starts with the keyword test_
    def test_short_notation(self):
        file = open('test_input/capability/short_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            capability = capability_definition_parser(name, value)
            self.assertEqual(capability.vertex_type_system, 'CapabilityDefinition')
            self.assertEqual(capability.name, 'test_capability_definition_name')
            self.assertEqual(capability.type, 'test_capability_type')
            self.assertEqual(capability.description, None)
            self.assertEqual(capability.properties, [])
            self.assertEqual(capability.attributes, [])
            self.assertEqual(capability.valid_source_types, [])
            self.assertEqual(capability.occurrences, [])

    def test_extended_notation(self):
        file = open('test_input/capability/extended_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            capability = capability_definition_parser(name, value)
            self.assertEqual(capability.vertex_type_system, 'CapabilityDefinition')
            self.assertEqual(capability.name, 'test_capability_definition_name')
            self.assertEqual(capability.type, 'test_capability_type')
            self.assertEqual(capability.description, 'test_capability_description')
            for index, properties in enumerate(capability.properties):
                self.assertEqual(properties.type, 'test_property_name_' + str(index))
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.description, 'test_property_description_' + str(index))
            for index, attribute in enumerate(capability.attributes):
                self.assertEqual(attribute.name, 'attribute_name_' + str(index))
                self.assertEqual(attribute.type, 'attribute_type_' + str(index))
            for index, valid_source, in enumerate(capability.valid_source_types):
                self.assertEqual(valid_source, 'node_type_name_' + str(index))
            self.assertEqual(capability.occurrences, [0, 10])
