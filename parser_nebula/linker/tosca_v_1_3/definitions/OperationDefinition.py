# Short notation
# <operation_name>: <implementation_artifact_name> #todo linker

# Extended notation for use in Type definitions
# <operation_name>:
#    description: <operation_description>
#    implementation: <Operation implementation definition>
#    inputs:
#      <property_definitions>
#    outputs: WRONG?
#       <interface mappings>

# Extended notation for use in TemplateDefinition definitions
# <operation_name>:
#    description: <operation_description>
#    implementation: <Operation implementation definition>
#    inputs:
#      <property_assignments>
import inspect

from parser_nebula.linker.GetAllArtifactDefinition import get_all_artifact_definition
from parser_nebula.linker.LinkByName import link_by_type_name
from parser_nebula.parser import ParserException
from parser_nebula.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_operation_definition(service_template: ServiceTemplateDefinition,
                              operation: OperationDefinition) -> None:
    if type(operation.implementation) == str:
        list_of_artifact_definition = get_all_artifact_definition(service_template)
        link_by_type_name(list_of_artifact_definition, operation, 'implementation')
    if str in {type(operation.implementation)}:
        raise ParserException(400, inspect.stack()[0][3] + ': str in {type(operation.implementation)}')
