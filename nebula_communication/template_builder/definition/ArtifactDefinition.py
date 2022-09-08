from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.assignment.PropertyAssignment import construct_property_assignment
from nebula_communication.template_builder.definition.ProperyDefinition import find_property_definition_dependencies
from nebula_communication.template_builder.type.DataTypes import DefaultDataTypes, find_data_type_dependencies
from parser.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition


def construct_artifact_definition(list_of_vid, only) -> dict:
    result = {}

    artifact_definition = ArtifactDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'ArtifactDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        edges = set(artifact_definition.keys()) - set(vertex_keys) - {'vid'}
        ss = find_destination(vid, 'type')
        if not find_destination(vid, 'type'):
            result[vertex_value['name'].as_string()] = vertex_value['file'].as_string()
        else:
            for vertex_key in vertex_value.keys():
                if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                    tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
            for edge in edges:
                destination = find_destination(vid, edge)
                if edge == 'type':
                    if destination:
                        data_type = fetch_vertex(destination[0], 'ArtifactType')
                        data_type = data_type.as_map()
                        data_type = data_type['name'].as_string()
                        tmp_result['type'] = data_type
                    elif len(tmp_result.keys()) == 1:
                        keys = list(tmp_result.keys())
                        tmp_result = tmp_result[keys[0]]
                        break
                elif edge == 'properties':
                    tmp_result['properties'] = construct_property_assignment(destination, only)
                else:
                    abort(500)
            result[vertex_value['name'].as_string()] = tmp_result
    return result


def find_artifact_definition_dependencies(list_of_vid, result) -> dict:
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
    artifact_definition = ArtifactDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'ArtifactDefinition')
        vertex_value = vertex_value.as_map()
        vertex_keys = vertex_value.keys()
        edges = set(artifact_definition.keys()) - set(vertex_keys) - {'vid'}
        if not find_destination(vid, 'type'):
            continue
        else:
            for edge in edges:
                destination = find_destination(vid, edge)
                if edge == 'type':
                    if destination:
                        if destination[0] not in result['DataType']:
                            data_type = fetch_vertex(destination[0], 'DataType')
                            data_type = data_type.as_map()
                            data_type = data_type['name'].as_string()
                            if data_type not in DefaultDataTypes:
                                dependencies = find_data_type_dependencies(destination, result)
                                for key, value in dependencies.items():
                                    result[key].union(value)
                                result['DataType'].add(destination[0])
                elif edge == 'properties':
                    dependencies = find_property_definition_dependencies(destination, result)
                    for key, value in dependencies.items():
                        result[key].union(value)
                else:
                    abort(500)
    return result
