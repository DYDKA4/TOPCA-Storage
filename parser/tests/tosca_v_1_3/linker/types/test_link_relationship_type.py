import unittest

from parser.linker.tosca_v_1_3.types.GroupType import link_group_type
from parser.linker.tosca_v_1_3.types.PolicyTypes import link_policy_type
from parser.linker.tosca_v_1_3.types.RelationshipType import link_relationship_type
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.GroupType import GroupType
from parser.parser.tosca_v_1_3.types.NodeType import NodeType
from parser.parser.tosca_v_1_3.types.PolicyTypes import PolicyType
from parser.parser.tosca_v_1_3.types.RelationshipType import RelationshipType


class TestRelationshipType(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.relationship_types.append(RelationshipType('relationship_type_parent'))
        self.relationship = RelationshipType('relationship_type')
        self.service_template.capability_types.append(NodeType('capability_type_1'))
        self.service_template.capability_types.append(NodeType('capability_type_2'))
        self.service_template.relationship_types.append(self.relationship)

    def test_link_derived_from(self):
        self.relationship.derived_from = 'relationship_type_parent'
        link_relationship_type(self.service_template, self.relationship)
        self.assertEqual(self.service_template.relationship_types[0], self.relationship.derived_from.get('derived_from')[1])

    def test_link_members(self):
        self.relationship.valid_target_types = ['capability_type_1', 'capability_type_2']
        link_relationship_type(self.service_template, self.relationship)
        self.assertListEqual(self.service_template.capability_types,
                             self.relationship.valid_target_types.get('valid_target_types')[1])


if __name__ == '__main__':
    unittest.main()
