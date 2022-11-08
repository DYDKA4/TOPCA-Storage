import unittest

from parser_nebula.linker.tosca_v_1_3.definitions.WorkflowPreconditionDefinition import link_workflow_precondition_definition
from parser_nebula.parser.tosca_v_1_3.definitions.GroupDefinition import GroupDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.WorkflowPreconditionDefinition import WorkflowPreconditionDefinition
from parser_nebula.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser_nebula.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate


class TestWorkflowPreconditionDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.node_template = NodeTemplate('node_template')
        self.target_relationship = RelationshipTemplate('relationship_template')
        self.group_definition = GroupDefinition('group_definition')
        self.topology_template = TemplateDefinition()
        self.topology_template.node_templates.append(self.node_template)
        self.topology_template.groups.append(self.group_definition)
        self.topology_template.relationship_templates.append(self.target_relationship)
        self.service_template.topology_template = self.topology_template
        self.workflow = WorkflowPreconditionDefinition()

    def test_link_template_target(self):
        self.workflow.target = 'node_template'
        link_workflow_precondition_definition(self.service_template, self.workflow)
        self.assertEqual(self.node_template, self.workflow.target.get('target')[1])

    def test_link_group_target(self):
        self.workflow.target = 'group_definition'
        link_workflow_precondition_definition(self.service_template, self.workflow)
        self.assertEqual(self.group_definition, self.workflow.target.get('target')[1])

    def test_link_target_relationship(self):
        self.workflow.target_relationship = 'relationship_template'
        link_workflow_precondition_definition(self.service_template, self.workflow)
        self.assertEqual(self.target_relationship, self.workflow.target_relationship.get('target_relationship')[1])


if __name__ == '__main__':
    unittest.main()
