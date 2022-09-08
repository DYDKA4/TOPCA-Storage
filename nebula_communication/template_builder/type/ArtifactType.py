from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination, find_all_edges
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.ProperyDefinition import construct_property_definition, \
    find_property_definition_dependencies
from parser.parser.tosca_v_1_3.types.ArtifactType import ArtifactType


def construct_artifact_type(list_of_vid) -> dict:
    result = {}
    artifact_type = ArtifactType('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'ArtifactType')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(artifact_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'derived_from':
                if destination:
                    derived_from = fetch_vertex(destination[0], 'ArtifactType')
                    derived_from = derived_from.as_map()
                    derived_from = derived_from['name'].as_string()
                    tmp_result['derived_from'] = derived_from
            elif edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            elif edge == 'properties':
                tmp_result['properties'] = construct_property_definition(destination)
            elif edge == 'file_ext':
                print(edge, destination)
            else:
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result


def find_artifact_type_dependencies(list_of_vid) -> dict:
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
    artifact_type = ArtifactType('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'ArtifactType')
        vertex_value = vertex_value.as_map()
        vertex_keys = vertex_value.keys()
        edges = set(artifact_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'derived_from':
                if destination:
                    dependencies = find_artifact_type_dependencies(destination)
                    for key, value in dependencies.items():
                        result[key].union(value)
                    result['ArtifactType'].add(destination[0])
            elif edge == 'metadata':
                continue
            elif edge == 'properties':
                dependencies = find_property_definition_dependencies(destination)
                for key, value in dependencies.items():
                    result[key].union(value)
            elif edge == 'file_ext':
                continue
            else:
                abort(500)
    return result
