# Short notation for use with single artifact
# implementation: <primary_artifact_name>

# Short notation for use with multiple artifact
# implementation:
#   primary: <primary_artifact_name>
#   dependencies:
#     - <list_of_dependent_artifact_names>
#   operation_host : SELF
#   timeout : 60

# Extended notation for use with single artifact
# implementation:
#   primary:
#     <primary_artifact_definition>
#   operation_host : HOST
#   timeout : 100

# Extended notation for use with multiple artifacts
# implementation:
#   primary:
#     <primary_artifact_definition>
#   dependencies:
#     - <list_of_dependent_artifact definitions>
#   operation_host: HOST
#   timeout: 120
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.ArtifactDefinition import ArtifactDefinition, artifact_definition_parser


class OperationImplementationDefinition:
    def __init__(self):
        self.vid = None
        self.vertex_type_system = 'OperationImplementationDefinition'
        self.primary_artifact_name = None
        self.primary_name = None
        self.primary_definition = None
        self.list_of_dependent_artifact_names = []
        self.list_of_dependent_artifact_definitions = []
        self.operation_host = None
        self.timeout = None

    def set_primary_artifact_name(self, value: str):
        self.primary_artifact_name = value

    def set_primary_name(self, primary_name: str):
        self.primary_name = primary_name

    def set_primary_definition(self, primary_definition: ArtifactDefinition):
        self.primary_definition = primary_definition

    def add_dependent_artifact_name(self, dependent_artifact_name: str):
        self.list_of_dependent_artifact_names.append(dependent_artifact_name)

    def add_dependent_artifact_definition(self, dependent_artifact_definition: ArtifactDefinition):
        self.list_of_dependent_artifact_definitions.append(dependent_artifact_definition)

    def set_operation_host(self, operation_host: str):
        self.operation_host = operation_host

    def set_timeout(self, timeout: int):
        self.timeout = timeout


def operation_implementation_definition(data: dict) -> OperationImplementationDefinition:
    operation = OperationImplementationDefinition()
    short_notation = True
    if data.get('primary'):
        short_notation = False
        if type(data.get('primary')) == str:
            operation.set_primary_name(data.get('primary'))
        else:
            for artifact_name, artifact_value in data.get('primary'):
                operation.set_primary_definition(artifact_definition_parser(artifact_name, artifact_value))
    if data.get('dependencies'):
        short_notation = False
        for dependency in data.get('dependencies'):
            if type(dependency) == str:
                if operation.primary_definition:
                    abort(400)
                for dependent_artifact_name in dependency:
                    operation.add_dependent_artifact_name(dependent_artifact_name)
            else:
                if operation.primary_name:
                    abort(400)
                for dependent_artifact_name, dependent_artifact_value in dependency:
                    operation.add_dependent_artifact_definition(artifact_definition_parser(
                        dependent_artifact_name,
                        dependent_artifact_value))
    if data.get('operation_host'):
        short_notation = False
        operation.set_operation_host(data.get('operation_host'))
    if data.get(' timeout'):
        short_notation = False
        operation.set_timeout(data.get('timeout'))
    if short_notation:
        operation.set_primary_artifact_name(str(data))
    return operation
