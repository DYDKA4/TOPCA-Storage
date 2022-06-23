# <node_type_name>:
#   derived_from: <parent_node_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <node_type_description>
#   attributes:
#     <attribute_definitions>
#   properties:
#     <property_definitions>
#   requirements:
#     - <requirement_definitions>
#   capabilities:
#     <capability_definitions>
#   interfaces:
#     <interface_definitions>
#   artifacts:
#     <artifact_definitions>
from werkzeug.exceptions import abort

from parser.linker.LinkDerivedFrom import link_derived_from
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.NodeType import NodeType


def link_node_type(service_template: ServiceTemplateDefinition,
                   node: NodeType) -> None:
    link_derived_from(service_template.node_types, node)
    if str in {type(node.derived_from)}:
        abort(400)
