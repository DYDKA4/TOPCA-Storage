import unittest

import yaml

from parser.parser.tosca_v_1_3.definitions.WorkflowStepDefinition import workflow_step_definition_parser


class TestWorkflowStep(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.workflow_step_definition_parser = workflow_step_definition_parser

    # Each test method starts with the keyword test_
    def test_template(self):
        file = open('test_input/workflow_step/notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            workflow_step = workflow_step_definition_parser(name, value)
            self.assertEqual(workflow_step.vertex_type_system, 'WorkflowStepDefinition')
            self.assertEqual(workflow_step.name, 'test_step_name')
            self.assertEqual(workflow_step.target, 'test_target_name')
            self.assertEqual(workflow_step.target_relationship, 'test_target_requirement_name')
            self.assertEqual(workflow_step.operation_host, 'test_operation_host_name')
            workflow_step_condition = workflow_step.filter[0]
            self.assertNotEqual(workflow_step_condition, [])
            self.assertNotEqual(workflow_step.activities, [])
            self.assertNotEqual(workflow_step.on_success, [])
            for index, on_success in enumerate(workflow_step.on_success):
                self.assertEqual(on_success, 'on_success_step_name_' + str(index))
            self.assertNotEqual(workflow_step.on_failure, [])
            for index, on_failure in enumerate(workflow_step.on_failure):
                self.assertEqual(on_failure, 'on_failure_step_name_' + str(index))
