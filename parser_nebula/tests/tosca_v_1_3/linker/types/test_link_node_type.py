import unittest

from parser_nebula.linker.tosca_v_1_3.types.NodeType import link_node_type
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.NodeType import NodeType


class TestNodeType(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.node_types.append(NodeType('interface_type_parent'))
        self.node = NodeType('interface_type')
        self.service_template.node_types.append(self.node)

    def test_link_derived_from(self):
        self.node.derived_from = 'interface_type_parent'
        link_node_type(self.service_template, self.node)
        self.assertEqual(self.service_template.node_types[0], self.node.derived_from.get('derived_from')[1])


if __name__ == '__main__':
    unittest.main()
