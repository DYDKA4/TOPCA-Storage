import unittest

import yaml

from parser.parser.tosca_v_1_3.others.ConstraintСlause import constraint_clause_parser


class TestConstraintClause(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.constraint_clause_parser = constraint_clause_parser

    # Each test method starts with the keyword test_
    def test_equal(self):
        file = open('test_input/constrain_clause/equal.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        constraint = constraint_clause_parser(data)
        self.assertEqual(constraint.operator, 'equal')
        self.assertEqual(constraint.vertex_type_system, 'ConstraintClause')
        self.assertEqual(constraint.value, '2')

    def test_greater_than(self):
        file = open('test_input/constrain_clause/greater_than.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        constraint = constraint_clause_parser(data)
        self.assertEqual(constraint.operator, 'greater_than')
        self.assertEqual(constraint.vertex_type_system, 'ConstraintClause')
        self.assertEqual(constraint.value, '1')
