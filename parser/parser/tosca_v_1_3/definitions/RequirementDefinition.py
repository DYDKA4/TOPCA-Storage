# Simple grammar (Capability Type only)
# <requirement_definition_name>: <capability_type_name>

# Extended grammar (with Node and Relationship Types)
# <requirement_definition_name>:
#   capability: <capability_type_name> Required
#   node: <node_type_name>
#   relationship: <relationship_type_name>
#   occurrences: [ <min_occurrences>, <max_occurrences> ]

# Extended grammar for declaring Property Definitions on the relationship’s Interfaces
# <requirement_definition_name>:
#   # Other keynames omitted for brevity
#   relationship:
#     type: # <relationship_type_name> Required
#     interfaces:
#       <interface_definitions>
import inspect

from parser.parser import ParserException
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition, interface_definition_parser
from parser.parser.tosca_v_1_3.others.Occurrences import Occurrences


class RequirementDefinition:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'RequirementDefinition'
        self.name = name
        self.capability = None
        self.node = None
        self.relationship = None
        self.interfaces = []
        self.occurrences = None

    def set_capability(self, capability: str):
        self.capability = capability

    def set_node(self, node: str):
        self.node = node

    def set_relationship_type_name(self, relationship_type_name: str):
        self.relationship = relationship_type_name

    def add_interface(self, interface: InterfaceDefinition):
        self.interfaces.append(interface)

    def set_occurrences(self, occurrences: Occurrences):
        self.occurrences = occurrences


def requirement_definition_parser(name: str, data: dict) -> RequirementDefinition:
    requirement = RequirementDefinition(name)
    if type(data) == str:
        requirement.set_capability(str(data))
        return requirement
    if data.get('capability'):
        requirement.set_capability(data.get('capability'))
    if data.get('node'):
        requirement.set_node(data.get('node'))
    if data.get('relationship'):
        relationship = data.get('relationship')
        if type(relationship) == str:
            requirement.set_relationship_type_name(relationship)
        else:
            if relationship.get('type'):
                requirement.set_relationship_type_name(relationship.get('type'))
            else:
                raise ParserException(400, inspect.stack()[0][3] + ': no_type')
            if relationship.get('interfaces'):
                for interface_name, interface_value in relationship.get('interfaces').items():
                    requirement.add_interface(interface_definition_parser(interface_name, interface_value))
    if data.get('occurrences'):
        occurrences = data.get('occurrences')
        requirement.set_occurrences(Occurrences(occurrences[0], occurrences[1]))
    if requirement.capability is None:
        raise ParserException(400, inspect.stack()[0][3] + ': requirement.capability is None')
    return requirement
