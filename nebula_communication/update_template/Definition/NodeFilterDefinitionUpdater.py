from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Definition.CapabilityFilterDefinition import \
    update_capability_filter_definition, add_capability_filter_definition, get_capability_filter_definition
from nebula_communication.update_template.Definition.PropertyFilterDefinitionUpdater import \
    update_property_filter_definition, add_property_filter_definition, get_property_filter_definition
from nebula_communication.update_template.find_functions import return_all
from parser.parser.tosca_v_1_3.definitions.NodeFilterDefinition import NodeFilterDefinition


def update_node_filter_definition(service_template_vid, father_node_vid, value, value_name, varargs: list,
                                  type_update, cluster_name):
    if len(varargs) < 2:
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
    node_filter_vid_to_update = destination[0]
    if node_filter_vid_to_update is None:
        abort(400)
    if type_update == 'delete':
        delete_vertex('"' + node_filter_vid_to_update.as_string() + '"')
        return
    elif varargs[1] == 'properties':
        if not add_property_filter_definition(type_update, varargs[1:], cluster_name, node_filter_vid_to_update,
                                              varargs[1]):
            update_property_filter_definition(service_template_vid, node_filter_vid_to_update, value, value_name,
                                              varargs[1:], type_update, cluster_name)
    elif varargs[1] == 'capability':
        if not add_capability_filter_definition(type_update, varargs[1:], cluster_name, node_filter_vid_to_update,
                                                varargs[1]):
            update_capability_filter_definition(service_template_vid, node_filter_vid_to_update, value, value_name,
                                                varargs[1:], type_update, cluster_name)
    else:
        abort(400)


def add_node_filter_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 1:
        data_type = NodeFilterDefinition()
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'vertex_type_system',
                      '"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_node_filter_definition(father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    if len(destination) > 1:
        abort(400)
    node_filter_vid_to_update = destination[0]
    if node_filter_vid_to_update is None:
        abort(400)
    if varargs[2] == 'properties':
        destination = find_destination(node_filter_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_property_filter_definition(father_node_vid, value, value_name, varargs[1:])
    elif varargs[2] == 'capability':
        destination = find_destination(node_filter_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_capability_filter_definition(father_node_vid, value, value_name, varargs[1:])
    else:
        abort(400)
