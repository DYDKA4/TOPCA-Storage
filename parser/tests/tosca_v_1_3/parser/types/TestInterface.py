import unittest

import yaml

from parser.parser.tosca_v_1_3.types.InterfaceType import interface_type_parser


class TestInterface(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.interface_type_parser = interface_type_parser

    # Each test method starts with the keyword test_
    def test_data(self):
        file = open('test_input/interface_type/interface.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            interface = interface_type_parser(name, value)
            self.assertEqual(interface.vertex_type_system, 'InterfaceType')
            self.assertEqual(interface.name, 'test_interface_type_name')
            self.assertEqual(interface.derived_from, 'test_parent_interface_type_name')
            self.assertEqual(interface.version, 'test_version_number')
            for index, metadata in enumerate(interface.metadata):
                self.assertEqual(metadata.name, 'metadata_key_' + str(index))
                self.assertEqual(metadata.value, 'metadata_value_' + str(index))
            self.assertEqual(interface.description, 'test_interface_description')
            for index, inputs in enumerate(interface.inputs):
                self.assertEqual(inputs.type, 'test_property_name_' + str(index))
                self.assertEqual(inputs.name, 'test_property_name_' + str(index))
                self.assertEqual(inputs.description, 'test_property_description_' + str(index))
            for index, operations in enumerate(interface.operations):
                self.assertEqual(operations.name, 'operation_test_name_' + str(index))
                self.assertEqual(operations.implementation, 'implementation_artifact_test_name_' +
                                 str(index))
            for index, notification in enumerate(interface.notifications):
                self.assertEqual(notification.name, 'notification_test_name_' + str(index))
                self.assertEqual(notification.description, 'test_notification_description_' + str(index))
                self.assertEqual(notification.implementation.primary,
                                 'test_notification_implementation_' + str(index))
