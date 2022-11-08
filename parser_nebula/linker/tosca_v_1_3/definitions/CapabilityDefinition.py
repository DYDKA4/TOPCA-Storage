import inspect

from parser_nebula.linker.LinkByName import link_by_type_name
from parser_nebula.linker.LinkerValidTypes import link_valid_source_types
from parser_nebula.parser import ParserException
from parser_nebula.parser.tosca_v_1_3.definitions.CapabilityDefinition import CapabilityDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_capability_definition(service_template: ServiceTemplateDefinition, capability: CapabilityDefinition) -> None:
    if type(capability.type) == str:
        link_by_type_name(service_template.capability_types, capability, 'type',)
    link_valid_source_types(service_template.node_types, capability)
    if str in {type(capability.type)}:
        raise ParserException(400, inspect.stack()[0][3] + ':  str in {type(capability.type)}')
