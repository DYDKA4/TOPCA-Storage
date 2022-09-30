# Extended

# <parameter_name>:
#   type: # <type> Required No
#   description: <parameter_description>
#   value: <parameter_value> | { <parameter_value_expression> } Required No #todo get_...
#   required: <parameter_required>
#   default: <parameter_default_value>
#   status: <status_value>
#   constraints:
#     - <parameter_constraints>
#   key_schema : <key_schema_definition>
#   entry_schema: <entry_schema_definition>

# Short
# <parameter_name>: <parameter_value>

# Single line
# <parameter_name>:
#     value : <parameter_value> | { <parameter_value_expression> }
import inspect

from parser.linker.LinkByName import link_by_type_name
from parser.parser import ParserException
from parser.parser.tosca_v_1_3.definitions import ParameterDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_parameter_definition(service_template: ServiceTemplateDefinition, parameter: ParameterDefinition) -> None:
    if type(parameter.type) == str:
        link_by_type_name(service_template.data_types, parameter, 'type')
    if str in {type(parameter.type)}:
        raise ParserException(400, inspect.stack()[0][3] + ':  str in {type(parameter.type)}')
