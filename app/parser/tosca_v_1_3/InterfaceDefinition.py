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

class InterfaceDefinition:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.vertex_type_system = 'InterfaceDefinition'
        self.type = None
        self.inputs_definition = []

    def set_type(self, interface_type: str):
        self.type = interface_type

    # def add_input_definition(self, input: ):


def interface_definition_parser(name: str, data: dict) -> InterfaceDefinition:
    interface = InterfaceDefinition(name)
    if data.get('type'):
        interface.set_type(data.get('type'))
        if data.get('inputs'):
            interface.add_input()

    return interface

