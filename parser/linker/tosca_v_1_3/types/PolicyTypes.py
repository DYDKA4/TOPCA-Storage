# <policy_type_name>:
#   derived_from: <parent_policy_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <policy_description>
#   properties:
#     <property_definitions>
#   targets: [ <list_of_valid_target_types> ]
#   triggers:
#     <trigger_definitions>
from werkzeug.exceptions import abort

from parser.linker.LinkDerivedFrom import link_derived_from
from parser.linker.LinkerValidTypes import link_members, link_with_list
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.PolicyTypes import PolicyType


def link_policy_type(service_template: ServiceTemplateDefinition,
                     policy: PolicyType) -> None:
    link_derived_from(service_template.policy_types, policy)
    link_with_list(service_template.node_types + service_template.group_types, policy, 'target')
    if str in {type(policy.derived_from)}:
        abort(400)
