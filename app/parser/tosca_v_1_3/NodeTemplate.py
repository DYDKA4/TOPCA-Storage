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

from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser


class NodeTemplate:
    def __init__(self, name):
        self.description = None
        self.type = None
        self.name = name
        self.vid = None
        self.vertex_type_system = 'NodeTemplate'

    def set_type(self, node_type: str):
        self.type = node_type

    def set_description(self, description: str):
        self.description = description


def node_template_parser(name: str, data: dict) -> NodeTemplate:
    node_template = NodeTemplate(name)
    if data.get('type'):
        node_template.set_type(data.get('type'))
    else:
        abort(400)
    if data.get('description'):
        description = description_parser(data)
        node_template.set_description(description)

    return node_template
