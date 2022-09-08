from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.SchemaDefinition import construct_schema_definition, \
    find_schema_definition_dependencies
from nebula_communication.template_builder.other.ConstraintClause import construct_constraint_schema
from parser.parser.tosca_v_1_3.definitions.PropertyDefinition import PropertyDefinition


def construct_property_definition(list_of_vid) -> dict:
    result = {}

    property_definition = PropertyDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'PropertyDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_value.keys():
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                value = vertex_value[vertex_key].as_string()
                if value == 'True':
                    value = True
                elif value == 'False':
                    value = False

                tmp_result[vertex_key] = value
        edges = set(property_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'entry_schema':
                tmp_result['entry_schema'] = construct_schema_definition(destination)
            elif edge == 'key_schema':
                tmp_result['key_schema'] = construct_schema_definition(destination)
            elif edge == 'type':
                data_type = fetch_vertex(destination[0], 'DataType')
                data_type = data_type.as_map()
                data_type = data_type['name'].as_string()
                tmp_result['type'] = data_type
            elif edge == 'constraints':
                tmp_result['constraints'] = construct_constraint_schema(destination)
            elif edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            else:
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result
    return result


def find_property_definition_dependencies(list_of_vid) -> dict:
    from nebula_communication.template_builder.type.DataTypes import DefaultDataTypes, find_data_type_dependencies
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
    property_definition = PropertyDefinition('name').__dict__
    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'PropertyDefinition')
        vertex_value = vertex_value.as_map()
        vertex_keys = vertex_value.keys()
        edges = set(property_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'entry_schema':
                dependencies = find_schema_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'key_schema':
                dependencies = find_schema_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'type':
                data_type = fetch_vertex(destination[0], 'DataType')
                data_type = data_type.as_map()
                data_type = data_type['name'].as_string()
                if data_type not in DefaultDataTypes:
                    dependencies = find_data_type_dependencies(destination)
                    for key, value in dependencies.items():
                        result[key].union(value)
                    result['DataType'].add(destination[0])
            elif edge == 'constraints':
                continue
            elif edge == 'metadata':
                continue
            else:
                abort(500)
    return result
