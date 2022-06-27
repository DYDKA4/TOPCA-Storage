import unittest

from parser.linker.tosca_v_1_3.others.NodeTemplate import link_node_template
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser.parser.tosca_v_1_3.types.CapabilityType import CapabilityType


class TestNodeTemplate(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.capability_types.append(CapabilityType('capability_type'))
        self.topology_template = TemplateDefinition()
        self.topology_template.node_templates.append(NodeTemplate('to_copy'))
        self.service_template.topology_template = self.topology_template
        self.node_template = NodeTemplate('node_template')

    def test_link_copy_node(self):
        self.node_template.copy = 'to_copy'
        link_node_template(self.service_template, self.node_template)
        self.assertEqual(self.topology_template.node_templates[0], self.node_template.copy.get('copy')[1])


if __name__ == '__main__':
    unittest.main()
