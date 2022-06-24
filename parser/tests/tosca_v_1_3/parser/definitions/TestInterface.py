import unittest

import yaml

from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import interface_definition_parser


class TestInterface(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.interface_definition_parser = interface_definition_parser

    # Each test method starts with the keyword test_
    def test_notation_for_type(self):
        file = open('test_input/interface/notation_for_type.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            interface = interface_definition_parser(name, value)
            self.assertEqual(interface.name, 'test_interface_definition_name')
            self.assertEqual(interface.type, 'test_interface_type')
            self.assertEqual(interface.vertex_type_system, 'InterfaceDefinition')
            for index, inputs in enumerate(interface.inputs_definition):
                self.assertEqual(inputs.type, 'test_property_name_' + str(index))
                self.assertEqual(inputs.name, 'test_property_name_' + str(index))
                self.assertEqual(inputs.description, 'test_property_description_' + str(index))
            self.assertEqual(interface.inputs_assignments, [])
            for index, operation in enumerate(interface.operations):
                self.assertEqual(operation.name, 'operation_test_name_' + str(index))
            for index, notification in enumerate(interface.notifications):
                self.assertEqual(notification.name, 'notification_test_name_' + str(index))


    def test_notation_for_template(self):
        file = open('test_input/interface/notation_for_template.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            interface = interface_definition_parser(name, value)
            self.assertEqual(interface.name, 'test_interface_definition_name')
            self.assertIsNone(interface.type)
            self.assertEqual(interface.vertex_type_system, 'InterfaceDefinition')
            self.assertEqual(interface.inputs_definition, [])
            for index, inputs in enumerate(interface.inputs_assignments):
                self.assertEqual(inputs.name, 'test_property_name_' + str(index))
                self.assertEqual(inputs.value, 'property_value_test_' + str(index))
            for index, operation in enumerate(interface.operations):
                self.assertEqual(operation.name, 'operation_test_name_' + str(index))
            for index, notification in enumerate(interface.notifications):
                self.assertEqual(notification.name, 'notification_test_name_' + str(index))
