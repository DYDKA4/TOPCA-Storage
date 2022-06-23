# Short notation for use with single artifact
# implementation: <primary_artifact_name>

#  Short notation for use with multiple artifact
# implementation:
#   primary: <primary_artifact_name>
#   dependencies:
#     - <list_of_dependent_artifact_names>
from werkzeug.exceptions import abort

from parser.linker.LinkByName import link_by_type_name
from parser.linker.LinkerValidTypes import link_members
from parser.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment
from parser.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition
from parser.parser.tosca_v_1_3.definitions.NotificationDefinition import NotificationDefinition
from parser.parser.tosca_v_1_3.definitions.NotificationImplementationDefinition import \
    NotificationImplementationDefinition
from parser.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition
from parser.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition
from parser.parser.tosca_v_1_3.definitions.RequirementDefinition import RequirementDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate
from parser.parser.tosca_v_1_3.types.InterfaceType import InterfaceType
from parser.parser.tosca_v_1_3.types.NodeType import NodeType
from parser.parser.tosca_v_1_3.types.RelationshipType import RelationshipType


def linker_operation_definition_artifact(interface, notification):
    for operation_definition in interface.operations:
        operation_definition: OperationDefinition
        operation_definition_implementation: OperationImplementationDefinition = \
            operation_definition.implementation
        if type(operation_definition_implementation.primary) not in {str, dict}:
            artifact: ArtifactDefinition = operation_definition_implementation.primary
            if artifact.name == notification.primary:
                notification.primary = {'primary': [notification, artifact]}


def linker_notification_definition_artifact(interface, notification):
    for notification_definition in interface.notifications:
        notification_definition: NotificationDefinition
        notification_definition_implementation: OperationImplementationDefinition \
            = notification_definition.implementation
        if type(notification_definition_implementation.primary) not in {str, dict}:
            artifact: ArtifactDefinition = notification_definition_implementation.primary
            if artifact.name == notification.primary:
                notification.primary = {'primary': [notification, artifact]}


def link_notification_implementation_definition(service_template: ServiceTemplateDefinition,
                                                notification: NotificationImplementationDefinition) -> None:
    # todo Maybe errors?
    if type(notification.primary) == str:
        for node_type in service_template.node_types:
            node_type: NodeType
            link_by_type_name(node_type.artifacts, notification, 'primary', )
            if type(notification.primary) != str:
                return
            for interface in node_type.interfaces:
                interface: InterfaceDefinition
                linker_operation_definition_artifact(interface, notification)
                # todo if artifact definition in notification uncomment it
                # linker_notification_definition_artifact(interface,notification)
                if type(notification.primary) != str:
                    return
            for requirement_definition in node_type.requirements:
                requirement_definition: RequirementDefinition
                for interface in requirement_definition.interfaces:
                    interface: InterfaceDefinition
                    # todo if artifact definition in notification uncomment it
                    # linker_notification_definition_artifact
                    if type(notification.primary) != str:
                        return
                    linker_operation_definition_artifact(interface, notification)
                    if type(notification.primary) != str:
                        return

    if type(notification.primary) == str:
        for interface in service_template.interface_types:
            interface: InterfaceType
            # todo if artifact definition in notification uncomment it
            # linker_notification_definition_artifact
            if type(notification.primary) != str:
                return
            linker_operation_definition_artifact(interface, notification)
            if type(notification.primary) != str:
                return

    if type(notification.primary) == str:
        for relationship_type in service_template.relationship_types:
            relationship_type: RelationshipType
            for interface in relationship_type.interfaces:
                interface: InterfaceDefinition
                # todo if artifact definition in notification uncomment it
                # linker_notification_definition_artifact
                if type(notification.primary) != str:
                    return
                linker_operation_definition_artifact(interface, notification)
                if type(notification.primary) != str:
                    return

    topology_template: TemplateDefinition = service_template.topology_template
    if type(notification.primary) == str and topology_template:
        for node_template in topology_template.node_templates:
            node_template: NodeTemplate
            link_by_type_name(node_template.artifacts, notification, 'primary')
            if type(notification) == str:
                break
            for interface in node_template.interfaces:
                interface: InterfaceDefinition
                linker_operation_definition_artifact(interface, notification)
                # todo if artifact definition in notification uncomment it
                # linker_notification_definition_artifact(interface,notification)
                if type(notification) == str:
                    break
            for requirement_assignment in node_template.requirements:
                requirement_assignment: RequirementAssignment
                for interface in requirement_assignment.interfaces:
                    interface: InterfaceDefinition
                    linker_operation_definition_artifact(interface, notification)
                    # todo if artifact definition in notification uncomment it
                    # linker_notification_definition_artifact(interface,notification)
                    if type(notification) == str:
                        break
        for relationship_templates in topology_template.relationship_templates:
            relationship_templates: RelationshipTemplate
            for interface in relationship_templates.interfaces:
                interface: InterfaceDefinition
                # todo if artifact definition in notification uncomment it
                # linker_notification_definition_artifact
                if type(notification.primary) != str:
                    return
                linker_operation_definition_artifact(interface, notification)
                if type(notification.primary) != str:
                    return

    link_members(service_template.node_types, notification)
    if str in {type(notification.primary)}:
        abort(400)
