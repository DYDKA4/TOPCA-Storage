from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.ProperyDefinition import construct_property_definition, \
    find_property_definition_dependencies
from nebula_communication.template_builder.definition.SchemaDefinition import construct_schema_definition, \
    find_schema_definition_dependencies
from nebula_communication.template_builder.other.ConstraintClause import construct_constraint_schema
from parser.parser.tosca_v_1_3.types.DataType import DataType

DefaultDataTypes = {'string', 'boolean', 'integer', 'float', 'timestamp', 'scalar-unit.size',
                    'scalar-unit.frequency', 'map', 'list', 'range', 'version', 'scalar-unit.time'}


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
        if vertex_value['name'].as_string() not in DefaultDataTypes:
            result[vertex_value['name'].as_string()] = tmp_result

    return result


def find_data_type_dependencies(list_of_vid, result) -> dict:
    if result is None:
        result = {
            'ArtifactType': set(),
            'CapabilityType': set(),
            'DataType': set(),
            'GroupType': set(),
            'InterfaceType': set(),
            'NodeType': set(),
            'PolicyType': set(),
            'RelationshipType': set(),
        }
    data_type = DataType('name').__dict__
    for vid in list_of_vid:
        if vid not in result['DataType']:
            vertex_value = fetch_vertex(vid, 'DataType')
            vertex_value = vertex_value.as_map()
            vertex_keys = vertex_value.keys()
            if vertex_value['name'].as_string() not in DefaultDataTypes:

                edges = set(data_type.keys()) - set(vertex_keys) - {'vid'}
                for edge in edges:
                    destination = find_destination(vid, edge)
                    if edge == 'derived_from':
                        if destination:
                            if destination[0] not in result['DataType']:
                                dependencies = find_data_type_dependencies(destination, result)
                                for key, value in dependencies.items():
                                    print(key, value)
                                    result[key].union(value)
                                result['DataType'].add(destination[0])
                    elif edge == 'metadata':
                        continue
                    elif edge == 'properties':
                        dependencies = find_property_definition_dependencies(destination, result)
                        for key, value in dependencies.items():
                            result[key].union(value)
                    elif edge == 'constraints':
                        continue
                    elif edge == 'entry_schema':
                        dependencies = find_schema_definition_dependencies(destination, result)
                        for key, value in dependencies.items():
                            result[key].union(value)
                    elif edge == 'key_schema':
                        dependencies = find_schema_definition_dependencies(destination, result)
                        for key, value in dependencies.items():
                            result[key].union(value)
                    else:
                        abort(500)
    return result
