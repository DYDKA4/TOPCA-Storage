import unittest

import yaml

from parser.parser.tosca_v_1_3.definitions.AssertDefinition import AssertDefinition
from parser.parser.tosca_v_1_3.definitions.ConditionClauseDefinition import condition_clause_definition_parser, \
    ConditionClauseDefinition
from parser.parser.tosca_v_1_3.others.ConstraintСlause import ConstraintClause


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
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')

        self.assertNotEqual(event.condition_assert, [])
        self.assertEqual(len(event.condition_assert), 1)
        for assert_definition in event.condition_assert:
            assert_definition: AssertDefinition
            self.assertEqual(assert_definition.attribute_name, 'my_attribute')
            self.assertEqual(len(assert_definition.constraint_clauses), 1)
            for constraint_clause in assert_definition.constraint_clauses:
                self.assertEqual(constraint_clause.operator, 'equal')
                self.assertEqual(constraint_clause.value, 'my_value')

    def test_two_asserts(self):
        file = open('test_input/condition_clause/two_asserts.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        self.assertEqual(event.type, 'condition')
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')
        self.assertEqual(len(event.condition_assert), 2)
        for index, assert_definition in enumerate(event.condition_assert):
            assert_definition: AssertDefinition
            self.assertEqual(assert_definition.attribute_name, 'my_attribute_' + str(index))
            self.assertEqual(len(assert_definition.constraint_clauses), 1)
            for assert_index, constraint_clause in enumerate(assert_definition.constraint_clauses):
                constraint_clause: ConstraintClause
                self.assertEqual(constraint_clause.operator, 'equal_' + str(assert_index))
                self.assertEqual(constraint_clause.value, 'my_value_' + str(assert_index))

    def test_and_clause(self):
        file = open('test_input/condition_clause/and_clause.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        event = event
        self.assertEqual(event.type, 'condition')
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')
        self.assertEqual(len(event.condition_and), 1)
        for and_dict in event.condition_not:
            and_dict: ConditionClauseDefinition
            self.assertEqual(len(and_dict.condition_assert), 2)
            for index, assert_dict in enumerate(and_dict.condition_assert):
                assert_dict: AssertDefinition
                self.assertEqual(len(assert_dict.constraint_clauses), 1)
                self.assertEqual(assert_dict.attribute_name, 'my_attribute_' + str(index))
                for constraint_clause in assert_dict.constraint_clauses:
                    constraint_clause: ConstraintClause
                    self.assertEqual(constraint_clause.operator, 'equal')
                    self.assertEqual(constraint_clause.value, 'my_value_' + str(index))

    def test_or_clause(self):
        file = open('test_input/condition_clause/or_clause.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        event = event
        self.assertEqual(event.type, 'condition')
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')

        self.assertNotEqual(event.condition_or, [])
        self.assertEqual(len(event.condition_or), 1)
        for and_dict in event.condition_or:
            and_dict: ConditionClauseDefinition
            self.assertEqual(len(and_dict.condition_assert), 2)
            for index, assert_dict in enumerate(and_dict.condition_assert):
                assert_dict: AssertDefinition
                self.assertEqual(len(assert_dict.constraint_clauses), 1)
                self.assertEqual(assert_dict.attribute_name, 'my_attribute_' + str(index))
                for constraint_clause in assert_dict.constraint_clauses:
                    constraint_clause: ConstraintClause
                    self.assertEqual(constraint_clause.operator, 'equal')
                    self.assertEqual(constraint_clause.value, 'my_value_' + str(index))

    def test_not_clause(self):
        file = open('test_input/condition_clause/not_clause.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        event = event
        self.assertEqual(event.type, 'condition')
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')
        self.assertEqual(len(event.condition_not), 1)
        for and_dict in event.condition_not:
            and_dict: ConditionClauseDefinition
            self.assertEqual(len(and_dict.condition_assert), 2)
            for index, assert_dict in enumerate(and_dict.condition_assert):
                assert_dict: AssertDefinition
                self.assertEqual(len(assert_dict.constraint_clauses), 1)
                self.assertEqual(assert_dict.attribute_name, 'my_attribute_' + str(index))
                for constraint_clause in assert_dict.constraint_clauses:
                    constraint_clause: ConstraintClause
                    self.assertEqual(constraint_clause.operator, 'equal')
                    self.assertEqual(constraint_clause.value, 'my_value_' + str(index))

    def test_and_with_not_example(self):
        file = open('test_input/condition_clause/and_with_not_example.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        event = condition_clause_definition_parser('condition', data)
        event = event
        self.assertEqual(event.type, 'condition')
        self.assertEqual(event.vertex_type_system, 'ConditionClauseDefinition')
        self.assertEqual(len(event.condition_not), 1)
        for and_dict in event.condition_not:
            and_dict: ConditionClauseDefinition
            self.assertEqual(len(and_dict.condition_and), 1)
            for condition_and in and_dict.condition_and:
                condition_and: ConditionClauseDefinition
                self.assertEqual(len(condition_and.condition_assert), 2)
                for index, assert_dict in enumerate(condition_and.condition_assert):
                    assert_dict: AssertDefinition
                    self.assertEqual(len(assert_dict.constraint_clauses), 1)
                    self.assertEqual(assert_dict.attribute_name, 'my_attribute_' + str(index))
                    for constraint_clause in assert_dict.constraint_clauses:
                        constraint_clause: ConstraintClause
                        self.assertEqual(constraint_clause.operator, 'equal')
                        self.assertEqual(constraint_clause.value, 'my_value_' + str(index))

