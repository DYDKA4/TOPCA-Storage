# # Required TOSCA Definitions version string
# tosca_definitions_version: < value >  # Required, see section 3.1 for usage
# namespace: < URI >  # Optional, see section 3.2 for usage
# # Optional metadata keyname: value pairs
# metadata:
# template_name: < value >  # Optional, name of this service template
# template_author: < value >  # Optional, author of this service template
# template_version: < value >  # Optional, version of this service template
# #  More optional entries of domain or profile specific metadata keynames
# # Optional description of the definitions inside the file.
# description: < template_type_description >
# dsl_definitions: #todo Make support for it?
# # map of YAML alias anchors (or macros)
# repositories:
# # map of external repository definitions which host TOSCA artifacts
# imports:
# # ordered list of import definitions
# artifact_types:
# # map of artifact type definitions
# data_types:
# # map of datatype definitions
# capability_types:
# # map of capability type definitions
# interface_types
# # map of interface type definitions
# relationship_types:
# # map of relationship type definitions
# node_types:
# # map of node type definitions
# group_types:
# # map of group type definitions
# policy_types:
# # map of policy type definitions
# topology_template:
# # topology template definition of the cloud application or service
from werkzeug.exceptions import abort

from parser.parser.tosca_v_1_3.others.Metadata import Metadata
from parser.parser.tosca_v_1_3.types.ArtifactType import ArtifactType, artifact_type_parser
from parser.parser.tosca_v_1_3.types.CapabilityType import CapabilityType, capability_type_parser
from parser.parser.tosca_v_1_3.types.DataType import DataType, data_type_parser
from parser.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser.parser.tosca_v_1_3.types.GroupType import group_type_parser, GroupType
from parser.parser.tosca_v_1_3.definitions.ImportDefinition import ImportDefinition, import_definition_parser
from parser.parser.tosca_v_1_3.types.InterfaceType import InterfaceType, interface_type_parser
from parser.parser.tosca_v_1_3.types.NodeType import node_type_parser, NodeType
from parser.parser.tosca_v_1_3.types.PolicyTypes import policy_type_parser, PolicyType
from parser.parser.tosca_v_1_3.types.RelationshipType import relationship_type_parser, RelationshipType
from parser.parser.tosca_v_1_3.definitions.RepositoryDefinition import RepositoryDefinition, \
    repository_definition_parser
from parser.parser.tosca_v_1_3.definitions.TemplateDefinition import TemplateDefinition, template_definition_parser


class ServiceTemplateDefinition:
    def __init__(self, cluster_name: str):
        self.tosca_definitions_version = None
        self.name = cluster_name
        self.vid = '"' + cluster_name + '"'
        self.vertex_type_system = 'ServiceTemplateDefinition'
        self.namespace = None
        self.metadata = []
        self.description = None
        self.dsl_definitions = None
        self.repositories = []
        self.imports = []
        self.artifact_types = []
        self.data_types = [DataType('string'), DataType('boolean'), DataType('float'), DataType('integer'),
                           DataType('timestamp'), DataType('scalar-unit.size'), DataType('scalar-unit.frequency'), DataType('map'),
                           DataType('list'), DataType('range'), DataType('version')]
        self.capability_types = []
        self.interface_types = []
        self.relationship_types = []
        self.node_types = []
        self.group_types = []
        self.policy_types = []
        self.topology_template = None
        self.template_type = None

    def set_tosca_definitions_version(self, tosca_definitions_version: str):
        self.tosca_definitions_version = tosca_definitions_version

    def set_namespace(self, namespace: str):
        self.namespace = namespace

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def set_description(self, description: str):
        self.description = description

    def set_dsl_definitions(self, dsl_definitions: str):
        self.dsl_definitions = dsl_definitions

    def add_repository(self, repository: RepositoryDefinition):
        self.repositories.append(repository)

    def add_import(self, imports: ImportDefinition):
        self.imports.append(imports)

    def add_artifact_type(self, artifact_type: ArtifactType):
        self.artifact_types.append(artifact_type)

    def add_data_type(self, data_type: DataType):
        self.data_types.append(data_type)

    def add_capability_type(self, capability_type: CapabilityType):
        self.capability_types.append(capability_type)

    def add_interface_types(self, interface_types: InterfaceType):
        self.interface_types.append(interface_types)

    def add_relationship_type(self, relationship_type: RelationshipType):
        self.relationship_types.append(relationship_type)

    def add_node_type(self, node_type: NodeType):
        self.node_types.append(node_type)

    def add_group_type(self, group_type: GroupType):
        self.group_types.append(group_type)

    def add_policy_type(self, policy_type: PolicyType):
        self.policy_types.append(policy_type)

    def set_template_definition(self, template: TemplateDefinition):
        self.topology_template = template


def service_template_definition_parser(cluster_name: str, data: dict) -> ServiceTemplateDefinition:
    service_template = ServiceTemplateDefinition(cluster_name)
    if data.get('tosca_definitions_version'):
        service_template.set_tosca_definitions_version(data.get('tosca_definitions_version'))
    else:
        abort(400)
    if data.get('namespace'):
        service_template.set_namespace(data.get('namespace'))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata').items():
            service_template.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            service_template.set_description(description)
    if data.get('dsl_definitions'):
        service_template.set_dsl_definitions(str(data.get('dsl_definitions')))
    if data.get('repositories'):
        for repository_name, repository_value in data.get('repositories').items():
            service_template.add_repository(repository_definition_parser(repository_name, repository_value))
    if data.get('imports'):
        for import_value in data.get('imports'):
            service_template.add_import(import_definition_parser(import_value))
    if data.get('artifact_types'):
        for artifact_name, artifact_value in data.get('artifact_types').items():
            service_template.add_artifact_type(artifact_type_parser(artifact_name, artifact_value))
    if data.get('data_types'):
        for data_type_name, data_type_value in data.get('data_types').items():
            service_template.add_data_type(data_type_parser(data_type_name, data_type_value))
    if data.get('capability_types'):
        for capability_type_name, capability_type_value in data.get('capability_types').items():
            service_template.add_capability_type(capability_type_parser(capability_type_name, capability_type_value))
    if data.get('interface_types'):
        for interface_type_name, interface_type_value in data.get('interface_types').items():
            service_template.add_interface_types(interface_type_parser(interface_type_name, interface_type_value))
    if data.get('relationship_types'):
        for relationship_name, relationship_value in data.get('relationship_types').items():
            service_template.add_relationship_type(relationship_type_parser(relationship_name, relationship_value))
    if data.get('node_types'):
        for node_type_name, node_type_value in data.get('node_types').items():
            service_template.add_node_type(node_type_parser(node_type_name, node_type_value))
    if data.get('group_types'):
        for group_type_name, group_type_value in data.get('group_types').items():
            service_template.add_group_type(group_type_parser(group_type_name, group_type_value))
    if data.get('policy_types'):
        for policy_type_name, policy_type_value, in data.get('policy_types').items():
            service_template.add_policy_type(policy_type_parser(policy_type_name, policy_type_value))
    service_template.set_template_definition(template_definition_parser(data))
    return service_template
