import unittest

import yaml

from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import service_template_definition_parser


class TestServiceTemplate(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.template_definition_parser = service_template_definition_parser

    # Each test method starts with the keyword test_
    def test_notation(self):
        file = open('test_input/service_template/notation.yaml')
        data = file.read()
        file.close()
        data = yaml.safe_load(data)
        template = service_template_definition_parser('test_cluster', data)
        self.assertEqual(template.tosca_definitions_version, 1.3)
        self.assertEqual(template.name, 'test_cluster')
        self.assertEqual(template.vertex_type_system, 'ServiceTemplateDefinition')
        self.assertEqual(template.namespace, 'URI')
        self.assertEqual(len(template.metadata), 3)
        for index, metadata in enumerate(template.metadata):
            self.assertEqual(metadata.name, 'metadata_key_' + str(index))
            self.assertEqual(metadata.value, 'metadata_value_' + str(index))
        self.assertEqual(template.dsl_definitions, None)
        self.assertEqual(len(template.repositories), 2)
        for index, repositories in enumerate(template.repositories):
            self.assertEqual(repositories.name, 'test_repository_name_' + str(index))
        self.assertEqual(len(template.imports), 2)
        for index, imports in enumerate(template.imports):
            self.assertEqual(imports.file, 'URI_' + str(index))
        self.assertEqual(len(template.artifact_types), 2)
        for index, imports in enumerate(template.artifact_types):
            self.assertEqual(imports.name, 'test_artifact_type_name_' + str(index))
        self.assertEqual(len(template.data_types), 2)
        for index, imports in enumerate(template.data_types):
            self.assertEqual(imports.name, 'test_data_type_name_' + str(index))
        self.assertEqual(len(template.capability_types), 2)
        for index, imports in enumerate(template.capability_types):
            self.assertEqual(imports.name, 'test_capability_type_name_' + str(index))
        self.assertEqual(len(template.interface_types), 2)
        for index, imports in enumerate(template.interface_types):
            self.assertEqual(imports.name, 'test_interface_type_name_' + str(index))
        self.assertEqual(len(template.relationship_types), 2)
        for index, imports in enumerate(template.relationship_types):
            self.assertEqual(imports.name, 'test_relationship_type_name_' + str(index))
        self.assertEqual(len(template.node_types), 2)
        for index, imports in enumerate(template.node_types):
            self.assertEqual(imports.name, 'test_node_type_name_' + str(index))
        self.assertEqual(len(template.group_types), 2)
        for index, imports in enumerate(template.group_types):
            self.assertEqual(imports.name, 'test_group_type_name_' + str(index))
        self.assertEqual(len(template.policy_types), 2)
        for index, imports in enumerate(template.policy_types):
            self.assertEqual(imports.name, 'test_policy_type_name_' + str(index))
        self.assertEqual(template.topology_template.description, 'test_template_description')
