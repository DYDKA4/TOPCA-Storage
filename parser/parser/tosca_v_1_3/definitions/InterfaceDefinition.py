# Extended notation for use in Type definitions
# <interface_definition_name>:
#   type: # <interface_type_name>
#   inputs:
#     <property_definitions>
#   operations:
#     <operation_definitions>
#   notifications:
#     <notification definitions>

# Extended notation for use in TemplateDefinition definitions
# <interface_definition_name>:
#   inputs:
#     <property_assignments>
#   operations:
#     <operation_definitions>
#   notifications:
#     <notification_definitions>
from parser.parser.tosca_v_1_3.definitions.NotificationDefinition import NotificationDefinition, notification_definition_parser
from parser.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition, operation_definition_parser
from parser.parser.tosca_v_1_3.assignments.PropertyAssignment import PropertyAssignment
from parser.parser.tosca_v_1_3.definitions.PropertyDefinition import PropertyDefinition, property_definition_parser


class InterfaceDefinition:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.vertex_type_system = 'InterfaceDefinition'
        self.type = None
        self.inputs = []
        self.operations = []
        self.notifications = []

    def set_type(self, interface_type: str):
        self.type = interface_type

    def add_input_definition(self, inputs: PropertyDefinition):
        self.inputs.append(inputs)

    def add_inputs_assignments(self, inputs: PropertyAssignment):
        self.inputs.append(inputs)

    def add_operation(self, operation: OperationDefinition):
        self.operations.append(operation)

    def add_notification(self, notifications: NotificationDefinition):
        self.notifications.append(notifications)


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
                interface.add_inputs_assignments(PropertyAssignment(input_property_name, input_property_value))
    if data.get('operations'):
        for operation_name, operation_value in data.get('operations').items():
            interface.add_operation(operation_definition_parser(operation_name, operation_value))
    if data.get('notifications'):
        for notification_name, notification_value in data.get('notifications').items():
            interface.add_notification(notification_definition_parser(notification_name, notification_value))
    return interface

