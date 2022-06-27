# <node_template_name>:
#   type: # <node_type_name> REQUIRED
#   description: <node_template_description>
#   directives: [<directives>]
#   metadata:
#     <map of string>
#   properties:
#     <property_assignments>
#   attributes:
#     <attribute_assignments>
#   requirements:
#     - <requirement_assignments>
#   capabilities:
#     <capability_assignments>
#   interfaces:
#     <interface_definitions>
#   artifacts:
#     <artifact_definitions>
#   node_filter:
#     <node_filter_definition>
#   copy: <source_node_template_name>
from werkzeug.exceptions import abort

from parser.linker.LinkByName import link_by_type_name
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate


def link_node_template(service_template: ServiceTemplateDefinition,
                       node: NodeTemplate) -> None:
    topology_template: TemplateDefinition = service_template.topology_template
    link_by_type_name(service_template.node_types, node, 'type')
    link_by_type_name(topology_template.node_templates, node, 'copy')
    if str in {type(node.copy)}:
        abort(400)
