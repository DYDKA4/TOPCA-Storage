# Simple grammar (Capability Type only)
# <requirement_definition_name>: <capability_type_name> todo Linker

# Extended grammar (with Node and Relationship Types)
# <requirement_definition_name>:
#   capability: <capability_type_name> Required #todo Linker
#   node: <node_type_name> #todo Linker
#   relationship: <relationship_type_name> todo Linker
#   occurrences: [ <min_occurrences>, <max_occurrences> ]

# Extended grammar for declaring Property Definitions on the relationship’s Interfaces
# <requirement_definition_name>:
#   # Other keynames omitted for brevity
#   relationship:
#     type: # <relationship_type_name> Required todo Linker
#     interfaces:
#       <interface_definitions>
from werkzeug.exceptions import abort

from parser.linker.LinkByName import link_by_type_name
from parser.parser.tosca_v_1_3.definitions.RequirementDefinition import RequirementDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_requirement_definition(service_template: ServiceTemplateDefinition, requirement: RequirementDefinition) -> None:
    if type(requirement.capability) == str:
        link_by_type_name(service_template.capability_types, requirement, 'capability',)

    if type(requirement.node) == str:
        link_by_type_name(service_template.node_types, requirement, 'node')

    if type(requirement.capability) == str:
        link_by_type_name(service_template.relationship_types, requirement, 'relationship')
    if str in {type(requirement.node), type(requirement.relationship), type(requirement.capability)}:
        abort(400)
