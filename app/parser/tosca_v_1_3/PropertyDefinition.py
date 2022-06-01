# <property_name>:
#   type: # <property_type> Required
#   description: <property_description>
#   required: <property_required>
#   default: <default_value>
#   status: <status_value>
#   constraints:
#     - <property_constraints>
#   key_schema : <key_schema_definition>
#   entry_schema: <entry_schema_definition>
#   metadata:
#     <metadata_map>
from werkzeug.exceptions import abort

from app.parser.tosca_v_1_3.ConstraintСlause import constraint_clause_parser
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.Metadata import Metadata
from app.parser.tosca_v_1_3.SchemaDefinition import schema_definition_parser, SchemaDefinition


class PropertyDefinition:
    def __init__(self, name: str):
        self.entry_schema = None
        self.key_schema = None
        self.name = name
        self.vid = None
        self.vertex_type_system = 'PropertyDefinition'
        self.type = None
        self.description = None
        self.required = None
        self.default = None
        self.status = None
        self.constraints = []
        self.metadata = []

    def set_type(self, property_type: str):
        self.type = property_type

    def set_description(self, description: str):
        self.description = description

    def set_required(self, required: str):
        if required in {"false", "False", "0"}:
            self.required = False
        if required in {"true", "True", "1"}:
            self.required = True

    def set_default(self, default: str):
        self.default = default

    def set_status(self, status: str):
        self.status = status

    def add_constraints(self, constraint):
        self.constraints.append(constraint)

    def set_key_schema(self, key_schema: SchemaDefinition):
        self.key_schema = key_schema

    def set_entry_schema(self, entry_schema: SchemaDefinition):
        self.entry_schema = entry_schema

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)


def property_definition_parser(name: str, data: dict) -> PropertyDefinition:
    property_definition = PropertyDefinition(name)
    if data.get('type'):
        property_definition.set_type(data.get('type'))
    else:
        abort(400)
    if data.get('description'):
        description = description_parser(data)
        property_definition.set_description(description)
    if data.get('required'):
        property_definition.set_required(data.get('required'))
    if data.get('default'):  # Data type?
        property_definition.set_default(data.get('default'))
    if data.get('status'):
        property_definition.set_status(data.get('status'))
    if data.get('constraints'):
        for constraint in data.get('constraints'):
            property_definition.add_constraints(constraint_clause_parser(constraint))
    if data.get('key_schema'):
        property_definition.set_key_schema(schema_definition_parser(data.get('key_schema')))
    if data.get('entry_schema'):
        property_definition.set_entry_schema(schema_definition_parser(data.get('entry_schema')))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata'):
            property_definition.add_metadata(Metadata(metadata_name, metadata_value))
    return property_definition
