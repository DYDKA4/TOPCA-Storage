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
from werkzeug.exceptions import abort

from parser.linker.GetAllArtifactDefinition import get_all_artifact_definition
from parser.linker.LinkByName import link_by_type_name
from parser.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition
from parser.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_operation_definition(service_template: ServiceTemplateDefinition,
                              operation: OperationDefinition) -> None:
    if type(operation.implementation) == str:
        list_of_artifact_definition = get_all_artifact_definition(service_template)
        link_by_type_name(list_of_artifact_definition, operation, 'implementation')
    if str in {type(operation.implementation)}:
        abort(400)
