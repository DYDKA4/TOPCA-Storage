from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import fetch_vertex, update_vertex, find_destination, delete_vertex, \
    add_in_vertex, add_edge
from parser.parser.tosca_v_1_3.others.Metadata import Metadata


def start_metadata(father_node_vid, varargs):
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
    return metadata_vid_to_update


def update_metadata(father_node_vid, value, value_name, varargs: list, type_update):
    metadata_vid_to_update = start_metadata(father_node_vid, varargs)
    if type_update == 'delete':
        delete_vertex('"' + metadata_vid_to_update.as_string() + '"')
        return
    if value_name != 'value':
        abort(400)
    else:
        value_name = 'values'
    update_vertex('Metadata', metadata_vid_to_update, value_name, value)


def add_metadata(type_update, varargs, value, value_name, cluster_name, parent_vid):
    if type_update == 'add':
        metadata = Metadata('"' + varargs[1] + '"', value)
        metadata.vertex_type_system = '"Metadata"'
        generate_uuid(metadata, cluster_name)
        add_in_vertex('Metadata', 'name, ' + value_name + ', vertex_type_system',
                      metadata.name + ',' + value + ',' + metadata.vertex_type_system, metadata.vid)
        add_edge('metadata', '', parent_vid, metadata.vid, '')
        return True
    return False


def get_metadata(father_node_vid, value, value_name, varargs: list):
    metadata_vid_to_update = start_metadata(father_node_vid, varargs)
    property_value = fetch_vertex(metadata_vid_to_update, 'Metadata')
    property_value = property_value.as_map()
    if value_name in property_value.keys():
        if value == property_value.get(value_name).as_string():
            return metadata_vid_to_update.as_string()
    else:
        abort(400)
