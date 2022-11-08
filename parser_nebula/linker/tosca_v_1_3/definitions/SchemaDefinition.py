from parser_nebula.linker.LinkByName import link_by_type_name
from parser_nebula.parser.tosca_v_1_3.definitions.SchemaDefinition import SchemaDefinition
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition


def link_schema_definition(service_template: ServiceTemplateDefinition, schema: SchemaDefinition) -> None:
    if type(schema.type) == str:
        link_by_type_name(service_template.data_types, schema, 'type',)
    if schema.entry_schema:
        link_schema_definition(service_template, schema.entry_schema)
    if schema.key_schema:
        link_schema_definition(service_template, schema.key_schema)
