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

from app.parser.tosca_v_1_3.ArtifactType import ArtifactType, artifact_type_parser
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.ImportDefinition import ImportDefinition, import_definition_parser
from app.parser.tosca_v_1_3.RepositoryDefinition import RepositoryDefinition, repository_definition_parser
from app.parser.tosca_v_1_3.TemplateDefinition import TemplateDefinition, template_definition_parser


class ServiceTemplateDefinition:
    def __init__(self, cluster_name: str):
        self.tosca_definitions_version = None
        self.name = cluster_name
        self.template = None
        self.vid = None
        self.vertex_type_system = 'ServiceTemplateDefinition'
        self.namespace = None
        self.metadata = {
            'template_name': None,
            'template_author': None,
            'template_version': None
        }
        self.description = None
        self.dsl_definitions = None
        self.repositories = []
        self.imports = []
        self.artifact_types = []


    def set_tosca_definitions_version(self, tosca_definitions_version: str):
        self.tosca_definitions_version = tosca_definitions_version

    def set_namespace(self, namespace: str):
        self.namespace = namespace

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


def service_template_definition(cluster_name: str, data: dict) -> ServiceTemplateDefinition:
    service_template = ServiceTemplateDefinition(cluster_name)
    if data.get('tosca_definitions_version'):
        service_template.set_tosca_definitions_version(data.get('tosca_definitions_version'))
    else:
        abort(400)
    if data.get('namespace'):
        service_template.set_namespace(data.get('namespace'))
    if data.get('metadata'):
        metadata = data.get('metadata')
        for metadata_name in service_template.metadata.keys():
            if metadata.get(metadata_name):
                service_template.metadata[metadata_name] = metadata.get(metadata_name)
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            service_template.set_description(description)
    if data.get('dsl_definitions'):
        service_template.set_dsl_definitions(str(data.get('dsl_definitions')))
    if data.get('repositories'):
        for repository_name, repository_value in data.get('repositories'):
            service_template.add_repository(repository_definition_parser(repository_name, repository_value))
    if data.get('imports'):
        for import_value in data.get('imports'):
            service_template.add_import(import_definition_parser(import_value))
    if data.get('artifact_types'):
        for artifact_name, artifact_value in data.get('artifact_types').items():
            service_template.add_artifact_type(artifact_type_parser(artifact_name,artifact_value))
    if data.get('data_types'):
        for data_type_name, data_type_value in data.get('data_types').items():


    return service_template
