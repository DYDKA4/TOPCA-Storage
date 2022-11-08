import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.assignments.CapabilityAssignment import capability_assignment_parser


class TestCapability(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.capability_assignment_parser = capability_assignment_parser

    # Each test method starts with the keyword test_
    def test_set_property(self):
        file = open('test_input/capability/TestCapabilitySingleProperty.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)

        for name, value in data.items():
            capability = self.capability_assignment_parser(name, value)
            self.assertEqual(capability.name, 'test_capability_name')
            for properties in capability.properties:
                self.assertEqual(properties.value, 'property_value_test')
            self.assertEqual(capability.attributes, [])
            self.assertEqual(capability.occurrences, None)
            self.assertEqual(capability.vertex_type_system, 'CapabilityAssignment')

    def test_set_properties(self):
        file = open('test_input/capability/TestCapabilityMutualProperties.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)

        for name, value in data.items():
            capability = self.capability_assignment_parser(name, value)
            self.assertEqual(capability.name, 'test_capability_name')
            for index, properties in enumerate(capability.properties):
                self.assertEqual(properties.value, 'property_value_test_' + str(index))
            self.assertEqual(capability.attributes, [])
            self.assertEqual(capability.occurrences, None)
            self.assertEqual(capability.vertex_type_system, 'CapabilityAssignment')

    def test_set_attribute(self):
        file = open('test_input/capability/TestCapabilitySingleAttribute.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)

        for name, value in data.items():
            capability = self.capability_assignment_parser(name, value)
            self.assertEqual(capability.name, 'test_capability_name')
            for attributes in capability.attributes:
                self.assertEqual(attributes.value, 'attribute_value_test')
            self.assertEqual(capability.properties, [])
            self.assertEqual(capability.occurrences, None)
            self.assertEqual(capability.vertex_type_system, 'CapabilityAssignment')

    def test_set_occurrences(self):
        file = open('test_input/capability/TestCapabilityWithOccurrences.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)

        for name, value in data.items():
            capability = self.capability_assignment_parser(name, value)
            self.assertEqual(capability.name, 'test_capability_name')
            self.assertEqual(capability.occurrences.minimum, 1)
            self.assertEqual(capability.occurrences.maximum, 10)
            self.assertEqual(capability.properties, [])
            self.assertEqual(capability.attributes, [])
            self.assertEqual(capability.vertex_type_system, 'CapabilityAssignment')


if __name__ == '__main__':
    unittest.main()
