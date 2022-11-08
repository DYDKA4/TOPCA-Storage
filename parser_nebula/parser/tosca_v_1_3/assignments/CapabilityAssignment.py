# <capability_definition_name>:
#   properties:
#     <property_assignments>
#   attributes:
#     <attribute_assignments>
#   occurrences: [ min_occurrences, max_occurrences ]
from parser_nebula.parser.tosca_v_1_3.assignments.AttributeAssignment import AttributeAssignment, attribute_assignments_parser
from parser_nebula.parser.tosca_v_1_3.assignments.PropertyAssignment import PropertyAssignment
from parser_nebula.parser.tosca_v_1_3.others.Occurrences import Occurrences


class CapabilityAssignment:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.vertex_type_system = 'CapabilityAssignment'
        self.properties = []
        self.attributes = []
        self.occurrences = None

    def add_property(self, properties: PropertyAssignment):
        self.properties.append(properties)

    def add_attributes(self, attribute: AttributeAssignment):
        self.attributes.append(attribute)

    def set_occurrences(self, occurrences: Occurrences):
        self.occurrences = occurrences


def capability_assignment_parser(name: str, data: dict) -> CapabilityAssignment:
    capability = CapabilityAssignment(name)
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            capability.add_property(PropertyAssignment(property_name, property_value))
    if data.get('attributes'):
        for attribute_name, attribute_value in data.get('attributes').items():
            capability.add_attributes(attribute_assignments_parser(attribute_name, attribute_value))
    if data.get('occurrences'):
        occurrences = data.get('occurrences')
        capability.set_occurrences(Occurrences(occurrences[0], occurrences[1]))
    return capability
