import unittest

import yaml

from app.parser.tosca_v_1_3.others.Directives import Directives


class TestDirectives(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.Directives = Directives

    # Each test method starts with the keyword test_
    def test_directives(self):
        directive = Directives('test_value')
        self.assertEqual(directive.value, 'test_value')
        self.assertEqual(directive.vertex_type_system, 'Directives')
