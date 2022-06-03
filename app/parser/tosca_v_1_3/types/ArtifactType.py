# <artifact_type_name>:
#   derived_from: <parent_artifact_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <artifact_description>
#   mime_type: <mime_type_string>
#   file_ext: [ <file_extensions> ]
#   properties:
#     <property_definitions>
from app.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.others.Metadata import Metadata
from app.parser.tosca_v_1_3.definitions.PropertyDefinition import property_definition_parser, PropertyDefinition


class ArtifactType:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'ArtifactType'
        self.name = name
        self.derived_from = None
        self.version = None
        self.metadata = []
        self.description = None
        self.mime_type = None
        self.file_ext = []
        self.properties = []

    def set_derived_from(self, derived_from: str):
        self.derived_from = derived_from

    def set_version(self, version: str):
        self.version = version

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def set_description(self, description: str):
        self.description = description

    def set_mime_type(self, mime_type: str):
        self.mime_type = mime_type

    def add_file_ext(self, file_ext: str):
        self.file_ext.append(file_ext)

    def add_property(self, properties: PropertyDefinition):
        self.properties.append(properties)


def artifact_type_parser(name: str, data: dict) -> ArtifactType:
    artifact = ArtifactType(name)
    if data.get('derived_from'):
        artifact.set_derived_from(data.get('derived_from'))
    if data.get('version'):
        artifact.set_version(data.get('version'))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata'):
            artifact.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            artifact.set_description(description)
    if data.get('mime_type'):
        artifact.set_mime_type(data.get('mime_type'))
    if data.get('file_ext'):
        for file_ext in data.get('file_ext'):
            artifact.add_file_ext(file_ext)
    if data.get('properties'):
        for property_name, property_value in data.get('inputs').items():
            artifact.add_property(property_definition_parser(property_name, property_value))
    return artifact
