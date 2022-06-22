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

from parser.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition, artifact_definition_parser
from parser.parser.tosca_v_1_3.assignments.AttributeAssignment import attribute_assignments_parser, AttributeAssignment
from parser.parser.tosca_v_1_3.assignments.CapabilityAssignment import CapabilityAssignment, capability_assignment_parser
from parser.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser.parser.tosca_v_1_3.others.Directives import Directives
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition, interface_definition_parser
from parser.parser.tosca_v_1_3.others.Metadata import Metadata
from parser.parser.tosca_v_1_3.definitions.NodeFilterDefinition import NodeFilterDefinition, node_filter_definition_parser
from parser.parser.tosca_v_1_3.assignments.PropertyAssignment import PropertyAssignment
from parser.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment, requirement_assignment_parser


class NodeTemplate:
    def __init__(self, name):
        self.description = None
        self.type = None
        self.name = name
        self.vid = None
        self.vertex_type_system = 'NodeTemplate'
        self.directives = []
        self.metadata = []
        self.properties = []
        self.attributes = []
        self.requirements = []
        self.capabilities = []
        self.interfaces = []
        self.artifacts = []
        self.node_filter = None
        self.copy = None

    def set_type(self, node_type: str):
        self.type = node_type

    def set_description(self, description: str):
        self.description = description

    def add_directives(self, directives: Directives):
        self.directives.append(directives)

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def add_property(self, property: PropertyAssignment):
        self.properties.append(property)

    def add_attributes(self, attribute: AttributeAssignment):
        self.attributes.append(attribute)

    def add_requirement(self, requirement: RequirementAssignment):
        self.requirements.append(requirement)

    def add_capability(self, capability: CapabilityAssignment):
        self.capabilities.append(capability)

    def add_interface(self, interface: InterfaceDefinition):
        self.interfaces.append(interface)

    def add_artifact(self, artifact: ArtifactDefinition):
        self.artifacts.append(artifact)

    def set_node_filter(self, node_filter: NodeFilterDefinition):
        self.node_filter = node_filter

    def set_copy(self, copy: str):
        self.copy = copy


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
        for directive in data.get('directives'):
            node_template.add_directives(Directives(directive))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata').items():
            node_template.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            node_template.add_property(PropertyAssignment(property_name, str(property_value)))
    if data.get('attributes'):
        for attributes_name, attributes_value in data.get('attributes').items():
            attribute = attribute_assignments_parser(attributes_name, attributes_value)
            node_template.add_attributes(attribute)
    if data.get('requirements'):
        for requirement in data.get('requirements'):
            for requirement_name, requirement_value in requirement.items():
                node_template.add_requirement(requirement_assignment_parser(requirement_name, requirement_value))
    if data.get('capabilities'):
        for capability_name, capability_value in data.get('capabilities').items():
            node_template.add_capability(capability_assignment_parser(capability_name, capability_value))
    if data.get('interfaces'):
        for interface_name, interface_value in data.get('interfaces').items():
            node_template.add_interface(interface_definition_parser(interface_name, interface_value))
    if data.get('artifacts'):
        for artifact_name, artifact_value in data.get('artifacts').items():
            node_template.add_artifact(artifact_definition_parser(artifact_name, artifact_value))
    if data.get('node_filter'):
        node_template.set_node_filter(node_filter_definition_parser(data.get('node_filter')))
    if data.get('copy'):
        node_template.set_copy(data.get('copy'))
    return node_template
