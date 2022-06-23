# <interface_type_name>:
#   derived_from: <parent_interface_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <interface_description>
#   inputs:
#     <property_definitions>
#   operations:
#     <operation_definitions>
#   notifications:
#     <notification definitions>
from werkzeug.exceptions import abort

from parser.linker.LinkDerivedFrom import link_derived_from
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.InterfaceType import InterfaceType


def link_interface_type(service_template: ServiceTemplateDefinition,
                        interface: InterfaceType) -> None:
    link_derived_from(service_template.interface_types, interface)
    if str in {type(interface.derived_from)}:
        abort(400)
