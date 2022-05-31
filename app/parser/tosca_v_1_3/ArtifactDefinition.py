# Short notation
# <artifact_name>: <artifact_file_URI>

# Extended notation:
# <artifact_name>:
#   description: <artifact_description>
#   type: # <artifact_type_name> Required
#   file: <artifact_file_URI> Required
#   repository: <artifact_repository_name>
#   deploy_path: <file_deployment_path>
#   version: <artifact _version>
#   checksum: <artifact_checksum>
#   checksum_algorithm: <artifact_checksum_algorithm>
#   properties: <property assignments>
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.PropertyAssignment import PropertyAssignment


class ArtifactDefinition:
    def __init__(self, name: str):
        self.name = name
        self.vid = None
        self.vertex_type_system = 'ArtifactDefinition'
        self.artifact_file_URI = None
        self.description = None
        self.type = None
        self.file = None
        self.repository = None
        self.deploy_path = None
        self.version = None
        self.checksum = None
        self.checksum_algorithm = None
        self.properties = []

    def set_artifact_file_uri(self, uri: str):
        self.artifact_file_URI = uri

    def set_description(self, description: str):
        self.description = description

    def set_type(self, artifact_type: str):
        self.type = artifact_type

    def set_file(self, file: str):
        self.file = file

    def set_repository(self, repository: str):
        self.repository = repository

    def set_deploy_path(self, deploy_path: str):
        self.deploy_path = deploy_path

    def set_version(self, version: str):
        self.version = version

    def set_checksum(self, checksum: str):
        self.checksum = checksum

    def set_checksum_algorithm(self, checksum_algorithm: str):
        self.checksum_algorithm = checksum_algorithm

    def add_properties(self, properties: PropertyAssignment):
        self.properties.append(properties)


def artifact_definition_parser(name: str, data: dict) -> ArtifactDefinition:
    artifact = ArtifactDefinition(name)
    short_notation = True
    if data.get('description'):
        short_notation = False
        description = description_parser(data)
        artifact.set_description(description)
    if data.get('type'):
        short_notation = False
        artifact.set_type(data.get('type'))
    if data.get('file'):
        short_notation = False
        artifact.set_file(data.get('file'))
    if data.get('repository'):
        short_notation = False
        artifact.set_repository(data.get('repository'))
    if data.get('deploy_path'):
        short_notation = False
        artifact.set_deploy_path(data.get('deploy_path'))
    if data.get('version'):
        short_notation = False
        artifact.set_version(data.get('version'))
    if data.get('checksum'):
        short_notation = False
        artifact.set_checksum(data.get('checksum'))
    if data.get('checksum_algorithm'):
        short_notation = False
        artifact.set_checksum_algorithm(data.get('checksum_algorithm'))
    if data.get('properties'):
        for property_name, property_value in data.get('properties').items():
            artifact.add_properties(PropertyAssignment(property_name, str(property_value)))
    if short_notation:
        artifact.set_artifact_file_uri(str(data))
    elif artifact.type is None:
        abort(400)
    elif artifact.file is None:
        abort(400)

    return artifact
