# <notification_name>:
#   description: <notification_description>
#   implementation: <notification_implementation_definition>
#   outputs:
#     <attribute_mappings>
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser


class NotificationDefinition:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.vertex_type_system = 'NotificationDefinition'
        self.description = None
        self.implementation = None

    def set_description(self, description: str):
        self.description = description

    def set_implementation(self,implementation: ?):


def notification_definition(name: str, data: dict) -> NotificationDefinition:
    notification = NotificationDefinition(name)
    if data.get('description'):
        description = description_parser(data)
        notification.set_description(description)
    return notification
