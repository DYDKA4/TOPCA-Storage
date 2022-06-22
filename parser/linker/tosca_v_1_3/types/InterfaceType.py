# <interface_type_name>:
#   derived_from: <parent_interface_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <interface_description>
#   inputs:
#     <property_definitions>
#   operations:
#     <operation_definitions>
#   notifications:
#     <notification definitions>
from parser.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser.parser.tosca_v_1_3.others.Metadata import Metadata
from parser.parser.tosca_v_1_3.definitions.NotificationDefinition import NotificationDefinition, notification_definition_parser
from parser.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition, operation_definition_parser
from parser.parser.tosca_v_1_3.definitions.PropertyDefinition import PropertyDefinition, property_definition_parser


class InterfaceType:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'InterfaceType'
        self.name = name
        self.derived_from = None
        self.version = None
        self.metadata = []
        self.description = None
        self.inputs = []
        self.operations = []
        self.notifications = []

    def set_derived_from(self, derived_from: str):
        self.derived_from = derived_from

    def set_version(self, version: str):
        self.version = version

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def set_description(self, description: str):
        self.description = description

    def add_input(self, inputs: PropertyDefinition):
        self.inputs.append(inputs)

    def add_operation(self, operation: OperationDefinition):
        self.operations.append(operation)

    def add_notification(self, notifications: NotificationDefinition):
        self.notifications.append(notifications)


def interface_type_parser(name: str, data: dict) -> InterfaceType:
    interface = InterfaceType(name)
    if data.get('derived_from'):
        interface.set_derived_from(data.get('derived_from'))
    if data.get('version'):
        interface.set_version(data.get('version'))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata').items():
            interface.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            interface.set_description(description)
    if data.get('inputs'):
        for property_name, property_value in data.get('inputs').items():
            interface.add_input(property_definition_parser(property_name, property_value))
    if data.get('operations'):
        for operation_name, operation_value in data.get('operations').items():
            interface.add_operation(operation_definition_parser(operation_name, operation_value))
    if data.get('notifications'):
        for notification_name, notification_value in data.get('notifications').items():
            interface.add_notification(notification_definition_parser(notification_name, notification_value))
    return interface
