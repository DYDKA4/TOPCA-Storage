# Short notation for use with single artifact
# implementation: <primary_artifact_name>

# Short notation for use with multiple artifact
# implementation:
#   primary: <primary_artifact_name> #todo Linker
#   dependencies:
#     - <list_of_dependent_artifact_names> #todo Linker
#   operation_host : SELF
#   timeout : 60

# Extended notation for use with single artifact
# implementation:
#   primary:
#     <primary_artifact_definition>
#   operation_host : HOST
#   timeout : 100

# Extended notation for use with multiple artifacts
# implementation:
#   primary:
#     <primary_artifact_definition>
#   dependencies:
#     - <list_of_dependent_artifact definitions>
#   operation_host: HOST
#   timeout: 120
from werkzeug.exceptions import abort

from parser.linker.GetAllArtifactDefinition import get_all_artifact_definition
from parser.linker.LinkByName import link_by_type_name
from parser.linker.LinkerValidTypes import link_members, link_with_list
from parser.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_operation_implementation_definition(service_template: ServiceTemplateDefinition,
                                             operation: OperationImplementationDefinition) -> None:
    list_of_artifact_definition = get_all_artifact_definition(service_template)
    if type(operation.primary) == str:
        link_by_type_name(list_of_artifact_definition, operation, 'primary')
    link_with_list(list_of_artifact_definition, operation, 'dependencies')
    if str in {type(operation.primary)}:
        abort(400)
