# Short notation
# <operation_name>: <implementation_artifact_name>

# Extended notation for use in Type definitions
# <operation_name>:
#    description: <operation_description>
#    implementation: <Operation implementation definition>
#    inputs:
#      <property_definitions>
#    outputs: WRONG?
#       <interface mappings>

# Extended notation for use in TemplateDefinition definitions
# <operation_name>:
#    description: <operation_description>
#    implementation: <Operation implementation definition>
#    inputs:
#      <property_assignments>
from parser_nebula.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser_nebula.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition, \
    operation_implementation_definition_parser
from parser_nebula.parser.tosca_v_1_3.assignments.PropertyAssignment import PropertyAssignment
from parser_nebula.parser.tosca_v_1_3.definitions.ParameterDefinition import ParameterDefinition, parameter_definition_parser
from parser_nebula.parser.tosca_v_1_3.definitions.PropertyDefinition import property_definition_parser, PropertyDefinition


class OperationDefinition:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.vertex_type_system = 'OperationDefinition'
        self.description = None
        self.implementation = None
        self.inputs = []
        self.outputs = []

    def set_implementation_artifact_name(self, value: str):
        self.implementation = value

    def set_description(self, description: str):
        self.description = description

    def set_implementation(self, implementation: OperationImplementationDefinition):
        self.implementation = implementation

    def set_outputs(self, outputs):
        # todo remake later
        self.outputs = outputs

    def add_input_definition(self, inputs: PropertyDefinition):
        self.inputs.append(inputs)

    def add_inputs_assignment(self, inputs: PropertyAssignment):
        self.inputs.append(inputs)


def operation_definition_parser(name: str, data: dict) -> OperationDefinition:
    operation = OperationDefinition(name)
    if type(data) == str:
        operation.set_implementation_artifact_name(str(data))
        return operation
    if data.get('description'):
        description = description_parser(data)
        operation.set_description(description)
    if data.get('implementation'):
        implementation = data.get('implementation')
        operation.set_implementation(operation_implementation_definition_parser(implementation))
    if data.get('outputs'):
        operation.set_outputs(data.get('outputs'))
    if data.get('inputs'):
        for input_property_name, input_property_value in data.get('inputs').items():
            if type(input_property_value) == str:
                operation.add_inputs_assignment(PropertyAssignment(input_property_name, input_property_value))
            else:
                operation.add_input_definition(property_definition_parser(input_property_name, input_property_value))
    return operation
