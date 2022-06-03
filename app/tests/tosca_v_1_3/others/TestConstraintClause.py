import unittest

import yaml

from app.parser.tosca_v_1_3.others.ConstraintСlause import constraint_clause_parser


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
        artifact = constraint_clause_parser(data)
        self.assertEqual(artifact.operator, 'equal')
        self.assertEqual(artifact.vertex_type_system, 'ConstraintClause')
        self.assertEqual(artifact.value, '2')

    def test_greater_than(self):
        file = open('test_input/constrain_clause/greater_than.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        artifact = constraint_clause_parser(data)
        self.assertEqual(artifact.operator, 'greater_than')
        self.assertEqual(artifact.vertex_type_system, 'ConstraintClause')
        self.assertEqual(artifact.value, '1')
