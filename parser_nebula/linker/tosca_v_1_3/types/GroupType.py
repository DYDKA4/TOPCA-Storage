# <group_type_name>:
#   derived_from: <parent_group_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <group_description>
#   attributes :
#     <attribute_definitions>
#   properties:
#     <property_definitions>
#   members: [ <list_of_valid_member_types> ]
import inspect

from parser_nebula.linker.LinkDerivedFrom import link_derived_from
from parser_nebula.linker.LinkerValidTypes import link_members
from parser_nebula.parser import ParserException
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.GroupType import GroupType


def link_group_type(service_template: ServiceTemplateDefinition,
                    group: GroupType) -> None:
    link_derived_from(service_template.group_types, group)
    link_members(service_template.node_types, group)
    if str in {type(group.derived_from)}:
        raise ParserException(400, inspect.stack()[0][3] + ':  str in {type(group.derived_from)}')
