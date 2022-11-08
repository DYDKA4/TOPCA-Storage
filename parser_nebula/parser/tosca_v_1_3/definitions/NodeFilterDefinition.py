# node_filter:
#   properties:
#     - <property_filter_def_1>
#     - ...
#     - <property_filter_def_n>
#   capabilities:
#     - <capability_name_or_type_1>:
#         properties:
#           - <cap_1_property_filter_def_1>
#           - ...
#           - <cap_m_property_filter_def_n>
#     -  ...
#     - <capability_name_or_type_n>:
#         properties:
#           - <cap_1_property_filter_def_1>
#           - ...
#           - <cap_m_property_filter_def_n>
from parser_nebula.parser.tosca_v_1_3.definitions.CapabilityFilterDefinition import CapabilityFilterDefinition, \
    capability_filter_definition_parser
from parser_nebula.parser.tosca_v_1_3.definitions.PropertyFilterDefinition import PropertyFilterDefinition, \
    property_filter_definition_parser


class NodeFilterDefinition:
    def __init__(self):
        self.vid = None
        self.vertex_type_system = 'NodeFilterDefinition'
        self.properties = []
        self.capabilities = []

    def add_properties(self, properties: PropertyFilterDefinition):
        self.properties.append(properties)

    def add_capabilities(self, capability: CapabilityFilterDefinition):
        self.capabilities.append(capability)


def node_filter_definition_parser(data: dict) -> NodeFilterDefinition:
    node = NodeFilterDefinition()
    if data.get('properties'):
        for property_filter in data.get('properties'):
            for property_filter_name, property_filter_value in property_filter.items():
                node.add_properties(property_filter_definition_parser(property_filter_name, property_filter_value))
    if data.get('capabilities'):
        for capability in data.get('capabilities'):
            for capability_name, properties in capability.items():
                node.add_capabilities(capability_filter_definition_parser(capability_name, properties))
    return node
