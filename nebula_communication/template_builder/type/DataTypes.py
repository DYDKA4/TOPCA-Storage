from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.ProperyDefinition import construct_property_definition
from nebula_communication.template_builder.definition.SchemaDefinition import construct_schema_definition
from nebula_communication.template_builder.other.ConstraintClause import construct_constraint_schema
from parser.parser.tosca_v_1_3.types.DataType import DataType


def construct_data_type(list_of_vid) -> dict:
    result = {}
    data_type = DataType('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'DataType')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(data_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'derived_from':
                if destination:
                    derived_from = fetch_vertex(destination[0], 'DataType')
                    derived_from = derived_from.as_map()
                    derived_from = derived_from['name'].as_string()
                    tmp_result['derived_from'] = derived_from
            elif edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            elif edge == 'properties':
                tmp_result['properties'] = construct_property_definition(destination)
            elif edge == 'constraints':
                tmp_result['constraints'] = construct_constraint_schema(destination)
            elif edge == 'entry_schema':
                tmp_result['entry_schema'] = construct_schema_definition(destination)
            elif edge == 'key_schema':
                tmp_result['key_schema'] = construct_schema_definition(destination)
            else:
                abort(500)
        if vertex_value['name'].as_string() not in {'string', 'boolean', 'integer', 'float', 'timestamp', 'scalar-unit.size',
                                                    'scalar-unit.frequency', 'map', 'list', 'range', 'version'}:
            result[vertex_value['name'].as_string()] = tmp_result

    return result
