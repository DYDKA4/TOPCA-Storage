import unittest

import yaml

from parser.parser.tosca_v_1_3.definitions.WorkflowPreconditionDefinition import workflow_precondition_definition_parser


class TestWorkflowPrecondition(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.workflow_precondition_definition_parser = workflow_precondition_definition_parser

    # Each test method starts with the keyword test_
    def test_template(self):
        file = open('test_input/workflow_prediction/notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        workflow_prediction = workflow_precondition_definition_parser(data)
        self.assertEqual(workflow_prediction.vertex_type_system, 'WorkflowPredictionDefinition')
        self.assertEqual(workflow_prediction.target, 'test_target_name')
        self.assertEqual(workflow_prediction.target_relationship, 'test_target_requirement_name')
        workflow_prediction_condition = workflow_prediction.conditions[0]
        self.assertNotEqual(workflow_prediction_condition, [])
        for assert_value in workflow_prediction_condition.operands.get('assert')[0].values():
            self.assertEqual(assert_value[0].value, 'my_value')
