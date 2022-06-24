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
from parser.linker.LinkerValidTypes import link_with_list
from parser.parser.tosca_v_1_3.definitions.NotificationImplementationDefinition import \
    NotificationImplementationDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_notification_implementation_definition(service_template: ServiceTemplateDefinition,
                                                notification: NotificationImplementationDefinition) -> None:
    list_of_artifact_definition = get_all_artifact_definition(service_template)
    if type(notification.primary) == str:
        link_by_type_name(list_of_artifact_definition, notification, 'primary')

    link_with_list(list_of_artifact_definition, notification, 'dependencies')
    if str in {type(notification.primary)}:
        abort(400)
