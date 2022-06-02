# Short notation
# <capability_definition_name>: <capability_type>

# Extended notation
# <capability_definition_name>:
#   type: # <capability_type> Required
#   description: <capability_description>
#   properties:
#     <property_definitions>
#   attributes:
#     <attribute_definitions>
#   valid_source_types: [ <node type_names> ]
#   occurrences : <range_of_occurrences>
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.AttributeDefinition import AttributeDefinition, attribute_definition_parser
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.PropertyDefinition import PropertyDefinition, property_definition_parser


class CapabilityDefinition:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'CapabilityDefinition'
        self.name = name
        self.type = None
        self.description = None
        self.properties = []
        self.attributes = []
        self.valid_source_types = []
        self.occurrences = []

    def set_type(self, capability_type: str):
        self.type = capability_type

    def set_description(self, description: str):
        self.description = description

    def add_property(self, properties: PropertyDefinition):
        self.properties.append(properties)

    def add_attribute(self, attribute: AttributeDefinition):
        self.attributes.append(attribute)

    def add_valid_source_type(self, valid_source_type: str):
        self.valid_source_types.append(valid_source_type)

    def set_occurrences(self, occurrences: list):
        self.occurrences = occurrences


def capability_definition_parser(name: str, data: dict) -> CapabilityDefinition:
    capability = CapabilityDefinition(name)
    short_notation = True
    if data.get('type'):
        short_notation = False
        capability.set_type(data.get('type'))
    if data.get('description'):
        short_notation = False
        description = description_parser(data)
        capability.set_description(description)
    if data.get('properties'):
        short_notation = False
        for property_name, property_value in data.get('inputs').items():
            capability.add_property(property_definition_parser(property_name, property_value))
    if data.get('attributes'):
        short_notation = False
        for attribute_name, attribute_value in data.get('attributes').items():
            capability.add_attribute(attribute_definition_parser(attribute_name, attribute_value))
    if data.get('valid_source_types'):
        short_notation = False
        for valid_source_type in data.get('valid_source_types'):
            capability.add_valid_source_type(valid_source_type)
    if data.get('occurrences'):
        short_notation = False
        capability.set_occurrences(data.get('occurrences'))
    if short_notation:
        capability.set_type(str(data))
    elif capability.type is None:
        abort(400)
    return capability

