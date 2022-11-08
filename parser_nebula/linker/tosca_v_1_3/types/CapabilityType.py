# <capability_type_name>:
#   derived_from: <parent_capability_type_name>
#   version: <version_number>
#   description: <capability_description>
#   properties:
#     <property_definitions>
#   attributes:
#     <attribute_definitions>
#   valid_source_types: [ <node type_names> ] #todo Linker
import inspect

from parser_nebula.linker.LinkDerivedFrom import link_derived_from
from parser_nebula.linker.LinkerValidTypes import link_valid_source_types
from parser_nebula.parser import ParserException
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.CapabilityType import CapabilityType


def link_capability_type(service_template: ServiceTemplateDefinition,
                         capability: CapabilityType) -> None:
    link_derived_from(service_template.capability_types, capability)
    link_valid_source_types(service_template.node_types, capability)
    if str in {type(capability.derived_from)}:
        raise ParserException(400, inspect.stack()[0][3] + ':  str in {type(capability.derived_from)}')
