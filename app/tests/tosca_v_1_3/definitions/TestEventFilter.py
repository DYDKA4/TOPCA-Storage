import unittest

import yaml

from app.parser.tosca_v_1_3.definitions.EventFilterDefinition import EventFilterDefinition


class TestEventFilter(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.EventFilterDefinition = EventFilterDefinition

    # Each test method starts with the keyword test_
    def test_parser(self):
        file = open('test_input/event_filter/event.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = EventFilterDefinition(data.get('node'), data.get('requirement'), data.get('capability'))
        self.assertEqual(event.node, 'test_node_type_name')
        self.assertEqual(event.requirement, 'test_requirement_name')
        self.assertEqual(event.capability, 'test_capability_name')
