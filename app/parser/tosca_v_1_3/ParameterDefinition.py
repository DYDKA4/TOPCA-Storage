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
from app.parser.tosca_v_1_3.ConstraintСlause import Constraint, constraint_parser
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser


class Parameter:
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
        self.key_schema = None  # IDK what is it
        self.entry_schema = None  # IDK what is it

    def set_description(self, description: str):
        self.description = description

    def set_type(self, parameter_type: str):
        self.type = parameter_type

    def set_value(self, value: str):
        self.value = value

    def set_required(self, required: str):
        if required in {"false", "False", "0"}:
            self.required = False
        if required in {"true", "True", "1"}:
            self.required = True

    def set_default(self, default: str):
        self.default = default

    def set_status(self, status: str):
        self.default = status

    def add_constraints(self, constraint: Constraint):
        self.constraints.append(constraint)

    def set_key_schema(self, key_schema: str):
        self.key_schema = key_schema

    def set_entry_schema(self, entry_schema: str):
        self.entry_schema = entry_schema


def parameter_parser(parameter_name: str, data: dict) -> Parameter:
    if type(data) == str:
        return Parameter(parameter_name, str(data))
    parameter = Parameter(parameter_name)
    short_notation = True
    if data.get('type'):
        short_notation = False
        parameter.set_type(data.get('type'))
    if data.get('description'):
        short_notation = False
        description = description_parser(data)
        parameter.set_description(description)
    if data.get('value'):  # Data type?
        short_notation = False
        parameter.set_value(data.get('value'))
    if data.get('required'):
        short_notation = False
        parameter.set_value(data.get('required'))
    if data.get('default'):  # Data type?
        short_notation = False
        parameter.set_default(data.get('default'))
    if data.get('status'):
        short_notation = False
        parameter.set_status(data.get('status'))
    if data.get('constraints'):
        short_notation = False
        for constraint in data.get('constraints'):
            parameter.add_constraints(constraint_parser(constraint))
    if data.get('key_schema'):
        short_notation = False
        parameter.set_key_schema(data.get('key_schema'))
    if data.get('entry_schema'):
        short_notation = False
        parameter.set_entry_schema(data.get('entry_schema'))
    if short_notation:
        parameter.set_value(str(data))
    return parameter
