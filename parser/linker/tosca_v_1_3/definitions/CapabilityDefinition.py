# Short notation
# <capability_definition_name>: <capability_type>

# Extended notation
# <capability_definition_name>:
#   type: # <capability_type> Required
#   description: <capability_description>
#   properties:
#     <property_definitions>
#   attributes:
#     <attribute_definitions>
#   valid_source_types: [ <node type_names> ]
#   occurrences : <range_of_occurrences>
from werkzeug.exceptions import abort

from parser.linker.LinkByName import link_by_type_name
from parser.linker.LinkerValidTypes import link_valid_source_types
from parser.parser.tosca_v_1_3.definitions.CapabilityDefinition import CapabilityDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_capability_definition(service_template: ServiceTemplateDefinition, capability: CapabilityDefinition) -> None:
    if type(capability.type) == str:
        link_by_type_name(service_template.artifact_types, capability, 'type',)
    link_valid_source_types(service_template.node_types, capability)
    if str in {type(capability.type)}:
        abort(400)
