from parser_nebula.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment
from parser_nebula.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.NotificationDefinition import NotificationDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.NotificationImplementationDefinition import \
    NotificationImplementationDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.RequirementDefinition import RequirementDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser_nebula.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser_nebula.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate
from parser_nebula.parser.tosca_v_1_3.types.InterfaceType import InterfaceType
from parser_nebula.parser.tosca_v_1_3.types.NodeType import NodeType
from parser_nebula.parser.tosca_v_1_3.types.RelationshipType import RelationshipType


def add_artifact_from_operation_definition_artifact(interface, artifact_definition_array: list):
    for operation_definition in interface.operations:
        operation_definition: OperationDefinition
        if type(operation_definition.implementation) not in {str, dict}:
            operation_definition_implementation: OperationImplementationDefinition = \
                operation_definition.implementation
            if type(operation_definition_implementation.primary) not in {str, dict}:
                artifact: ArtifactDefinition = operation_definition_implementation.primary
                artifact_definition_array.append(artifact)
                artifact_definition_array += operation_definition_implementation.dependencies


def add_artifact_from_notification_definition_artifact(interface, artifact_definition_array: list):
    for notification_definition in interface.notifications:
        notification_definition: NotificationDefinition
        notification_definition_implementation: OperationImplementationDefinition \
            = notification_definition.implementation
        if type(notification_definition_implementation.primary) not in {str, dict}:
            artifact: ArtifactDefinition = notification_definition_implementation.primary
            artifact_definition_array.append(artifact)
            artifact_definition_array += notification_definition_implementation.dependencies


def get_all_artifact_definition(service_template: ServiceTemplateDefinition) -> list:
    # todo Maybe errors?
    artifact_definition_array = []
    for node_type in service_template.node_types:
        node_type: NodeType
        artifact_definition_array += node_type.artifacts
        for interface in node_type.interfaces:
            interface: InterfaceDefinition
            add_artifact_from_notification_definition_artifact(interface, artifact_definition_array)
            add_artifact_from_operation_definition_artifact(interface,artifact_definition_array)
        for requirement_definition in node_type.requirements:
            requirement_definition: RequirementDefinition
            for interface in requirement_definition.interfaces:
                interface: InterfaceDefinition
                add_artifact_from_operation_definition_artifact(interface, artifact_definition_array)
                add_artifact_from_notification_definition_artifact(interface, artifact_definition_array)
    for interface in service_template.interface_types:
        interface: InterfaceType
        add_artifact_from_operation_definition_artifact(interface, artifact_definition_array)
        add_artifact_from_notification_definition_artifact(interface, artifact_definition_array)

    for relationship_type in service_template.relationship_types:
        relationship_type: RelationshipType
        for interface in relationship_type.interfaces:
            interface: InterfaceDefinition
            add_artifact_from_operation_definition_artifact(interface,artifact_definition_array)
            add_artifact_from_notification_definition_artifact(interface, artifact_definition_array)

    topology_template: TemplateDefinition = service_template.topology_template
    if topology_template:
        for node_template in topology_template.node_templates:
            node_template: NodeTemplate
            artifact_definition_array += node_template.artifacts
            for interface in node_template.interfaces:
                interface: InterfaceDefinition
                add_artifact_from_notification_definition_artifact(interface, artifact_definition_array)
                add_artifact_from_operation_definition_artifact(interface, artifact_definition_array)
            for requirement_assignment in node_template.requirements:
                requirement_assignment: RequirementAssignment
                for interface in requirement_assignment.interfaces:
                    interface: InterfaceDefinition
                    add_artifact_from_notification_definition_artifact(interface, artifact_definition_array)
                    add_artifact_from_operation_definition_artifact(interface, artifact_definition_array)

        for relationship_templates in topology_template.relationship_templates:
            relationship_templates: RelationshipTemplate
            for interface in relationship_templates.interfaces:
                interface: InterfaceDefinition
                add_artifact_from_operation_definition_artifact(interface, artifact_definition_array)
                add_artifact_from_notification_definition_artifact(interface, artifact_definition_array)

    return artifact_definition_array
