import unittest

from parser_nebula.linker.tosca_v_1_3.assignments.RequirementAssignment import link_requirement_assignments
from parser_nebula.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment
from parser_nebula.parser.tosca_v_1_3.definitions.CapabilityDefinition import CapabilityDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser_nebula.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser_nebula.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate
from parser_nebula.parser.tosca_v_1_3.types.CapabilityType import CapabilityType
from parser_nebula.parser.tosca_v_1_3.types.NodeType import NodeType
from parser_nebula.parser.tosca_v_1_3.types.RelationshipType import RelationshipType


class TestRequirementAssignment(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_template')
        self.service_template.node_types.append(NodeType('test_node_type'))
        self.service_template.relationship_types.append(RelationshipType('relationship_type'))
        self.requirement = RequirementAssignment('test_requirement')
        self.service_template.topology_template = TemplateDefinition()
        self.service_template.topology_template.node_templates.append(NodeTemplate('test_node_template'))
        self.service_template.topology_template.relationship_templates.append(
            RelationshipTemplate('RelationshipTemplate')
        )
        self.relationship_template = self.service_template.topology_template.relationship_templates
        self.node_template = self.service_template.topology_template.node_templates

    def test_link_node_type_requirement_(self):
        self.requirement.node = 'test_node_type'
        link_requirement_assignments(self.service_template, self.requirement)
        self.assertEqual(self.service_template.node_types[0], self.requirement.node.get('node')[1])

    def test_link_node_template_requirement_(self):
        self.requirement.node = 'test_node_template'
        link_requirement_assignments(self.service_template, self.requirement)
        self.assertEqual(self.node_template[0], self.requirement.node.get('node')[1])

    def test_link_relationship_template_requirement(self):
        self.requirement.relationship = 'RelationshipTemplate'
        link_requirement_assignments(self.service_template, self.requirement)
        self.assertEqual(self.relationship_template[0], self.requirement.relationship.get('relationship')[1])

    def test_link_relationship_type_requirement(self):
        self.requirement.relationship = 'relationship_type'
        link_requirement_assignments(self.service_template, self.requirement)
        self.assertEqual(self.service_template.relationship_types[0],
                         self.requirement.relationship.get('relationship')[1])

    def test_link_capability_node_type_requirement(self):
        self.service_template.node_types[0].capabilities.append(CapabilityDefinition('capability_node_type'))
        self.requirement.capability = 'capability_node_type'
        link_requirement_assignments(self.service_template, self.requirement)
        self.assertEqual(self.service_template.node_types[0].capabilities[0],
                         self.requirement.capability.get('capability')[1])

    def test_link_capability_type_requirement(self):
        self.service_template.capability_types.append(CapabilityType('capability_type'))
        self.requirement.capability = 'capability_type'
        link_requirement_assignments(self.service_template, self.requirement)
        self.assertEqual(self.service_template.capability_types[0],
                         self.requirement.capability.get('capability')[1])

if __name__ == '__main__':
    unittest.main()
