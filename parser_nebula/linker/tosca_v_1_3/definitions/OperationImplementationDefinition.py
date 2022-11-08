# Short notation for use with single artifact
# implementation: <primary_artifact_name>

# Short notation for use with multiple artifact
# implementation:
#   primary: <primary_artifact_name>
#   dependencies:
#     - <list_of_dependent_artifact_names>
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
import inspect

from parser_nebula.linker.GetAllArtifactDefinition import get_all_artifact_definition
from parser_nebula.linker.LinkByName import link_by_type_name
from parser_nebula.linker.LinkerValidTypes import link_members, link_with_list
from parser_nebula.parser import ParserException
from parser_nebula.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_operation_implementation_definition(service_template: ServiceTemplateDefinition,
                                             operation: OperationImplementationDefinition) -> None:
    list_of_artifact_definition = get_all_artifact_definition(service_template)
    if type(operation.primary) == str:
        link_by_type_name(list_of_artifact_definition, operation, 'primary')
    if operation.primary and type(operation.primary) != dict and type(operation.primary) != str:
        operation.primary = {'primary': [operation, operation.primary, {'type': 'definition'}]}
    if operation.dependencies and type(operation.dependencies[0]) == str:
        link_with_list(list_of_artifact_definition, operation, 'dependencies')
    elif operation.dependencies:
        operation.dependencies = {'dependencies': [operation, operation.dependencies, {'type': 'definition'}]}
    if str in {type(operation.primary)}:
        raise ParserException(400, inspect.stack()[0][3] + ':  str in {type(operation.primary)}')
