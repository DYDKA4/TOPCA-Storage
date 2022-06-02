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
from app.parser.tosca_v_1_3.ArtifactDefinition import ArtifactDefinition, artifact_definition_parser
from app.parser.tosca_v_1_3.AttributeDefinition import AttributeDefinition, attribute_definition_parser
from app.parser.tosca_v_1_3.CapabilityDefinition import CapabilityDefinition, capability_definition_parser
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.InterfaceDefinition import InterfaceDefinition, interface_definition_parser
from app.parser.tosca_v_1_3.Metadata import Metadata
from app.parser.tosca_v_1_3.PropertyDefinition import PropertyDefinition, property_definition_parser
from app.parser.tosca_v_1_3.RequirementDefinition import RequirementDefinition, requirement_definition_parser


class NodeType:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'NodeType'
        self.name = name
        self.derived_from = None
        self.version = None
        self.metadata = []
        self.description = None
        self.properties = []
        self.attributes = []
        self.requirements = []
        self.interfaces = []
        self.capabilities = []
        self.artifacts = []

    def set_derived_from(self, derived_from: str):
        self.derived_from = derived_from

    def set_version(self, version: str):
        self.version = version

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def set_description(self, description: str):
        self.description = description

    def add_property(self, properties: PropertyDefinition):
        self.properties.append(properties)

    def add_attribute(self, attribute: AttributeDefinition):
        self.attributes.append(attribute)

    def add_requirements(self, requirements: RequirementDefinition):
        self.requirements.append(requirements)

    def add_capability(self, capability: CapabilityDefinition):
        self.capabilities.append(capability)

    def add_interface(self, interface: InterfaceDefinition):
        self.interfaces.append(interface)

    def add_artifact(self, artifact: ArtifactDefinition):
        self.artifacts.append(artifact)


def node_type_parser(name: str, data: dict) -> NodeType:
    node = NodeType(name)
    if data.get('derived_from'):
        node.set_derived_from(data.get('derived_from'))
    if data.get('version'):
        node.set_version(data.get('version'))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata'):
            node.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            node.set_description(description)
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            node.add_property(property_definition_parser(property_name, property_value))
    if data.get('attributes'):
        for attribute_name, attribute_value in data.get('attributes').items():
            node.add_attribute(attribute_definition_parser(attribute_name, attribute_value))
    if data.get('requirements'):
        for requirement in data.get('requirements'):
            for requirement_name, requirements_value in requirement.items():
                node.add_requirements(requirement_definition_parser(requirement_name, requirements_value))
    if data.get('capabilities'):
        for capability_name, capability_value in data.get('capabilities'):
            node.add_capability(capability_definition_parser(capability_name, capability_value))
    if data.get('interfaces'):
        for interface_name, interface_value in data.get('interface').items():
            node.add_interface(interface_definition_parser(interface_name, interface_value))
    if data.get('artifacts'):
        for artifact_name, artifact_value in data.get('artifacts').items():
            node.add_artifact(artifact_definition_parser(artifact_name, artifact_value))
    return node
