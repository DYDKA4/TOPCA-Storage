import unittest

from parser_nebula.linker.tosca_v_1_3.definitions.GroupDefinition import link_group_definition
from parser_nebula.parser.tosca_v_1_3.definitions.GroupDefinition import GroupDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser_nebula.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser_nebula.parser.tosca_v_1_3.types.GroupType import GroupType
from parser_nebula.parser.tosca_v_1_3.types.NodeType import NodeType


class TestGroupDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.group_types.append(GroupType('group_type'))
        self.template_definition = TemplateDefinition()
        self.template_definition.node_templates.append(NodeTemplate('node_template_0'))
        self.template_definition.node_templates.append(NodeTemplate('node_template_1'))
        self.service_template.topology_template = self.template_definition
        self.group = GroupDefinition('group_definition')

    def test_link_group_type(self):
        self.group.type = 'group_type'
        link_group_definition(self.service_template, self.group)
        self.assertEqual(self.service_template.group_types[0], self.group.type.get('type')[1])

    def test_link_group_members(self):
        self.group.type = 'group_type'
        self.group.members = ['node_template_0', 'node_template_1']
        link_group_definition(self.service_template, self.group)
        self.assertEqual(self.service_template.group_types[0], self.group.type.get('type')[1])
        self.assertListEqual(self.template_definition.node_templates, self.group.members.get('members')[1])
if __name__ == '__main__':
    unittest.main()
