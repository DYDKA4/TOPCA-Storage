import unittest

import yaml

from app.parser.tosca_v_1_3.others.Metadata import Metadata


class TestMetadata(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.Metadata = Metadata

    # Each test method starts with the keyword test_
    def test_directives(self):
        directive = Metadata('test_name', 'test_value')
        self.assertEqual(directive.name, 'test_name')
        self.assertEqual(directive.value, 'test_value')
        self.assertEqual(directive.vertex_type_system, 'Metadata')
        