from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.SchemaDefinition import construct_schema_definition
from parser.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition


def construct_artifact_definition(list_of_vid) -> dict:
    result = {}

    artifact_definition = ArtifactDefinition('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'ArtifactDefinition')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_value.keys():
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(artifact_definition.keys()) - set(vertex_keys) - {'vid'}
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
                props = {}
                for properties in destination:
                    data_type = fetch_vertex(properties, 'PropertyAssignment')
                    data_type = data_type.as_map()
                    props[data_type['name'].as_string] = data_type['values'].as_string
                tmp_result['properties'] = props
            else:
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result
    return result
