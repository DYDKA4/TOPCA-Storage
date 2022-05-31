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

class OperationImplementationDefinition:
    def __init__(self):
        self.vid = None
        self.vertex_type_system = 'OperationImplementationDefinition'
        self.primary_artifact_name = None
        self.primary_name = None
        self.primary_definition = None

    def set_primary_artifact_name(self, value: str):
        self.primary_artifact_name = value

    def set_primary_name(self, primary_name: str):
        self.primary_name = primary_name

    def set_primary_definition(self, primary_name: ?):


def operation_implementation_definition(data: dict) -> OperationImplementationDefinition:
    operation = OperationImplementationDefinition()
    short_notation = True
    if data.get('primary'):
        short_notation = False
        if type(data.get('primary')) == str:
            operation.set_primary_name(data.get('primary'))
        else:
            operation.set_primary_definition
    if short_notation:
        operation.set_primary_artifact_name(str(data))
    return operation
