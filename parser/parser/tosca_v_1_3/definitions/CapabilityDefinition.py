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

from parser.parser.tosca_v_1_3.definitions.AttributeDefinition import AttributeDefinition, attribute_definition_parser
from parser.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser.parser.tosca_v_1_3.definitions.PropertyDefinition import PropertyDefinition, property_definition_parser
from parser.parser.tosca_v_1_3.others.Occurrences import Occurrences


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

    def set_occurrences(self, occurrences: Occurrences):
        self.occurrences = occurrences


def capability_definition_parser(name: str, data: dict) -> CapabilityDefinition:
    capability = CapabilityDefinition(name)
    if type(data) == str:
        capability.set_type(str(data))
        return capability
    if data.get('type'):
        capability.set_type(data.get('type'))
    if data.get('description'):
        description = description_parser(data)
        capability.set_description(description)
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            capability.add_property(property_definition_parser(property_name, property_value))
    if data.get('attributes'):
        for attribute_name, attribute_value in data.get('attributes').items():
            capability.add_attribute(attribute_definition_parser(attribute_name, attribute_value))
    if data.get('valid_source_types'):
        for valid_source_type in data.get('valid_source_types'):
            capability.add_valid_source_type(valid_source_type)
    if data.get('occurrences'):
        occurrences = data.get('occurrences')
        capability.set_occurrences(Occurrences(occurrences[0], occurrences[1]))
    if capability.type is None:
        abort(400)
    return capability

