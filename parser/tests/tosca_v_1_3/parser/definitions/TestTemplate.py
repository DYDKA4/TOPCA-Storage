import unittest

import yaml

from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import template_definition_parser


class TestTemplate(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.template_definition_parser = template_definition_parser

    # Each test method starts with the keyword test_
    def test_notation(self):
        file = open('test_input/template/notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        template = template_definition_parser(data)
        self.assertEqual(template.vertex_type_system, 'TopologyTemplateDefinition')
        self.assertEqual(template.description, 'test_template_description')
        self.assertNotEqual(template.inputs, [])
        for index, inputs in enumerate(template.inputs):
            self.assertEqual(inputs.name, 'input_' + str(index))
        self.assertNotEqual(template.outputs, [])
        for index, outputs in enumerate(template.outputs):
            self.assertEqual(outputs.name, 'output_' + str(index))
        self.assertNotEqual(template.node_templates, [])
        for index, node_templates in enumerate(template.node_templates):
            self.assertEqual(node_templates.name, 'test_node_template_name_' + str(index))
        self.assertNotEqual(template.node_templates, [])
        for index, relationship_templates in enumerate(template.relationship_templates):
            self.assertEqual(relationship_templates.name, 'test_relationship_template_name_' + str(index))
        self.assertNotEqual(template.groups, [])
        for index, groups in enumerate(template.groups):
            self.assertEqual(groups.name, 'test_group_name_' + str(index))
        self.assertNotEqual(template.policies, [])
        for index, policies in enumerate(template.policies):
            self.assertEqual(policies.name, 'test_policy_name_' + str(index))
        self.assertNotEqual(template.workflows, [])
        for index, workflows in enumerate(template.workflows):
            self.assertEqual(workflows.name, 'test_workflow_name_' + str(index))
        self.assertEqual(template.substitution_mappings, 'test_substitution_mappings')
