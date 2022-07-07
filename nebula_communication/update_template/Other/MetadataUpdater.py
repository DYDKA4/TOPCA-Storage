from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, update_vertex, find_destination


def update_metadata(father_node_vid, value, value_name, varargs: list):
    if len(varargs) != 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    metadata_vid_to_update = None
    for metadata_vid in destination:
        metadata_value = fetch_vertex(metadata_vid, 'Metadata')
        metadata_value = metadata_value.as_map()
        if metadata_value.get('name').as_string() == varargs[1]:
            metadata_vid_to_update = metadata_vid
            break
    if metadata_vid_to_update is None:
        abort(400)
    if value_name != 'value':
        abort(400)
    else:
        value_name = 'values'
    update_vertex('Metadata', metadata_vid_to_update, value_name, value)
