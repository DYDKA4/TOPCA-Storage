# <schema_definition>:
#   type: # <schema_type> Required
#   description: <schema_description>
#   constraints:
#     - <schema_constraints>
#   key_schema : <key_schema_definition>
#   entry_schema: <entry_schema_definition>
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.others.ConstraintСlause import constraint_clause_parser, ConstraintClause
from app.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser


class SchemaDefinition:
    def __init__(self):
        self.description = None
        self.type = None
        self.vid = None
        self.type = None
        self.constraints = []
        self.key_schema = None
        self.entry_schema = None

    def set_type(self, schema_type: str):
        self.type = schema_type

    def set_description(self, description: str):
        self.description = description

    def add_constraints(self, constraint: ConstraintClause):
        self.constraints.append(constraint)

    def set_key_schema(self, schema):
        self.key_schema = schema

    def set_entry_schema(self, schema):
        self.entry_schema = schema


def schema_definition_parser(data: dict) -> SchemaDefinition:
    schema = SchemaDefinition()
    if data.get('type'):
        schema.set_type('type')
    else:
        abort(400)
    if data.get('description'):
        description = description_parser(data)
        schema.set_description(description)
    if data.get('constraints'):
        for constraint in data.get('constraints'):
            schema.add_constraints(constraint_clause_parser(constraint))
    if data.get('key_schema'):
        schema.set_key_schema(schema_definition_parser(data.get('key_schema')))
    if data.get('entry_schema'):
        schema.set_entry_schema(schema_definition_parser(data.get('entry_schema')))
    return schema
