# <attribute_name>:
#   description: <attribute_description>
#   value: <attribute_value> | { <attribute_value_expression> }
# complete
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser


class AttributeAssignment:
    def __init__(self, name: str, value: str = None):
        self.vid = None
        self.name = name
        self.value = value
        self.description = None
        self.vertex_type_system = 'AttributeAssignment'

    def set_value(self, value: str):
        self.value = value

    def set_description(self, description: str):
        self.description = description


def attribute_assignments_parser(name: str, data: dict) -> AttributeAssignment:
    if type(data) == str:
        return AttributeAssignment(name, str(data))
    attribute = AttributeAssignment(name)
    short_notation = True
    if data.get('description'):
        short_notation = False
        description = description_parser(data)
        attribute.set_description(description)
    if data.get('value'):
        short_notation = False
        attribute.set_value(data.get('value'))
    if short_notation:
        attribute.set_value(str(data))
    return attribute
