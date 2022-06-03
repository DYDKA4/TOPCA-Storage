# <relationship_template_name>:
#   type: # <relationship_type_name> Required
#   description: <relationship_type_description>
#   metadata:
#     <map of string>
#   properties:
#     <property_assignments>
#   attributes:
#     <attribute_assignments>
#   interfaces:
#     <interface_definitions>
#   copy:
#     <source_relationship_template_name>
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.assignments.AttributeAssignment import AttributeAssignment, attribute_assignments_parser
from app.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition, interface_definition_parser
from app.parser.tosca_v_1_3.others.Metadata import Metadata
from app.parser.tosca_v_1_3.assignments.PropertyAssignment import PropertyAssignment


class RelationshipTemplate:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.vertex_type_system = 'RelationshipTemplate'
        self.type = None
        self.description = None
        self.metadata = []
        self.properties = []
        self.attributes = []
        self.interfaces = []
        self.copy = None

    def set_type(self, relationship_type: str):
        self.type = relationship_type

    def set_description(self, description: str):
        self.description = description

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def add_property(self, properties: PropertyAssignment):
        self.properties.append(properties)

    def add_attributes(self, attribute: AttributeAssignment):
        self.attributes.append(attribute)

    def add_interface(self, interface: InterfaceDefinition):
        self.interfaces.append(interface)

    def set_copy(self, copy: str):
        self.copy = copy


def relationship_template_parser(name: str, data: dict) -> RelationshipTemplate:
    relationship = RelationshipTemplate(name)
    if data.get('type'):
        relationship.set_type(data.get('type'))
    else:
        abort(400)
    if data.get('description'):
        description = description_parser(data)
        relationship.set_description(description)
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata'):
            relationship.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            relationship.add_property(PropertyAssignment(property_name, property_value))
    if data.get('attributes'):
        for attribute_name, attribute_value in data.get('attributes').items():
            relationship.add_attributes(attribute_assignments_parser(attribute_name, attribute_value))
    if data.get('interfaces'):
        for interface_name, interface_value in data.get('interface').items():
            relationship.add_interface(interface_definition_parser(interface_name, interface_value))
    if data.get('copy'):
        relationship.set_copy(data.get('copy'))
    return relationship
