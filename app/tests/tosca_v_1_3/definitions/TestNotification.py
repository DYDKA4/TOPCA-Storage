import unittest

import yaml

from app.parser.tosca_v_1_3.definitions.NotificationDefinition import notification_definition_parser


class TestNotification(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.notification_definition_parser = notification_definition_parser

    # Each test method starts with the keyword test_
    def test_single_artifact(self):
        file = open('test_input/notification/notification_without_outputs.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        notification = notification_definition_parser('notification_test_name', data.get('notification_test_name'))
        self.assertEqual(notification.vertex_type_system, 'NotificationDefinition')
        self.assertEqual(notification.description, 'test_notification_description')
        self.assertEqual(notification.implementation.primary_artifact_name, 'test_notification_implementation')
