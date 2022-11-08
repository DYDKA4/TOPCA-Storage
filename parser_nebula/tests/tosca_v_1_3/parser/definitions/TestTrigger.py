import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.definitions.TriggerDefinition import trigger_definition_parser
from parser_nebula.parser.tosca_v_1_3.others.ConstraintСlause import ConstraintClause


class TestTrigger(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.trigger_definition_parser = trigger_definition_parser

    # Each test method starts with the keyword test_
    def test_simple(self):
        file = open('test_input/trigger/short.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)

        for name, value in data.items():
            trigger = trigger_definition_parser(name, value)
            self.assertEqual(trigger.name, 'test_trigger_name')
            self.assertEqual(trigger.vertex_type_system, 'TriggerDefinition')
            self.assertEqual(trigger.description, 'test_trigger_description')
            self.assertEqual(trigger.event, 'test_event_name')
            self.assertEqual(trigger.schedule_start, 0)
            self.assertEqual(trigger.schedule_end, 1)
            self.assertEqual(trigger.event_filter.node, 'test_node_type_name')
            self.assertNotEqual(trigger.constraint.condition_assert[0].constraint_clauses, [])
            for constraint_clause in trigger.constraint.condition_assert[0].constraint_clauses:
                constraint_clause: ConstraintClause
                self.assertEqual(constraint_clause.value, 'my_value')
            self.assertEqual(trigger.period, None)
            self.assertEqual(trigger.evaluations, None)
            self.assertEqual(trigger.method, None)
            self.assertNotEqual(trigger.action, [])

    def test_extended(self):
        file = open('test_input/trigger/extended.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            trigger = trigger_definition_parser(name, value)
            self.assertEqual(trigger.name, 'test_trigger_name')
            self.assertEqual(trigger.vertex_type_system, 'TriggerDefinition')
            self.assertEqual(trigger.description, 'test_trigger_description')
            self.assertEqual(trigger.event, 'test_event_name')
            self.assertEqual(trigger.schedule_start, 0)
            self.assertEqual(trigger.schedule_end, 1)
            self.assertEqual(trigger.event_filter.node, 'test_node_type_name')
            self.assertNotEqual(trigger.constraint.condition_assert[0].constraint_clauses, [])
            for constraint_clause in trigger.constraint.condition_assert[0].constraint_clauses:
                constraint_clause: ConstraintClause
                self.assertEqual(constraint_clause.value, 'my_value')
            self.assertEqual(trigger.period, '60 sec')
            self.assertEqual(trigger.evaluations, 1)
            self.assertEqual(trigger.method, 'average')
            self.assertNotEqual(trigger.action, [])

