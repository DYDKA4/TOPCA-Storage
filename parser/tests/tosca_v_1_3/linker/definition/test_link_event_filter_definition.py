import unittest

from parser.linker.tosca_v_1_3.definitions.EventFilterDefinition import link_event_filter_definition
from parser.parser.tosca_v_1_3.assignments.CapabilityAssignment import CapabilityAssignment
from parser.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment
from parser.parser.tosca_v_1_3.definitions.CapabilityDefinition import CapabilityDefinition
from parser.parser.tosca_v_1_3.definitions.EventFilterDefinition import EventFilterDefinition
from parser.parser.tosca_v_1_3.definitions.RequirementDefinition import RequirementDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser.parser.tosca_v_1_3.types.DataType import DataType
from parser.parser.tosca_v_1_3.types.NodeType import NodeType


class TestEventFilterDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.node_types.append(NodeType('node_type'))
        self.service_template.node_types[0].requirements.append(RequirementDefinition('requirement_definition'))
        self.service_template.node_types[0].capabilities.append(CapabilityDefinition('capability_definition'))
        self.service_template.topology_template = TemplateDefinition()
        self.service_template.topology_template.node_templates.append(NodeTemplate('node_template'))
        self.node_template = self.service_template.topology_template.node_templates
        self.node_template[0].capabilities.append(CapabilityAssignment('capability_assignment'))
        self.node_template[0].requirements.append(RequirementAssignment('requirement_assignment'))
        self.service_template.data_types.append(DataType('data_type'))

    def test_link_node_type_event_filter(self):
        event_filter = EventFilterDefinition('node_type')
        link_event_filter_definition(self.service_template, event_filter)
        self.assertEqual(self.service_template.node_types[0], event_filter.node.get('node')[1])

    def test_link_node_template_event_filter(self):
        event_filter = EventFilterDefinition('node_template')
        link_event_filter_definition(self.service_template, event_filter)
        self.assertEqual(self.node_template[0], event_filter.node.get('node')[1])

    def test_link_requirement_type_event_filter(self):
        event_filter = EventFilterDefinition('node_type', 'requirement_definition')
        link_event_filter_definition(self.service_template, event_filter)
        self.assertEqual(self.service_template.node_types[0], event_filter.node.get('node')[1])
        self.assertEqual(self.service_template.node_types[0].requirements[0],
                         event_filter.requirement.get('requirement')[1])

    def test_link_capability_type_event_filter(self):
        event_filter = EventFilterDefinition('node_type', capability='capability_definition')
        link_event_filter_definition(self.service_template, event_filter)
        self.assertEqual(self.service_template.node_types[0], event_filter.node.get('node')[1])
        self.assertEqual(self.service_template.node_types[0].capabilities[0],
                         event_filter.capability.get('capability')[1])

    def test_link_requirement_template_event_filter(self):
        event_filter = EventFilterDefinition('node_template', 'requirement_assignment')
        link_event_filter_definition(self.service_template, event_filter)
        self.assertEqual(self.node_template[0], event_filter.node.get('node')[1])
        self.assertEqual(self.node_template[0].requirements[0],
                         event_filter.requirement.get('requirement')[1])

    def test_link_capability_template_event_filter(self):
        event_filter = EventFilterDefinition('node_template', capability='capability_assignment')
        link_event_filter_definition(self.service_template, event_filter)
        self.assertEqual(self.node_template[0], event_filter.node.get('node')[1])
        self.assertEqual(self.node_template[0].capabilities[0],
                         event_filter.capability.get('capability')[1])

if __name__ == '__main__':
    unittest.main()
