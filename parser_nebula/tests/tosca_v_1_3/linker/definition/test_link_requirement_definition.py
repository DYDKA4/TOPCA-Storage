import unittest

from parser_nebula.linker.tosca_v_1_3.definitions.RequirementDefinition import link_requirement_definition
from parser_nebula.parser.tosca_v_1_3.definitions.RequirementDefinition import RequirementDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.CapabilityType import CapabilityType
from parser_nebula.parser.tosca_v_1_3.types.NodeType import NodeType
from parser_nebula.parser.tosca_v_1_3.types.RelationshipType import RelationshipType


class TestRequirementDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.capability_types.append(CapabilityType('capability_type'))
        self.service_template.node_types.append(NodeType('node_type'))
        self.service_template.relationship_types.append(RelationshipType('relationship_type'))
        self.requirement = RequirementDefinition('parameter_definition')

    def test_link_capability_type(self):
        self.requirement.capability = 'capability_type'
        link_requirement_definition(self.service_template, self.requirement)
        self.assertEqual(self.service_template.capability_types[0], self.requirement.capability.get('capability')[1])

    def test_link_relationship_type(self):
        self.requirement.relationship = 'relationship_type'
        link_requirement_definition(self.service_template, self.requirement)
        self.assertEqual(self.service_template.relationship_types[0],
                         self.requirement.relationship.get('relationship')[1])

    def test_link_node_type(self):
        self.requirement.node = 'node_type'
        link_requirement_definition(self.service_template, self.requirement)
        self.assertEqual(self.service_template.node_types[0],
                         self.requirement.node.get('node')[1])


if __name__ == '__main__':
    unittest.main()
