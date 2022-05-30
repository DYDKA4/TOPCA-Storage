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
# todo requirements capabilities interfaces artifacts node_filter copy: <source_node_template_name>
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.AttributeAssignment import attribute_assignments_parser, AttributeAssignment
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.Metadata import Metadata
from app.parser.tosca_v_1_3.PropertyAssignment import PropertyAssignment


class NodeTemplate:
    def __init__(self, name):
        self.description = None
        self.type = None
        self.name = name
        self.vid = None
        self.vertex_type_system = 'NodeTemplate'
        self.directives = None  # IDK what is it
        self.metadata = []
        self.properties = []
        self.attributes = []

    def set_type(self, node_type: str):
        self.type = node_type

    def set_description(self, description: str):
        self.description = description

    def set_directives(self, directives: str):
        self.directives = directives

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def add_property(self, property: PropertyAssignment):
        self.properties.append(property)

    def add_attributes(self, attribute: AttributeAssignment):
        self.attributes.append(attribute)


def node_template_parser(name: str, data: dict) -> NodeTemplate:
    node_template = NodeTemplate(name)
    if data.get('type'):
        node_template.set_type(data.get('type'))
    else:
        abort(400)
    if data.get('description'):
        description = description_parser(data)
        node_template.set_description(description)
    if data.get('directives'):
        node_template.set_directives(data.get('directives'))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata'):
            node_template.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            node_template.add_property(PropertyAssignment(property_name, str(property_value)))
    if data.get('attributes'):
        for attributes_name, attributes_value in data.get('attributes').items():
            attribute = attribute_assignments_parser(attributes_name, attributes_value)
            node_template.add_attributes(attribute)

    # requirements:
    # capabilities:
    # interfaces:
    # artifacts:
    # node_filter:
    # copy: <source_node_template_name>
    # if data.get('')
    return node_template
