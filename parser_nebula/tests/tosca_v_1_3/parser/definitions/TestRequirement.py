import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.definitions.RequirementDefinition import requirement_definition_parser


class TestRequirement(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.requirement_definition_parser = requirement_definition_parser

    # Each test method starts with the keyword test_
    def test_short_notation(self):
        file = open('test_input/requirement/short_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            requirement = requirement_definition_parser(name, value)
            self.assertEqual(requirement.vertex_type_system, 'RequirementDefinition')
            self.assertEqual(requirement.name, 'test_requirement_definition_name')
            self.assertEqual(requirement.capability, 'test_capability_type_name')
            self.assertEqual(requirement.node, None)
            self.assertEqual(requirement.relationship, None)
            self.assertEqual(requirement.interfaces, [])
            self.assertEqual(requirement.occurrences, None)

    def test_extended_grammar(self):
        file = open('test_input/requirement/extended_grammar.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            requirement = requirement_definition_parser(name, value)
            self.assertEqual(requirement.vertex_type_system, 'RequirementDefinition')
            self.assertEqual(requirement.name, 'test_requirement_definition_name')
            self.assertEqual(requirement.capability, 'test_capability_type_name')
            self.assertEqual(requirement.node, 'test_node_type_name')
            self.assertEqual(requirement.relationship, 'test_relationship_type_name')
            self.assertEqual(requirement.interfaces, [])
            self.assertEqual(requirement.occurrences.minimum, 0)
            self.assertEqual(requirement.occurrences.maximum, 10)

    def test_extended_grammar_with_property(self):
        file = open('test_input/requirement/extended_grammar_with_property.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            requirement = requirement_definition_parser(name, value)
            self.assertEqual(requirement.vertex_type_system, 'RequirementDefinition')
            self.assertEqual(requirement.name, 'test_requirement_definition_name')
            self.assertEqual(requirement.capability, 'test_capability_type_name')
            self.assertEqual(requirement.node, 'test_node_type_name')
            self.assertEqual(requirement.relationship, 'test_relationship_type_name')
            for index, interface in enumerate(requirement.interfaces):
                self.assertEqual(interface.name, 'test_interface_definition_name_' + str(index))
                self.assertEqual(interface.type, 'test_interface_type_' + str(index))
            self.assertEqual(requirement.occurrences.minimum, 0)
            self.assertEqual(requirement.occurrences.maximum, 10)
