import unittest

from parser.linker.tosca_v_1_3.types.GroupType import link_group_type
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.GroupType import GroupType
from parser.parser.tosca_v_1_3.types.NodeType import NodeType


class TestGroupType(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.group_types.append(GroupType('capability_type_parent'))
        self.group = GroupType('capability_type')
        self.service_template.node_types.append(NodeType('node_type_1'))
        self.service_template.node_types.append(NodeType('node_type_2'))
        self.service_template.group_types.append(self.group)

    def test_link_derived_from(self):
        self.group.derived_from = 'capability_type_parent'
        link_group_type(self.service_template, self.group)
        self.assertEqual(self.service_template.group_types[0], self.group.derived_from.get('derived_from')[1])

    def test_link_members(self):
        self.group.members = ['node_type_1', 'node_type_2']
        link_group_type(self.service_template, self.group)
        self.assertListEqual(self.service_template.node_types,
                             self.group.members.get('members')[1])


if __name__ == '__main__':
    unittest.main()
