import unittest

import yaml

from app.parser.tosca_v_1_3.definitions.NodeFilterDefinition import node_filter_definition_parser


class TestNodeFilter(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.node_filter_definition_parser = node_filter_definition_parser

    # Each test method starts with the keyword test_
    def test_short_notation(self):
        file = open('test_input/node_filter/node_filter.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        node_filter = node_filter_definition_parser(data.get('node_filter'))
        self.assertEqual(node_filter.vertex_type_system, 'NodeFilterDefinition')
        for index, properties in enumerate(node_filter.properties):
            self.assertEqual(properties.name, 'test_property_name_' + str(index))
            for index_2, property_constraint in enumerate(properties.property_constraint_list):
                self.assertEqual(property_constraint.operator, 'equal_' + str(index_2))
                self.assertEqual(property_constraint.value, 'value_' + str(index_2))
        for capabilities_name, capabilities_value in node_filter.capabilities.items():
            for capabilities in capabilities_value:
                for index_2, property_constraint in enumerate(capabilities.property_constraint_list):
                    self.assertEqual(property_constraint.operator, 'equal_' + str(index_2))
                    self.assertEqual(property_constraint.value, 'value_' + str(index_2))


