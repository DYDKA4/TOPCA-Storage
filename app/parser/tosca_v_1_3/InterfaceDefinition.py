# Extended notation for use in Type definitions
# <interface_definition_name>:
#   type: # <interface_type_name>
#   inputs:
#     <property_definitions>
#   operations:
#     <operation_definitions>
#   notifications:
#     <notification definitions>

# Extended notation for use in Template definitions
# <interface_definition_name>:
#   inputs:
#     <property_assignments>
#   operations:
#     <operation_definitions>
#   notifications:
#     <notification_definitions>
from app.parser.tosca_v_1_3.PropertyAssignment import PropertyAssignment
from app.parser.tosca_v_1_3.PropertyDefinition import PropertyDefinition, property_definition_parser


class InterfaceDefinition:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.vertex_type_system = 'InterfaceDefinition'
        self.type = None
        self.inputs_definition = []
        self.inputs_assignments = []

    def set_type(self, interface_type: str):
        self.type = interface_type

    def add_input_definition(self, inputs: PropertyDefinition):
        self.inputs_definition.append(inputs)

    def add_inputs_assignments(self, inputs: PropertyAssignment):
        self.inputs_assignments.append(inputs)


def interface_definition_parser(name: str, data: dict) -> InterfaceDefinition:
    interface = InterfaceDefinition(name)
    if data.get('type'):
        interface.set_type(data.get('type'))
        if data.get('inputs'):
            for input_property_name, input_property_value in data.get('inputs').items():
                interface.add_input_definition(property_definition_parser(input_property_name, input_property_value))
    else:
        if data.get('inputs'):
            for input_property_name, input_property_value in data.get('inputs').items():
                interface.add_inputs_assignments(PropertyAssignment(input_property_name, str(input_property_value)))
    if data.get('operations'):
        

    return interface

