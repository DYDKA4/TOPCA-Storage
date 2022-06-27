import unittest

from parser.linker.tosca_v_1_3.definitions.WorkflowStepDefinition import link_workflow_step_definition
from parser.parser.tosca_v_1_3.definitions.GroupDefinition import GroupDefinition
from parser.parser.tosca_v_1_3.definitions.ImperativeWorkflowDefinition import ImperativeWorkflowDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.definitions.WorkflowStepDefinition import WorkflowStepDefinition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate


class TestWorkflowStepDefinition(unittest.TestCase):
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
        self.workflow_step_on_success = WorkflowStepDefinition('on_success')
        self.workflow_step_on_failure = WorkflowStepDefinition('on_failure')
        self.workflow_definition = ImperativeWorkflowDefinition('workflow_definition')
        self.workflow_definition.steps.append(self.workflow_step_on_success)
        self.workflow_definition.steps.append(self.workflow_step_on_failure)
        self.service_template.topology_template.workflows.append(self.workflow_definition)
        self.workflow = WorkflowStepDefinition('workflow')

    def test_link_template_target(self):
        self.workflow.target = 'node_template'
        link_workflow_step_definition(self.service_template, self.workflow)
        self.assertEqual(self.node_template, self.workflow.target.get('target')[1])

    def test_link_group_target(self):
        self.workflow.target = 'group_definition'
        link_workflow_step_definition(self.service_template, self.workflow)
        self.assertEqual(self.group_definition, self.workflow.target.get('target')[1])

    def test_link_target_relationship(self):
        self.workflow.target_relationship = 'relationship_template'
        link_workflow_step_definition(self.service_template, self.workflow)
        self.assertEqual(self.target_relationship, self.workflow.target_relationship.get('target_relationship')[1])

    def test_link_on_success(self):
        self.workflow.on_success = ['on_success']
        link_workflow_step_definition(self.service_template, self.workflow)
        self.assertListEqual([self.workflow_step_on_success],
                             self.workflow.on_success.get('on_success')[1])

    def test_link_on_failure(self):
        self.workflow.on_failure = ['on_failure']
        link_workflow_step_definition(self.service_template, self.workflow)
        self.assertListEqual([self.workflow_step_on_failure],
                             self.workflow.on_failure.get('on_failure')[1])

if __name__ == '__main__':
    unittest.main()
