# Short notation for use with single artifact
# implementation: <primary_artifact_name>

#  Short notation for use with multiple artifact
# implementation:
#   primary: <primary_artifact_name>
#   dependencies:
#     - <list_of_dependent_artifact_names>
from werkzeug.exceptions import abort

from parser.linker.GetAllArtifactDefinition import get_all_artifact_definition
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


def link_notification_implementation_definition(service_template: ServiceTemplateDefinition,
                                                notification: NotificationImplementationDefinition) -> None:
    list_of_artifact_definition = get_all_artifact_definition(service_template)
    if type(notification.primary) == str:
        link_by_type_name(list_of_artifact_definition, notification, 'primary')
    link_members(list_of_artifact_definition, notification)
    if str in {type(notification.primary)}:
        abort(400)
