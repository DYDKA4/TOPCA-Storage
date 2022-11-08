# Extended

# <parameter_name>:
#   type: # <type> Required No
#   description: <parameter_description>
#   value: <parameter_value> | { <parameter_value_expression> } Required No
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

from parser_nebula.parser import ParserException
from parser_nebula.parser.tosca_v_1_3.others.ConstraintСlause import ConstraintClause, constraint_clause_parser
from parser_nebula.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
# complete
from parser_nebula.parser.tosca_v_1_3.definitions.SchemaDefinition import SchemaDefinition, schema_definition_parser


class ParameterDefinition:
    def __init__(self, name: str, value: str = None):
        self.name = name
        self.type = None
        self.vid = None
        self.vertex_type_system = 'ParameterDefinition'
        self.description = None
        self.value = value
        self.required = None
        self.default = None
        self.status = None
        self.constraints = []
        self.key_schema = None
        self.entry_schema = None

    def set_description(self, description: str):
        self.description = description

    def set_type(self, parameter_type: str):
        self.type = parameter_type

    def set_value(self, value: str):
        self.value = value

    def set_required(self, required: str):
        if {required}.union({"false", "False", 0, "0", False}):
            self.required = False
        elif {required}.union({"true", "True", 1, "1", True}):
            self.required = True

    def set_default(self, default: str):
        self.default = default

    def set_status(self, status: str):
        self.status = status

    def add_constraints(self, constraint: ConstraintClause):
        self.constraints.append(constraint)

    def set_key_schema(self, key_schema: SchemaDefinition):
        self.key_schema = key_schema

    def set_entry_schema(self, entry_schema: SchemaDefinition):
        self.entry_schema = entry_schema


def parameter_definition_parser(parameter_name: str, data: dict) -> ParameterDefinition:
    if type(data) == str:
        return ParameterDefinition(parameter_name, str(data))
    if len(data.keys()) == 1:
        if data.get('value'):
            return ParameterDefinition(parameter_name, data.get('value'))
        else:
            raise ParserException(400, inspect.stack()[0][3] + ': no_value')
    parameter = ParameterDefinition(parameter_name)
    if data.get('type'):
        parameter.set_type(data.get('type'))
    if data.get('description'):
        description = description_parser(data)
        parameter.set_description(description)
    if data.get('value'):  # Data type?
        parameter.set_value(data.get('value'))
    required = data.get('required')
    if required is not None:
        parameter.set_required(data.get('required'))
    if data.get('default'):  # todo Data type problem?
        parameter.set_default(data.get('default'))
    if data.get('status'):
        parameter.set_status(data.get('status'))
    if data.get('constraints'):
        for constraint in data.get('constraints'):
            parameter.add_constraints(constraint_clause_parser(constraint))
    if data.get('key_schema'):
        parameter.set_key_schema(schema_definition_parser(data.get('key_schema')))
    if data.get('entry_schema'):
        parameter.set_entry_schema(schema_definition_parser(data.get('entry_schema')))
    return parameter
