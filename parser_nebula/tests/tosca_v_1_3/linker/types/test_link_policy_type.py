import unittest

from parser_nebula.linker.tosca_v_1_3.types.PolicyTypes import link_policy_type
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.NodeType import NodeType
from parser_nebula.parser.tosca_v_1_3.types.PolicyTypes import PolicyType


class TestPolicyType(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.policy_types.append(PolicyType('policy_type_parent'))
        self.policy = PolicyType('policy_type')
        self.service_template.node_types.append(NodeType('node_type_1'))
        self.service_template.node_types.append(NodeType('node_type_2'))
        self.service_template.policy_types.append(self.policy)

    def test_link_derived_from(self):
        self.policy.derived_from = 'policy_type_parent'
        link_policy_type(self.service_template, self.policy)
        self.assertEqual(self.service_template.policy_types[0], self.policy.derived_from.get('derived_from')[1])

    def test_link_members(self):
        self.policy.targets = ['node_type_1', 'node_type_2']
        link_policy_type(self.service_template, self.policy)
        self.assertListEqual(self.service_template.node_types,
                             self.policy.targets.get('targets')[1])


if __name__ == '__main__':
    unittest.main()
