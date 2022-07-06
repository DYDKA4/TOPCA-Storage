# Short notation for use with single artifact
# implementation: <primary_artifact_name>

#  Short notation for use with multiple artifact
# implementation:
#   primary: <primary_artifact_name>
#   dependencies:
#     - <list_of_dependent_artifact_names>
from parser.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition, artifact_definition_parser


class NotificationImplementationDefinition:
    def __init__(self):
        self.vid = None
        self.vertex_type_system = 'NotificationImplementationDefinition'
        self.primary = None
        self.dependencies = []

    def set_primary(self, primary: str):
        self.primary = primary

    def add_dependencies_artefact_names(self, dependency: str):
        self.dependencies.append(dependency)


def notification_implementation_definition_parser(data: dict) -> NotificationImplementationDefinition:
    notification = NotificationImplementationDefinition()
    if type(data) == str:
        notification.set_primary(str(data))
        return notification
    if data.get('primary'):
        if type(data.get('primary')) == str:
            notification.set_primary(data.get('primary'))
    if data.get('dependencies'):
        for dependency in data.get('dependencies'):
            notification.add_dependencies_artefact_names(dependency)
    return notification
