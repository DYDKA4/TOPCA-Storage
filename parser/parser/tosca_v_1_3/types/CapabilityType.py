# <capability_type_name>:
#   derived_from: <parent_capability_type_name>
#   version: <version_number>
#   description: <capability_description>
#   properties:
#     <property_definitions>
#   attributes:
#     <attribute_definitions>
#   valid_source_types: [ <node type_names> ]
from parser.parser.tosca_v_1_3.definitions.AttributeDefinition import AttributeDefinition, attribute_definition_parser
from parser.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser.parser.tosca_v_1_3.definitions.PropertyDefinition import PropertyDefinition, property_definition_parser
from parser.parser.tosca_v_1_3.others.Metadata import Metadata


class CapabilityType:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'CapabilityType'
        self.name = name
        self.metadata = []
        self.derived_from = None
        self.version = None
        self.description = None
        self.properties = []
        self.attributes = []
        self.valid_source_types = []

    def set_derived_from(self, derived_from: str):
        self.derived_from = derived_from

    def set_version(self, version: str):
        self.version = version

    def set_description(self, description: str):
        self.description = description

    def add_property(self, properties: PropertyDefinition):
        self.properties.append(properties)

    def add_attribute(self, attribute: AttributeDefinition):
        self.attributes.append(attribute)

    def add_valid_source_type(self, valid_source_type: str):
        self.valid_source_types.append(valid_source_type)

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)


def capability_type_parser(name: str, data: dict) -> CapabilityType:
    capability_type = CapabilityType(name)
    if data.get('derived_from'):
        capability_type.set_derived_from(data.get('derived_from'))
    if data.get('version'):
        capability_type.set_version(data.get('version'))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata').items():
            capability_type.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            capability_type.set_description(description)
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            capability_type.add_property(property_definition_parser(property_name, property_value))
    if data.get('attributes'):
        for attribute_name, attribute_value in data.get('attributes').items():
            capability_type.add_attribute(attribute_definition_parser(attribute_name, attribute_value))
    if data.get('valid_source_types'):
        for valid_source_type in data.get('valid_source_types'):
            capability_type.add_valid_source_type(valid_source_type)
    return capability_type
