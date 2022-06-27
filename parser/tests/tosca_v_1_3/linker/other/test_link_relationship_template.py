import unittest

from parser.linker.tosca_v_1_3.others.RelationshipTemplate import link_relationship_template
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate
from parser.parser.tosca_v_1_3.types.CapabilityType import CapabilityType


class TestRelationshipTemplate(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.capability_types.append(CapabilityType('capability_type'))
        self.topology_template = TemplateDefinition()
        self.topology_template.relationship_templates.append(RelationshipTemplate('to_copy'))
        self.service_template.topology_template = self.topology_template
        self.relationship_template = RelationshipTemplate('node_template')

    def test_link_copy_relationship(self):
        self.relationship_template.copy = 'to_copy'
        link_relationship_template(self.service_template, self.relationship_template)
        self.assertEqual(self.topology_template.relationship_templates[0],
                         self.relationship_template.copy.get('copy')[1])


if __name__ == '__main__':
    unittest.main()
