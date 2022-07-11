from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge


def update_artifact_definition(service_template_vid, father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    artifact_vid_to_update = None
    for artifact_vid in destination:
        artifact_value = fetch_vertex(artifact_vid, 'ArtifactDefinition')
        artifact_value = artifact_value.as_map()
        if artifact_value.get('name').as_string() == varargs[1]:
            artifact_vid_to_update = artifact_vid
            break
    if artifact_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(artifact_vid_to_update, 'ArtifactDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            type_vertex = find_destination(artifact_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template_vid, 'artifact_types')
            for artifact_type_vid in destination:
                artifact_type_value = fetch_vertex(artifact_type_vid, 'ArtifactType')
                artifact_type_value = artifact_type_value.as_map()
                if '"' + artifact_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = artifact_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, artifact_vid_to_update, type_vertex[0])
            add_edge(value_name, '', artifact_vid_to_update, new_type_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('ArtifactDefinition', artifact_vid_to_update, value_name, value)
        else:
            abort(501)
    else:
        abort(400)
