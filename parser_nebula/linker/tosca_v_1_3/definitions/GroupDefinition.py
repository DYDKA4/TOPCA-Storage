# <group_name>:
#   type: # <group_type_name> Required
#   description: <group_description>
#   metadata:
#     <map of string>
#   attributes :
#     <attribute_assignments>
#   properties:
#     <property_assignments>
#   members: [ <list_of_node_templates> ]
import inspect

from parser_nebula.linker.LinkByName import link_by_type_name
from parser_nebula.linker.LinkerValidTypes import link_members
from parser_nebula.parser import ParserException
from parser_nebula.parser.tosca_v_1_3.assignments.AttributeAssignment import AttributeAssignment, attribute_assignments_parser
from parser_nebula.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser_nebula.parser.tosca_v_1_3.definitions.GroupDefinition import GroupDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.others.Metadata import Metadata
from parser_nebula.parser.tosca_v_1_3.assignments.PropertyAssignment import PropertyAssignment


def link_group_definition(service_template: ServiceTemplateDefinition, group: GroupDefinition) -> None:
    if type(group.type) == str:
        link_by_type_name(service_template.group_types, group, 'type',)
    link_members(service_template.topology_template.node_templates, group)
    if str in {type(group.type)}:
        raise ParserException(400, inspect.stack()[0][3] + ': str in {type(group.type)}')

