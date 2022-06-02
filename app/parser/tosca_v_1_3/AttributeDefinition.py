# attributes:
#   <attribute_name>:
#     type: # <attribute_type> Required
#     description: <attribute_description>
#     default: <default_value>
#     status: <status_value>
#     key_schema : <key_schema_definition>
#     entry_schema: <entry_schema_definition>
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.SchemaDefinition import SchemaDefinition, schema_definition_parser


class AttributeDefinition:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'AttributeDefinition'
        self.name = name
        self.type = None
        self.description = None
        self.default = None
        self.status = None
        self.entry_schema = None
        self.key_schema = None

    def set_type(self, attribute_type: str):
        self.type = attribute_type

    def set_description(self, description: str):
        self.description = description

    def set_default(self, default: str):
        self.default = default

    def set_status(self, status: str):
        self.status = status

    def set_key_schema(self, key_schema: SchemaDefinition):
        self.key_schema = key_schema

    def set_entry_schema(self, entry_schema: SchemaDefinition):
        self.entry_schema = entry_schema


def attribute_definition_parser(name: str, data: dict) -> AttributeDefinition:
    attribute = AttributeDefinition(name)
    if data.get('type'):
        attribute.set_type(data.get('type'))
    else:
        abort(400)
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            attribute.set_description(description)
    if data.get('default'):  # todo Data type problem?
        attribute.set_default(data.get('default'))
    if data.get('status'):
        attribute.set_status(data.get('status'))
    if data.get('key_schema'):
        attribute.set_key_schema(schema_definition_parser(data.get('key_schema')))
    if data.get('entry_schema'):
        attribute.set_entry_schema(schema_definition_parser(data.get('entry_schema')))
    return attribute
