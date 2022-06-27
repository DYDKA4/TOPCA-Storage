import unittest

from parser.linker.tosca_v_1_3.definitions.PolicyDefinition import link_policy_definition
from parser.parser.tosca_v_1_3.definitions.GroupDefinition import GroupDefinition
from parser.parser.tosca_v_1_3.definitions.PolicyDefinition import PolicyDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser.parser.tosca_v_1_3.types.PolicyTypes import PolicyType


class TestPolicyDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.policy_types.append(PolicyType('policy_type'))
        self.policy = PolicyDefinition('policy_definition')
        self.topology_template = TemplateDefinition()
        self.group = GroupDefinition('group_name')
        self.topology_template.groups.append(self.group)
        self.node_template = NodeTemplate('node_template')
        self.topology_template.node_templates.append(self.node_template)
        self.service_template.topology_template = self.topology_template

    def test_link_policy_type(self):
        self.policy.type = 'policy_type'
        link_policy_definition(self.service_template, self.policy)
        self.assertEqual(self.service_template.policy_types[0], self.policy.type.get('type')[1])

    def test_link_policy_type_and_targets(self):
        self.policy.type = 'policy_type'
        self.policy.targets = ['group_name', 'node_template']
        link_policy_definition(self.service_template, self.policy)
        self.assertEqual(self.service_template.policy_types[0], self.policy.type.get('type')[1])
        self.assertListEqual([self.group, self.node_template], self.policy.targets.get('targets')[1])



if __name__ == '__main__':
    unittest.main()
