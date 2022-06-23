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
from werkzeug.exceptions import abort

from parser.linker.LinkDerivedFrom import link_derived_from
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.ArtifactType import ArtifactType


def link_artifact_type(service_template: ServiceTemplateDefinition,
                       artifact: ArtifactType) -> None:
    link_derived_from(service_template.artifact_types, artifact, )
    if str in {type(artifact.derived_from)}:
        abort(400)
