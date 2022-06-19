import unittest

import yaml

from app.parser.tosca_v_1_3.definitions.ConditionClauseDefinition import condition_clause_definition_parser


class TestConditionClause(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.condition_clause_definition_parser = condition_clause_definition_parser

    # Each test method starts with the keyword test_
    def test_simple(self):
        file = open('test_input/condition_clause/simle.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        self.assertEqual(event.type, 'condition')
        self.assertNotEqual(event.operands.get('assert'), [])
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')
        for assert_dict in event.operands.get('assert'):
            for assert_attribute, asset_conditions in assert_dict.items():
                self.assertEqual(assert_attribute, 'my_attribute')
                for assert_condition in asset_conditions:
                    self.assertEqual(assert_condition.operator, 'equal')
                    self.assertEqual(assert_condition.value, 'my_value')

    def test_two_asserts(self):
        file = open('test_input/condition_clause/two_asserts.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        self.assertEqual(event.type, 'condition')
        self.assertNotEqual(event.operands.get('assert'), [])
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')
        for index, assert_dict in enumerate(event.operands.get('assert')):
            for assert_attribute, asset_conditions in assert_dict.items():
                self.assertEqual(assert_attribute, 'my_attribute_' + str(index))
                for assert_index, assert_condition in enumerate(asset_conditions):
                    self.assertEqual(assert_condition.operator, 'equal_' + str(assert_index))
                    self.assertEqual(assert_condition.value, 'my_value_' + str(assert_index))

    def test_and_clause(self):
        file = open('test_input/condition_clause/and_clause.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        event = event
        self.assertEqual(event.type, 'condition')
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')
        self.assertNotEqual(event.operands.get('and'), [])
        for and_dict in event.operands.get('and'):
            self.assertNotEqual(and_dict.operands.get('assert'), [])
            for index, assert_dict in enumerate(and_dict.operands.get('assert')):
                self.assertNotEqual(assert_dict, {})
                for assert_attribute, asset_conditions in assert_dict.items():
                    self.assertEqual(assert_attribute, 'my_attribute_' + str(index))
                    self.assertNotEqual(asset_conditions, [])
                    for assert_index, assert_condition in enumerate(asset_conditions):
                        self.assertEqual(assert_condition.operator, 'equal')
                        self.assertEqual(assert_condition.value, 'my_value_' + str(assert_index))

    def test_or_clause(self):
        file = open('test_input/condition_clause/or_clause.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        event = event
        self.assertEqual(event.type, 'condition')
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')
        self.assertNotEqual(event.operands.get('or'), [])
        for and_dict in event.operands.get('or'):
            self.assertNotEqual(and_dict.operands.get('assert'), [])
            for index, assert_dict in enumerate(and_dict.operands.get('assert')):
                self.assertNotEqual(assert_dict, {})
                for assert_attribute, asset_conditions in assert_dict.items():
                    self.assertEqual(assert_attribute, 'my_attribute_' + str(index))
                    self.assertNotEqual(asset_conditions, [])
                    for assert_index, assert_condition in enumerate(asset_conditions):
                        self.assertEqual(assert_condition.operator, 'equal')
                        self.assertEqual(assert_condition.value, 'my_value_' + str(assert_index))

    def test_not_clause(self):
        file = open('test_input/condition_clause/not_clause.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        event = event
        self.assertEqual(event.type, 'condition')
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')
        self.assertNotEqual(event.operands.get('not'), [])
        for and_dict in event.operands.get('not'):
            self.assertNotEqual(and_dict.operands.get('assert'), [])
            for index, assert_dict in enumerate(and_dict.operands.get('assert')):
                self.assertNotEqual(assert_dict, {})
                for assert_attribute, asset_conditions in assert_dict.items():
                    self.assertEqual(assert_attribute, 'my_attribute_' + str(index))
                    self.assertNotEqual(asset_conditions, [])
                    for assert_condition in asset_conditions:
                        self.assertEqual(assert_condition.operator, 'equal')
                        self.assertEqual(assert_condition.value, 'my_value_' + str(index))

    def test_and_with_not_example(self):
        file = open('test_input/condition_clause/and_with_not_example.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        event = event
        self.assertEqual(event.type, 'condition')
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')
        self.assertNotEqual(event.operands.get('not'), [])
        for not_dict in event.operands.get('not'):
            self.assertEqual(not_dict.type, 'not')
            self.assertNotEqual(not_dict.operands.get('and'), [])
            for and_dict in not_dict.operands.get('and'):
                self.assertEqual(and_dict.type, 'and')
                self.assertNotEqual(and_dict.operands.get('assert'), [])
                for index, assert_dict in enumerate(and_dict.operands.get('assert')):
                    self.assertNotEqual(assert_dict, {})
                    for assert_attribute, asset_conditions in assert_dict.items():
                        self.assertEqual(assert_attribute, 'my_attribute_' + str(index))
                        self.assertNotEqual(asset_conditions, [])
                        for assert_condition in asset_conditions:
                            self.assertEqual(assert_condition.operator, 'equal')
                            self.assertEqual(assert_condition.value, 'my_value_' + str(index))

    def test_or_with_two_not(self):
        file = open('test_input/condition_clause/or _with_two_not.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        event = event
        self.assertEqual(event.type, 'condition')
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')
        self.assertNotEqual(event.operands.get('or'), [])
        for not_index, or_dict in enumerate(event.operands.get('or')):
            self.assertNotEqual(or_dict.operands.get('not'), [])
            for not_dict in or_dict.operands.get('not'):
                self.assertNotEqual(not_dict.operands.get('assert'), [])
                for index, assert_dict in enumerate(not_dict.operands.get('assert')):
                    self.assertNotEqual(assert_dict, {})
                    for assert_attribute, asset_conditions in assert_dict.items():
                        self.assertEqual(assert_attribute, 'my_attribute_not_' + str(not_index) + str(index))
                        self.assertNotEqual(asset_conditions, [])
                        for assert_condition in asset_conditions:
                            self.assertEqual(assert_condition.operator, 'equal')
                            self.assertEqual(assert_condition.value, 'my_value_' + str(not_index+index))
