import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.definitions.PropertyFilterDefinition import property_filter_definition_parser


class TestPropertyFilter(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.property_filter_definition_parser = property_filter_definition_parser

    # Each test method starts with the keyword test_
    def test_short_notation(self):
        file = open('test_input/property_filter/short_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            property_filter = property_filter_definition_parser(name, value)
            self.assertEqual(property_filter.name, 'test_property_name')
            self.assertEqual(property_filter.property_constraint[0].operator, 'equal')
            self.assertEqual(property_filter.vertex_type_system, 'PropertyFilterDefinition')
            self.assertEqual(property_filter.property_constraint[0].value, '2')

    def test_extended_notation(self):
        file = open('test_input/property_filter/extended_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            property_filter = property_filter_definition_parser(name, value)
            self.assertEqual(property_filter.name, 'test_property_name')
            # self.assertEqual(property_filter.property_constraint, None)
            self.assertEqual(property_filter.vertex_type_system, 'PropertyFilterDefinition')
            for index, property_constraint in enumerate(property_filter.property_constraint):
                self.assertEqual(property_constraint.operator, 'equal_'+str(index))
                self.assertEqual(property_constraint.value, 'value_'+str(index))

    def test_alternative_extended_notation(self):
        file = open('test_input/property_filter/alternative_extended_notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            property_filter = property_filter_definition_parser(name, value)
            self.assertEqual(property_filter.name, 'test_property_name')
            # self.assertEqual(property_filter.property_constraint, None)
            self.assertEqual(property_filter.vertex_type_system, 'PropertyFilterDefinition')
            for index, property_constraint in enumerate(property_filter.property_constraint):
                self.assertEqual(property_constraint.operator, 'equal_'+str(index))
                self.assertEqual(property_constraint.value, 'value_'+str(index))

