# Short notation for use with single artifact
# implementation: <primary_artifact_name>

#  Short notation for use with multiple artifact
# implementation:
#   primary: <primary_artifact_name>
#   dependencies:
#     - <list_of_dependent_artifact_names>
from app.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition, artifact_definition_parser


class NotificationImplementationDefinition:
    def __init__(self):
        self.vid = None
        self.vertex_type_system = 'NotificationImplementationDefinition'
        self.primary = None
        self.implementation = None
        self.primary_artifact_name = None
        self.dependencies_artefact_names = []

    def set_primary_artifact_name(self, primary_artifact_name: str):
        self.primary_artifact_name = primary_artifact_name

    def set_primary(self, primary: ArtifactDefinition):
        self.primary = primary

    def add_dependencies_artefact_names(self, dependency: str):
        self.dependencies_artefact_names.append(dependency)


def notification_implementation_definition_parser(data: dict) -> NotificationImplementationDefinition:
    notification = NotificationImplementationDefinition()
    short_notation = True
    if data.get('primary'):
        short_notation = False
        for artifact_name, artifact_value in data.get('primary'):
            notification.set_primary(artifact_definition_parser(artifact_name, artifact_value))
    if data.get('dependencies'):
        for dependency in data.get('dependencies'):
            for artefact_names in dependency:
                notification.add_dependencies_artefact_names(artefact_names)
    if short_notation:
        notification.set_primary_artifact_name(str(data))

    return notification
