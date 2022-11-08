import unittest

from parser_nebula.linker.tosca_v_1_3.definitions.OperationDefinition import link_operation_definition
from parser_nebula.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition

from parser_nebula.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.NodeType import NodeType


class TestOperationDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.node_type = (NodeType('interface_type'))
        self.interface = InterfaceDefinition('interface_definition')
        self.operation_definition = OperationDefinition('operation_definition')
        self.primary = ArtifactDefinition('artifact_definition_in_interface')
        self.implementation_definition = OperationImplementationDefinition()
        self.implementation_definition.primary = self.primary
        self.operation_definition.implementation = self.implementation_definition
        self.interface.operations.append(self.operation_definition)
        self.node_type.artifacts.append(ArtifactDefinition('artifact_definition_in_node'))
        self.node_type.interfaces.append(self.interface)
        self.operation = OperationDefinition('operation')
        self.service_template.node_types.append(self.node_type)

    def test_link_artifact_definition_in_node(self):
        self.operation.implementation = 'artifact_definition_in_node'
        link_operation_definition(self.service_template, self.operation)
        self.assertEqual(self.node_type.artifacts[0], self.operation.implementation.get('implementation')[1])

    def test_link_artifact_definition_in_interface(self):
        self.operation.implementation = 'artifact_definition_in_interface'
        link_operation_definition(self.service_template, self.operation)
        self.assertEqual(self.primary, self.operation.implementation.get('implementation')[1])

    def test_blank_implementation(self):
        implementation = OperationImplementationDefinition()
        self.operation.implementation = implementation
        link_operation_definition(self.service_template, self.operation)
        self.assertEqual(implementation, self.operation.implementation)


if __name__ == '__main__':
    unittest.main()
