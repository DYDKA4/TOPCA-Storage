from werkzeug.exceptions import abort

from parser.linker.LinkByName import link_by_type_name
from parser.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_artifact_definition(service_template: ServiceTemplateDefinition, artifact: ArtifactDefinition) -> None:
    if type(artifact.type) == str:
        link_by_type_name(service_template.artifact_types, artifact, 'type',)
    if str in {type(artifact.type)}:
        abort(400)
