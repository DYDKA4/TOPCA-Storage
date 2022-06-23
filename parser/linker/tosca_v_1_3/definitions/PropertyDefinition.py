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

from parser.linker.LinkByName import link_by_type_name
from parser.parser.tosca_v_1_3.definitions.PropertyDefinition import PropertyDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.others.ConstraintСlause import constraint_clause_parser, ConstraintClause
from parser.parser.tosca_v_1_3.definitions.DescriptionDefinition import description_parser
from parser.parser.tosca_v_1_3.others.Metadata import Metadata
from parser.parser.tosca_v_1_3.definitions.SchemaDefinition import schema_definition_parser, SchemaDefinition


def link_property_definition(service_template: ServiceTemplateDefinition, property_vertex: PropertyDefinition) -> None:
    if type(property_vertex.type) == str:
        link_by_type_name(service_template.data_types, property_vertex, 'type')
    if str in {type(property_vertex.type)}:
        abort(400)
