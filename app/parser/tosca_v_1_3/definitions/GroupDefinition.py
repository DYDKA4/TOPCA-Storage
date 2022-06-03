# <group_name>:
#   type: # <group_type_name> Required
#   description: <group_description>
#   metadata:
#     <map of string>
#   attributes :
#     <attribute_assignments>
#   properties:
#     <property_assignments>
#   members: [ <list_of_node_templates> ]
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.assignments.AttributeAssignment import AttributeAssignment, attribute_assignments_parser
from app.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.others.Metadata import Metadata
from app.parser.tosca_v_1_3.assignments.PropertyAssignment import PropertyAssignment


class GroupDefinition:
    def __init__(self, name: str):
        self.vid = None
        self.name = name
        self.vertex_type_system = 'GroupDefinition'
        self.type = None
        self.description = None
        self.metadata = []
        self.attributes = []
        self.properties = []
        self.attributes = []
        self.members = []

    def set_type(self, group_type: str):
        self.type = group_type

    def set_description(self, description: str):
        self.description = description

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def add_property(self, properties: PropertyAssignment):
        self.properties.append(properties)

    def add_attributes(self, attribute: AttributeAssignment):
        self.attributes.append(attribute)

    def add_members(self, member: str):
        self.members.append(member)


def group_definition_parser(name: str, data: dict) -> GroupDefinition:
    group = GroupDefinition(name)
    if data.get('type'):
        group.set_type(data.get('type'))
    else:
        abort(400)
    if data.get('description'):
        description = description_parser(data)
        group.set_description(description)
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata'):
            group.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            group.add_property(PropertyAssignment(property_name, property_value))
    if data.get('attributes'):
        for attribute_name, attribute_value in data.get('attributes').items():
            group.add_attributes(attribute_assignments_parser(attribute_name, attribute_value))
    if data.get('members'):
        for member in data.get('members'):
            group.add_members(member)
    return group
