from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex


def update_import_definition(father_node_vid, value, value_name, varargs: list):
    if len(varargs) != 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    repository_vid_to_update = None
    for repository_vid in destination:
        metadata_value = fetch_vertex(repository_vid, 'ImportDefinition')
        metadata_value = metadata_value.as_map()
        if metadata_value.get('file').as_string() == varargs[1]:
            repository_vid_to_update = repository_vid
            break
    if repository_vid_to_update is None:
        abort(400)
    vertex_value = fetch_vertex(repository_vid_to_update, 'ImportDefinition')
    vertex_value = vertex_value.as_map()
    if value_name not in vertex_value.keys():
        abort(400)
    update_vertex('ImportDefinition', repository_vid_to_update, value_name, value)
