# <policy_name>:
#   type: # <policy_type_name> Required
#   description: <policy_description>
#   metadata:
#     <map of string>
#   properties:
#     <property_assignments>
#   targets: [<list_of_policy_targets>]
#   triggers:
#     <trigger_definitions>
import copy
import inspect

from parser.linker.LinkByName import link_by_type_name
from parser.linker.LinkerValidTypes import link_with_list
from parser.parser import ParserException
from parser.parser.tosca_v_1_3.definitions.PolicyDefinition import PolicyDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition


def link_policy_definition(service_template: ServiceTemplateDefinition, policy: PolicyDefinition) -> None:
    if type(policy.type) == str:
        link_by_type_name(service_template.policy_types, policy, 'type')
    array_to_find = copy.deepcopy(service_template.group_types)
    topology_template: TemplateDefinition = service_template.topology_template
    if topology_template:
        array_to_find += topology_template.groups
        array_to_find += topology_template.node_templates
    link_with_list(array_to_find, policy, 'targets')
    if str in {type(policy.type)}:
        raise ParserException(400, inspect.stack()[0][3] + ':  str in {type(policy.type)}')
