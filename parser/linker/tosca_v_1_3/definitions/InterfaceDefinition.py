# Extended notation for use in Type definitions
# <interface_definition_name>:
#   type: # <interface_type_name>
#   inputs:
#     <property_definitions>
#   operations:
#     <operation_definitions>
#   notifications:
#     <notification definitions>

# Extended notation for use in TemplateDefinition definitions
# <interface_definition_name>:
#   inputs:
#     <property_assignments>
#   operations:
#     <operation_definitions>
#   notifications:
#     <notification_definitions>
from werkzeug.exceptions import abort

from parser.linker.LinkByName import link_by_type_name
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_interface_definition(service_template: ServiceTemplateDefinition, interface: InterfaceDefinition) -> None:
    if type(interface.type) == str:
        link_by_type_name(service_template.artifact_types, interface, 'type',)
    if str in {type(interface.type)}:
        abort(400)
