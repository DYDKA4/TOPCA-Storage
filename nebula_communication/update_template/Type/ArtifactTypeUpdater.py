from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition


def update_artifact_type(father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    artifact_vid_to_update = None
    for artifact_vid in destination:
        artifact_value = fetch_vertex(artifact_vid, 'ArtifactType')
        artifact_value = artifact_value.as_map()
        if artifact_value.get('name').as_string() == varargs[1]:
            artifact_vid_to_update = artifact_vid
            break
    if artifact_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(artifact_vid_to_update, 'ArtifactType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            derived_from_vertex = find_destination(artifact_vid_to_update, value_name)
            new_derived_artifact_vid = None
            for artifact_vid in destination:
                artifact_value = fetch_vertex(artifact_vid, 'ArtifactType')
                artifact_value = artifact_value.as_map()
                if '"' + artifact_value.get('name').as_string() + '"' == value:
                    new_derived_artifact_vid = artifact_vid
                    break
            if new_derived_artifact_vid is None:
                abort(400)
            if derived_from_vertex is not None:
                if len(derived_from_vertex) > 1:
                    abort(500)
                delete_edge(value_name, artifact_vid_to_update, derived_from_vertex[0])
            add_edge(value_name, '', artifact_vid_to_update, new_derived_artifact_vid, '')

        elif value_name in vertex_value.keys():
            update_vertex('ArtifactType', artifact_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'properties':
        update_property_definition(father_node_vid,artifact_vid_to_update, value, value_name, varargs[2:])
    else:
        abort(400)


