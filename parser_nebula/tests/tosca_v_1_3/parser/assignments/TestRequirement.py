import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.assignments.RequirementAssignment import requirement_assignment_parser
from parser_nebula.parser.tosca_v_1_3.definitions.PropertyFilterDefinition import PropertyFilterDefinition


class TestRequirement(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.requirement_assignment_parser = requirement_assignment_parser

    # Each test method starts with the keyword test_
    def test_short_notation(self):
        file = open('test_input/requirement/short_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)

        for name, value in data.items():
            requirement = self.requirement_assignment_parser(name, value)
            self.assertEqual(requirement.name, 'test_requirement_name')
            self.assertEqual(requirement.vertex_type_system, 'RequirementAssignment')
            self.assertEqual(requirement.node, 'test_node_template_name')
            self.assertEqual(requirement.relationship, None)
            self.assertEqual(requirement.properties, [])
            self.assertEqual(requirement.interfaces, [])
            self.assertEqual(requirement.capability, None)
            self.assertEqual(requirement.node_filter, None)
            self.assertEqual(requirement.occurrences, [])

    def test_extended_notation(self):
        file = open('test_input/requirement/extended_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)

        for name, value in data.items():
            requirement = self.requirement_assignment_parser(name, value)
            self.assertEqual(requirement.name, 'test_requirement_name')
            self.assertEqual(requirement.vertex_type_system, 'RequirementAssignment')
            self.assertEqual(requirement.node, 'test_node_template_name')
            self.assertEqual(requirement.relationship, 'test_relationship_template_name')
            self.assertEqual(requirement.properties, [])
            self.assertEqual(requirement.interfaces, [])
            self.assertEqual(requirement.capability, 'test_capability_symbolic_name')
            self.assertEqual(len(requirement.node_filter.properties), 2)
            for index, properties in enumerate(requirement.node_filter.properties):
                properties: PropertyFilterDefinition
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                for index_2, property_constraint in enumerate(properties.property_constraint):
                    self.assertEqual(property_constraint.operator, 'equal_' + str(index_2))
                    self.assertEqual(property_constraint.value, 'value_' + str(index_2))
            self.assertEqual(len(requirement.node_filter.capabilities), 0)
            self.assertEqual(requirement.occurrences.minimum, 0)
            self.assertEqual(requirement.occurrences.maximum, 10)

    def test_extended_notation_with_property(self):
        file = open('test_input/requirement/extended_notation_with_property.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            requirement = self.requirement_assignment_parser(name, value)
            self.assertEqual(requirement.name, 'test_requirement_name')
            self.assertEqual(requirement.vertex_type_system, 'RequirementAssignment')
            self.assertEqual(requirement.node, 'test_node_template_name')
            self.assertEqual(requirement.relationship, 'test_relationship_template_name')
            for index, properties in enumerate(requirement.properties):
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.value, 'property_value_test_' + str(index))
            for index, interface in enumerate(requirement.interfaces):
                self.assertEqual(interface.name, 'test_interface_definition_name_' + str(index))
                self.assertEqual(interface.type, 'test_interface_type_' + str(index))
            self.assertEqual(requirement.capability, 'test_capability_symbolic_name')
            self.assertEqual(requirement.node_filter, None)
            self.assertEqual(requirement.occurrences, [])


if __name__ == '__main__':
    unittest.main()