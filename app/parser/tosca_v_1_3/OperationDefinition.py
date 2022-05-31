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
from app.parser.tosca_v_1_3.OperationImplementationDefinition import OperationImplementationDefinition, \
    operation_implementation_definition_parser
from app.parser.tosca_v_1_3.PropertyAssignment import PropertyAssignment
from app.parser.tosca_v_1_3.PropertyDefinition import property_definition_parser, PropertyDefinition


class OperationDefinition:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.implementation_artifact_name = None
        self.vertex_type_system = 'OperationDefinition'
        self.description = None
        self.implementation = None
        self.inputs_definition = []
        self.outputs = []
        self.inputs_assignment = []

    def set_implementation_artifact_name(self, value: str):
        self.implementation_artifact_name = value

    def set_description(self, description: str):
        self.description = description

    def set_implementation(self, implementation: OperationImplementationDefinition):
        self.implementation = implementation

    def set_outputs(self, outputs):
        #todo remake later
        self.outputs = outputs

    def add_input_definition(self, inputs: PropertyDefinition):
        self.input_definition.append(inputs)

    def add_inputs_assignment(self, inputs: PropertyAssignment ):
        self.inputs_assignment.append(inputs)

def operation_definition(name: str, data: dict) -> OperationDefinition:
    operation = OperationDefinition(name)
    short_notation = True
    if data.get('description'):
        short_notation = False
        description = description_parser(data)
        operation.set_description(description)
    if data.get('implementation'):
        short_notation = False
        implementation = data.get('implementation')
        operation.set_implementation(operation_implementation_definition_parser(implementation))
    if data.get('outputs'):
        short_notation = False
        operation.set_outputs(data.get('outputs'))
        if data.get('inputs'):
            for input_property_name, input_property_value in data.get('inputs').items():
                operation.add_input_definition(property_definition_parser(input_property_name, input_property_value))
    if data.get('inputs'): #todo look at 71 to 77 may be wrong?
        for input_property_name, input_property_value in data.get('inputs').items():
            operation.add_inputs_assignment(PropertyAssignment(input_property_name, str(input_property_value)))


    if short_notation:
        operation.set_implementation_artifact_name(str(data))
    return operation
