# <notification_name>:
#   description: <notification_description>
#   implementation: <notification_implementation_definition>
#   outputs:
#     <attribute_mappings>
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.NotificationImplementationDefinition import NotificationImplementationDefinition, \
    notification_implementation_definition_parser


class NotificationDefinition:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.vertex_type_system = 'NotificationDefinition'
        self.description = None
        self.implementation = None
        self.outputs = None

    def set_description(self, description: str):
        self.description = description

    def set_implementation(self, implementation: NotificationImplementationDefinition):
        self.implementation = implementation

    def set_outputs(self, outputs: str):
        self.outputs = outputs


def notification_definition_parser(name: str, data: dict) -> NotificationDefinition:
    notification = NotificationDefinition(name)
    if data.get('description'):
        description = description_parser(data)
        notification.set_description(description)
    if data.get('implementation'):
        notification.set_implementation(notification_implementation_definition_parser(data.get('implementation')))
    if data.get('outputs'):
        # todo REMAKE LATER
        notification.set_outputs(str(data.get('outputs')))

    return notification
