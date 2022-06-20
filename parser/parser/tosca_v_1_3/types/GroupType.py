# <group_type_name>:
#   derived_from: <parent_group_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <group_description>
#   attributes :
#     <attribute_definitions>
#   properties:
#     <property_definitions>
#   members: [ <list_of_valid_member_types> ]
from parser.parser.tosca_v_1_3.definitions.AttributeDefinition import AttributeDefinition, attribute_definition_parser
from parser.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser.parser.tosca_v_1_3.others.Metadata import Metadata
from parser.parser.tosca_v_1_3.definitions.PropertyDefinition import PropertyDefinition, property_definition_parser


class GroupType:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'GroupType'
        self.name = name
        self.derived_from = None
        self.version = None
        self.metadata = []
        self.description = None
        self.attributes = []
        self.properties = []
        self.members = []

    def set_derived_from(self, derived_from: str):
        self.derived_from = derived_from

    def set_version(self, version: str):
        self.version = version

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def set_description(self, description: str):
        self.description = description

    def add_attribute(self, attribute: AttributeDefinition):
        self.attributes.append(attribute)

    def add_property(self, properties: PropertyDefinition):
        self.properties.append(properties)

    def add_member(self, valid_member_type: str):
        self.members.append(valid_member_type)


def group_type_parser(name: str, data: dict) -> GroupType:
    group = GroupType(name)
    if data.get('derived_from'):
        group.set_derived_from(data.get('derived_from'))
    if data.get('version'):
        group.set_version(data.get('version'))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata').items():
            group.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            group.set_description(description)
    if data.get('attributes'):
        for attribute_name, attribute_value in data.get('attributes').items():
            group.add_attribute(attribute_definition_parser(attribute_name, attribute_value))
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            group.add_property(property_definition_parser(property_name, property_value))
    if data.get('members'):
        for valid_member_type in data.get('members'):
            group.add_member(valid_member_type)
    return group
