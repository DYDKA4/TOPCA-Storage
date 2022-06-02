# <data_type_name>:
#   derived_from: <existing_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <datatype_description>
#   constraints:
#     - <type_constraints>
#   properties:
#     <property_definitions>
#   key_schema : <key_schema_definition>
#   entry_schema: <entry_schema_definition>
from app.parser.tosca_v_1_3.ConstraintСlause import constraint_clause_parser, ConstraintClause
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.Metadata import Metadata
from app.parser.tosca_v_1_3.PropertyDefinition import PropertyDefinition, property_definition_parser
from app.parser.tosca_v_1_3.SchemaDefinition import SchemaDefinition, schema_definition_parser


class DataType:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'ArtifactType'
        self.name = name
        self.derived_from = None
        self.version = None
        self.metadata = []
        self.description = None
        self.constraints = []
        self.properties = []
        self.entry_schema = None
        self.key_schema = None

    def set_derived_from(self, derived_from: str):
        self.derived_from = derived_from

    def set_version(self, version: str):
        self.version = version

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def set_description(self, description: str):
        self.description = description

    def add_constraints(self, constraints: ConstraintClause):
        self.constraints.append(constraints)

    def add_property(self, properties: PropertyDefinition):
        self.properties.append(properties)

    def set_key_schema(self, key_schema: SchemaDefinition):
        self.key_schema = key_schema

    def set_entry_schema(self, entry_schema: SchemaDefinition):
        self.entry_schema = entry_schema


def data_type_parser(name: str, data: dict) -> DataType:
    data_type = DataType(name)
    if data.get('derived_from'):
        data_type.set_derived_from(data.get('derived_from'))
    if data.get('version'):
        data_type.set_version(data.get('version'))
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata'):
            data_type.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('description'):
        if data.get('description'):
            description = description_parser(data)
            data_type.set_description(description)
    if data.get('constraints'):
        for constraint in data.get('constraints'):
            data_type.add_constraints(constraint_clause_parser(constraint))
    if data.get('properties'):
        for property_name, property_value in data.get('inputs').items():
            data_type.add_property(property_definition_parser(property_name, property_value))
    if data.get('key_schema'):
        data_type.set_key_schema(schema_definition_parser(data.get('key_schema')))
    if data.get('entry_schema'):
        data_type.set_entry_schema(schema_definition_parser(data.get('entry_schema')))
    return data_type
