import unittest

import yaml

from app.parser.tosca_v_1_3.definitions.ImperativeWorkflowDefinition import imperative_workflow_definition_parser


class TestImperativeWorkflow(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.imperative_workflow_definition_parser = imperative_workflow_definition_parser

    # Each test method starts with the keyword test_
    def test_template(self):
        file = open('test_input/imperative_workflow/notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        for name, value in data.items():
            workflow = imperative_workflow_definition_parser(name, value)
            self.assertEqual(workflow.vertex_type_system, 'ImperativeWorkflowDefinition')
            self.assertEqual(workflow.description, 'test_workflow_description')
            self.vertex_type_system = 'ImperativeWorkflowDefinition'
            self.assertNotEqual(workflow.metadata, [])
            for index, metadata in enumerate(workflow.metadata):
                self.assertEqual(metadata.name, 'metadata_key_' + str(index))
                self.assertEqual(metadata.value, 'metadata_value_' + str(index))
            self.assertNotEqual(workflow.inputs, [])
            for index, inputs in enumerate(workflow.inputs):
                self.assertEqual(inputs.name, 'test_property_name_' + str(index))
                self.assertEqual(inputs.type, 'test_property_name_' + str(index))
                self.assertEqual(inputs.description, 'test_property_description_' + str(index))
            self.assertNotEqual(workflow.preconditions, [])
            for index, predictions in enumerate(workflow.preconditions):
                self.assertEqual(predictions.target, 'test_target_name_' + str(index))
                self.assertEqual(predictions.target_relationship, 'test_target_requirement_name_' + str(index))
            self.assertNotEqual(workflow.steps, [])
            for index, step in enumerate(workflow.steps):
                self.assertEqual(step.name, 'test_step_name_' + str(index))
            self.assertEqual(workflow.implementation.primary_artifact_name, 'test_primary_artifact_name')
            self.assertEqual(workflow.outputs, 'test_attribute_mappings')
