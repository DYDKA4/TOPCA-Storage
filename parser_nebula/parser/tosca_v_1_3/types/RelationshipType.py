# <relationship_type_name>:
#   derived_from: <parent_relationship_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <relationship_description>
#   properties:
#     <property_definitions>
#   attributes:
#     <attribute_definitions>
#   interfaces:
#     <interface_definitions>
#   valid_target_types: [ <capability_type_names> ]
from parser_nebula.parser.tosca_v_1_3.definitions.AttributeDefinition import AttributeDefinition, attribute_definition_parser
from parser_nebula.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser_nebula.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition, interface_definition_parser
from parser_nebula.parser.tosca_v_1_3.others.Metadata import Metadata
from parser_nebula.parser.tosca_v_1_3.definitions.PropertyDefinition import PropertyDefinition, property_definition_parser


class RelationshipType:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'RelationshipType'
        self.name = name
        self.derived_from = None
        self.version = None
        self.metadata = []
        self.description = None
        self.properties = []
        self.attributes = []
        self.interfaces = []
        self.valid_target_types = []

    def set_derived_from(self, derived_from: str):
        self.derived_from = derived_from

    def set_version(self, version: str):
        self.version = version

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def set_description(self, description: str):
        self.description = description

    def add_property(self, properties: PropertyDefinition):
        self.properties.append(properties)

    def add_attribute(self, attribute: AttributeDefinition):
        self.attributes.append(attribute)

    def add_interface(self, interface: InterfaceDefinition):
        self.interfaces.append(interface)

    def add_valid_source_type(self, valid_source_type: str):
        self.valid_target_types.append(valid_source_type)


def relationship_type_parser(name: str, data: dict) -> RelationshipType:
    relationship = RelationshipType(name)
    if data.get('derived_from'):
        relationship.set_derived_from(data.get('derived_from'))
    if data.get('version'):
        relationship.set_version(data.get('version'))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata').items():
            relationship.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            relationship.set_description(description)
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            relationship.add_property(property_definition_parser(property_name, property_value))
    if data.get('attributes'):
        for attribute_name, attribute_value in data.get('attributes').items():
            relationship.add_attribute(attribute_definition_parser(attribute_name, attribute_value))
    if data.get('interfaces'):
        for interface_name, interface_value in data.get('interfaces').items():
            relationship.add_interface(interface_definition_parser(interface_name, interface_value))
    if data.get('valid_target_types'):
        for valid_source_type in data.get('valid_target_types'):
            relationship.add_valid_source_type(valid_source_type)
    return relationship
