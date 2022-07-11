from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, update_vertex, find_destination


def update_occurrences(father_node_vid, value, value_name, varargs: list):
    if len(varargs) != 1:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None or len(destination) != 1:
        abort(400)
    occurrences_vid_to_update = destination[0]
    if occurrences_vid_to_update is None:
        abort(400)
    occurrences_keys = fetch_vertex(occurrences_vid_to_update, 'Occurrences').as_map().keys()
    if value_name in occurrences_vid_to_update.as_map().keys():
        update_vertex('Occurrences', occurrences_vid_to_update, value_name, value)
    else:
        abort(400)
