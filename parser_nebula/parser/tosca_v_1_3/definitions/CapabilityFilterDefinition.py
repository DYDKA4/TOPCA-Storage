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
from parser_nebula.parser.tosca_v_1_3.definitions.PropertyFilterDefinition import PropertyFilterDefinition, \
    property_filter_definition_parser


class CapabilityFilterDefinition:
    def __init__(self, name: str):
        self.vid = None
        self.name = name
        self.vertex_type_system = 'CapabilityFilterDefinition'
        self.properties = []

    def add_properties(self, properties: PropertyFilterDefinition):
        self.properties.append(properties)


def capability_filter_definition_parser(name: str, data: dict) -> CapabilityFilterDefinition:
    capability = CapabilityFilterDefinition(name)
    if data.get('properties'):
        for property_filter in data.get('properties'):
            for property_filter_name, property_filter_value in property_filter.items():
                capability.add_properties(
                    property_filter_definition_parser(property_filter_name, property_filter_value))

    return capability
