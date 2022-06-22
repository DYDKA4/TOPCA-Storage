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
from werkzeug.exceptions import abort

from parser.linker.LinkByName import link_by_type_name
from parser.linker.LinkerValidTypes import link_members
from parser.parser.tosca_v_1_3.assignments.AttributeAssignment import AttributeAssignment, attribute_assignments_parser
from parser.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser.parser.tosca_v_1_3.definitions.GroupDefinition import GroupDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.others.Metadata import Metadata
from parser.parser.tosca_v_1_3.assignments.PropertyAssignment import PropertyAssignment


def link_capability_definition(service_template: ServiceTemplateDefinition, group: GroupDefinition) -> None:
    if type(group.type) == str:
        link_by_type_name(service_template.artifact_types, group, 'type',)
    link_members(service_template.node_types, group)
    if str in {type(group.type)}:
        abort(400)

