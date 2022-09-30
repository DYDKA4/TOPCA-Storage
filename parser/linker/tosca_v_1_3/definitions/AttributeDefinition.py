import inspect

from parser.linker.LinkByName import link_by_type_name
from parser.parser import ParserException
from parser.parser.tosca_v_1_3.definitions.AttributeDefinition import AttributeDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_attribute_definition(service_template: ServiceTemplateDefinition, attribute: AttributeDefinition) -> None:
    if type(attribute.type) == str:
        link_by_type_name(service_template.data_types, attribute, 'type',)
    if str in {type(attribute.type)}:
        raise ParserException(400, inspect.stack()[0][3] + ':  str in {type(attribute.type)}')
