import unittest

from parser.linker.tosca_v_1_3.definitions.NotificationImplementationDefinition import \
    link_notification_implementation_definition
from parser.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition
from parser.parser.tosca_v_1_3.definitions.NotificationImplementationDefinition import \
    NotificationImplementationDefinition
from parser.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition
from parser.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.NodeType import NodeType


class TestNotificationImplementationDefinition(unittest.TestCase):
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
        self.notification_implementation = NotificationImplementationDefinition()
        self.service_template.node_types.append(self.node_type)

    def test_link_artifact_definition_in_node(self):
        self.notification_implementation.primary = 'artifact_definition_in_node'
        link_notification_implementation_definition(self.service_template, self.notification_implementation)
        self.assertEqual(self.node_type.artifacts[0], self.notification_implementation.primary.get('primary')[1])

    def test_link_artifact_definition_in_interface(self):
        self.notification_implementation.primary = 'artifact_definition_in_interface'
        link_notification_implementation_definition(self.service_template, self.notification_implementation)
        self.assertEqual(self.primary, self.notification_implementation.primary.get('primary')[1])

    def test_link_artifact_definition_in_interface_with_dependencies(self):
        self.notification_implementation.primary = 'artifact_definition_in_interface'
        self.notification_implementation.dependencies = ['artifact_definition_in_interface',
                                                         'artifact_definition_in_node']
        link_notification_implementation_definition(self.service_template, self.notification_implementation)
        self.assertEqual(self.primary, self.notification_implementation.primary.get('primary')[1])
        self.assertListEqual([self.node_type.artifacts[0],self.primary],
                             self.notification_implementation.dependencies.get('dependencies')[1])

if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
