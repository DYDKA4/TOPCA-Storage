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
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.InterfaceDefinition import InterfaceDefinition, interface_definition_parser


class RequirementDefinition:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'RequirementDefinition'
        self.name = name
        self.capability = None
        self.node = None
        self.relationship_type_name = None
        self.type = None
        self.interfaces = []
        self.occurrences = []

    def set_capability(self, capability: str):
        self.capability = capability

    def set_node(self, node: str):
        self.node = node

    def set_relationship_type_name(self, relationship_type_name: str):
        self.relationship_type_name = relationship_type_name

    def set_type(self, relationship_type: str):
        self.type = relationship_type

    def add_interface(self, interface: InterfaceDefinition):
        self.interfaces.append(interface)

    def set_occurrences(self, occurrences: list):
        self.occurrences = occurrences


def requirement_definition_parser(name: str, data: dict) -> RequirementDefinition:
    requirement = RequirementDefinition(name)
    short_notation = True
    if data.get('capability'):
        short_notation = False
        requirement.set_capability(data.get('capability'))
    if data.get('node'):
        short_notation = False
        requirement.set_node(data.get('node'))
    if data.get('relationship'):
        short_notation = False
        relationship = data.get('relationship')
        if type(relationship) == str:
            requirement.set_relationship_type_name(relationship)
        else:
            if data.get('type'):
                requirement.set_type(data.get('type'))
            else:
                abort(400)
            if data.get('interfaces'):
                for interface_name, interface_value in data.get('interfaces').items():
                    requirement.add_interface(interface_definition_parser(interface_name, interface_value))
    if data.get('occurrences'):
        short_notation = False
        requirement.set_occurrences(data.get('occurrences'))
    if short_notation:
        requirement.set_capability(str(data))
    elif requirement.capability is None:
        abort(400)
    return requirement
