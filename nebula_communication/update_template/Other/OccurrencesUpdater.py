from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import fetch_vertex, update_vertex, find_destination, delete_vertex, \
    add_in_vertex, add_edge
from parser.parser.tosca_v_1_3.others.Occurrences import Occurrences


def update_occurrences(father_node_vid, value, value_name, varargs: list, type_update):
    if len(varargs) != 1:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    if len(destination) > 1:
        if type_update == 'delete':
            for destination_vid in destination:
                delete_vertex('"' + destination_vid.as_string() + '"')
            return
        else:
            abort(400)
    occurrences_vid_to_update = destination[0]
    if type_update == 'delete':
        delete_vertex('"' + occurrences_vid_to_update.as_string() + '"')
        return
    if occurrences_vid_to_update is None:
        abort(400)
    if value_name in occurrences_vid_to_update.as_map().keys():
        update_vertex('Occurrences', occurrences_vid_to_update, value_name, value)
    else:
        abort(400)


def add_occurrences(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 1:
        schema_definition = Occurrences('Unbounded', 'Unbounded')
        generate_uuid(schema_definition, cluster_name)
        add_in_vertex(schema_definition.vertex_type_system, 'vertex_type_system',
                      '"' + schema_definition.vertex_type_system + '"', schema_definition.vid)
        add_edge(edge_name, '', parent_vid, schema_definition.vid, '')
        return True
    return False
