import unittest

import yaml

from parser.parser.tosca_v_1_3.assignments.PropertyAssignment import PropertyAssignment


class TestProperty(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.property_assignments = PropertyAssignment

    # Each test method starts with the keyword test_
    def test_set_value(self):
        file = open('test_input/property/TestProperty.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)

        for name, value in data.items():
            properties = self.property_assignments(name, value)
            self.assertEqual(properties.name, 'test_property_name')
            self.assertEqual(properties.value, 'property_value_test')
            self.assertEqual(properties.vertex_type_system, 'PropertyAssignment')

    def test_set_value_complex(self):
        file = open('test_input/property/TestPropertyComplex.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)

        for name, value in data.items():
            properties = self.property_assignments(name, value)
            self.assertEqual(properties.name, 'test_property_name')
            self.assertEqual(properties.value, {'get_input': 'test_value'})
            self.assertEqual(properties.vertex_type_system, 'PropertyAssignment')


if __name__ == '__main__':
    unittest.main()