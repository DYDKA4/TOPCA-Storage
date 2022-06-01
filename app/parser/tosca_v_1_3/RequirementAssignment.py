# short notation
# <requirement_name>: <node_template_name>

#  Extended notation
# <requirement_name>:
#   node: <node_template_name> | <node_type_name>
#   relationship: <relationship_template_name> | <relationship_type_name>
#   capability: <capability_symbolic_name> | <capability_type_name>
#   node_filter:
#     <node_filter_definition>
#   occurrences: [ min_occurrences, max_occurrences ]

# with Property Assignments for the relationship’s Interfaces
# <requirement_name>:
#   # Other keynames omitted for brevity
#   relationship:
#     type: # <relationship_template_name> | <relationship_type_name>
#     properties:
#       <property_assignments>
#     interfaces:
#       <interface_assignments>
from app.parser.tosca_v_1_3.InterfaceDefinition import InterfaceDefinition, interface_definition_parser
from app.parser.tosca_v_1_3.NodeFilterDefinition import NodeFilterDefinition, node_filter_definition_parser
from app.parser.tosca_v_1_3.PropertyAssignment import PropertyAssignment


class RequirementAssignment:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.vertex_type_system = 'RequirementAssignment'
        self.node = None
        self.relationship = None
        self.relationship_complex = None
        self.properties = []
        self.interfaces = []
        self.capability = None
        self.node_filter = None
        self.occurrences = []

    def set_node(self, node: str):
        self.node = node

    def set_relationship(self, relationship: str):
        self.relationship = relationship

    def set_relationship_complex(self, relationship: str):
        self.relationship_complex = relationship

    def add_property(self, property: PropertyAssignment):
        self.properties.append(property)

    def add_interface(self, interface: InterfaceDefinition):
        self.properties.append(interface)

    def set_capability(self, capability: str):
        self.capability = capability

    def set_node_filter(self, node_filter: NodeFilterDefinition):
        self.node_filter = node_filter

    def set_occurrences(self, occurrences: list):
        self.occurrences = occurrences


def requirement_parser(name: str, data: dict) -> RequirementAssignment:
    requirement = RequirementAssignment(name)
    short_notation = True
    if data.get('node'):
        short_notation = False
        requirement.set_node(data.get('node'))
    if data.get('relationship'):
        short_notation = False
        if type(data.get('relationship')) == str:
            requirement.set_relationship(data.get('relationship'))
        else:
            relationship_data = data.get('relationship')
            if relationship_data.get('type'):
                requirement.set_relationship_complex(relationship_data.get('type'))
            if relationship_data.get('properties'):
                for property_name, property_value in data.get('properties').items():
                    requirement.add_property(PropertyAssignment(property_name, str(property_value)))
            if relationship_data.get('interfaces'):
                for interface_name, interface_value in data.get('interfaces').items():
                    requirement.add_interface(interface_definition_parser(interface_name, interface_value))
    if data.get('capability'):
        short_notation = False
        requirement.set_capability(data.get('capability'))
    if data.get('node_filter'):
        short_notation = False
        requirement.set_node_filter(node_filter_definition_parser(data.get('node_filter')))
    if data.get('occurrences'):
        short_notation = False
        requirement.set_occurrences(data.get('occurrences'))
    if short_notation:
        requirement.set_node(str(data))
    return requirement
