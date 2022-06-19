import unittest

import yaml

from app.parser.tosca_v_1_3.types.PolicyTypes import policy_type_parser


class TestPolicy(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.policy_type_parser = policy_type_parser

    # Each test method starts with the keyword test_
    def test_policy(self):
        file = open('test_input/policy_type/policy.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            policy = policy_type_parser(name, value)
            self.assertEqual(policy.vertex_type_system, 'PolicyType')
            self.assertEqual(policy.name, 'test_policy_type_name')
            self.assertEqual(policy.derived_from, 'test_parent_policy_type_name')
            self.assertEqual(policy.version, 'test_version_number')
            for index, metadata in enumerate(policy.metadata):
                self.assertEqual(metadata.name, 'metadata_key_' + str(index))
                self.assertEqual(metadata.value, 'metadata_value_' + str(index))
            self.assertEqual(policy.description, 'test_policy_description')
            for index, properties in enumerate(policy.properties):
                self.assertEqual(properties.type, 'test_property_name_' + str(index))
                self.assertEqual(properties.name, 'test_property_name_' + str(index))
                self.assertEqual(properties.description, 'test_property_description_' + str(index))
            for index, targets in enumerate(policy.targets):
                self.assertEqual(targets, 'valid_target_type_' + str(index))
            self.assertNotEqual(policy.triggers, [])
            for index, trigger in enumerate(policy.triggers):
                self.assertEqual(trigger.name, 'test_trigger_name_' + str(index))
