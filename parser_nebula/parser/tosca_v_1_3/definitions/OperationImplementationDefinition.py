# Short notation for use with single artifact
# implementation: <primary_artifact_name>

# Short notation for use with multiple artifact
# implementation:
#   primary: <primary_artifact_name> #todo Linker
#   dependencies:
#     - <list_of_dependent_artifact_names> #todo Linker
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

from parser_nebula.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition, artifact_definition_parser


class OperationImplementationDefinition:
    def __init__(self):
        self.vid = None
        self.vertex_type_system = 'OperationImplementationDefinition'
        self.primary = None
        self.dependencies = []
        self.operation_host = None
        self.timeout = None

    def set_primary_artifact_name(self, value: str):
        self.primary = value

    def set_primary_definition(self, primary_definition: ArtifactDefinition):
        self.primary = primary_definition

    def add_dependent_artifact_name(self, dependent_artifact_name: str):
        self.dependencies.append(dependent_artifact_name)

    def add_dependent_artifact_definition(self, dependent_artifact_definition: ArtifactDefinition):
        self.dependencies.append(dependent_artifact_definition)

    def set_operation_host(self, operation_host: str):
        self.operation_host = operation_host

    def set_timeout(self, timeout: int):
        self.timeout = timeout


def operation_implementation_definition_parser(data: dict) -> OperationImplementationDefinition:
    operation = OperationImplementationDefinition()
    short_notation = True
    if type(data) == str:
        operation.set_primary_artifact_name(str(data))
        return operation
    if data.get('primary'):
        short_notation = False
        if type(data.get('primary')) == str:
            operation.set_primary_artifact_name(data.get('primary'))
        else:
            for artifact_name, artifact_value in data.get('primary').items():
                operation.set_primary_definition(artifact_definition_parser(artifact_name, artifact_value))
    if data.get('dependencies'):
        short_notation = False
        for dependency in data.get('dependencies'):
            if type(dependency) == str:
                operation.add_dependent_artifact_name(dependency)
            else:
                for dependent_artifact_name, dependent_artifact_value in dependency.items():
                    operation.add_dependent_artifact_definition(artifact_definition_parser(
                        dependent_artifact_name,
                        dependent_artifact_value))
    if data.get('operation_host'):
        short_notation = False
        operation.set_operation_host(data.get('operation_host'))
    if data.get('timeout'):
        short_notation = False
        operation.set_timeout(data.get('timeout'))
    if short_notation:
        for artifact_name, artifact_value in data.items():
            operation.set_primary_definition(artifact_definition_parser(artifact_name, artifact_value))
    return operation
