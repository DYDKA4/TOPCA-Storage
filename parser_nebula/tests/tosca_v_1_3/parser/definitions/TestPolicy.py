import unittest

import yaml

from parser_nebula.parser.tosca_v_1_3.definitions.PolicyDefinition import policy_definition_parser


class TestPolicy(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.policy_definition_parser = policy_definition_parser

    # Each test method starts with the keyword test_
    def test_policy(self):
        file = open('test_input/policy/notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        policy = policy_definition_parser('test_policy_name', data.get('test_policy_name'))
        self.assertEqual(policy.name, 'test_policy_name')
        self.assertEqual(policy.vertex_type_system, 'PolicyDefinition')
        self.assertEqual(policy.type, 'test_policy_type_name')
        self.assertEqual(policy.description, 'test_policy_description')
        self.assertNotEqual(policy.metadata, [])
        for index, metadata in enumerate(policy.metadata):
            self.assertEqual(metadata.name, 'metadata_key_' + str(index))
            self.assertEqual(metadata.value, 'metadata_value_' + str(index))
        self.assertNotEqual(policy.properties, [])
        for index, properties in enumerate(policy.properties):
            self.assertEqual(properties.name, 'test_property_name_' + str(index))
            self.assertEqual(properties.value, 'property_value_test_' + str(index))
        self.assertNotEqual(policy.targets, [])
        for index, target in enumerate(policy.targets):
            self.assertEqual(target, 'policy_target_' + str(index))
        self.assertNotEqual(policy.triggers, [])
        for index, trigger in enumerate(policy.triggers):
            self.assertEqual(trigger.name, 'test_trigger_name_' + str(index))
