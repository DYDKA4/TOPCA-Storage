# Short notation
# <operation_name>: <implementation_artifact_name>

# Extended notation for use in Type definitions
# <operation_name>:
#    description: <operation_description>
#    implementation: <Operation implementation definition>
#    inputs:
#      <property_definitions>
#    outputs: WRONG?
#       <attribute mappings>

# Extended notation for use in Template definitions
# <operation_name>:
#    description: <operation_description>
#    implementation: <Operation implementation definition>
#    inputs:
#      <property_assignments>
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser


class OperationDefinition:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.implementation_artifact_name = None
        self.vertex_type_system = 'OperationDefinition'
        self.description = None
        self.implementation = None

    def set_implementation_artifact_name(self, value: str):
        self.implementation_artifact_name = value

    def set_description(self, description: str):
        self.description = description

    def set_implementation(self, implementation:):


def operation_definition(name: str, data: dict) -> OperationDefinition:
    operation = OperationDefinition(name)
    short_notation = True
    if data.get('description'):
        description = description_parser(data)
        operation.set_description(description)

    if short_notation:
        operation.set_implementation_artifact_name(str(data))
    return operation
