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
from parser.parser.tosca_v_1_3.definitions.NotificationImplementationDefinition import \
    NotificationImplementationDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_notification_implementation_definition(service_template: ServiceTemplateDefinition,
                                                notification: NotificationImplementationDefinition) -> None:
    if type(notification.primary) == str:
        link_by_type_name(service_template.artifact_types, notification, 'type', )
    link_members(service_template.node_types, notification)
    if str in {type(notification.primary)}:
        abort(400)
