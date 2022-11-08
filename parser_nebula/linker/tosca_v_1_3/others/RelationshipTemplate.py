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
import inspect

from parser_nebula.linker.LinkByName import link_by_type_name
from parser_nebula.parser import ParserException
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser_nebula.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate
from parser_nebula.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate


def link_relationship_template(service_template: ServiceTemplateDefinition,
                               relationship: RelationshipTemplate) -> None:
    topology_template: TemplateDefinition = service_template.topology_template
    link_by_type_name(service_template.relationship_types, relationship, 'type')
    link_by_type_name(topology_template.relationship_templates, relationship, 'copy')
    if str in {type(relationship.copy), type(relationship.type)}:
        raise ParserException(400, inspect.stack()[0][3] + ':  str in {type(relationship.copy), type('
                                                           'relationship.type)}')
