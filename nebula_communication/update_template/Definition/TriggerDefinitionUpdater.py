from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, \
    delete_vertex, add_in_vertex
from parser.parser.tosca_v_1_3.definitions.TriggerDefinition import TriggerDefinition


def update_trigger_definition(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update,
                              cluster_name):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    requirement_vid_to_update = None
    for requirement_vid in destination:
        requirement_value = fetch_vertex(requirement_vid, 'TriggerDefinition')
        requirement_value = requirement_value.as_map()
        if requirement_value.get('name').as_string() == varargs[1]:
            requirement_vid_to_update = requirement_vid
            break
    if requirement_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + requirement_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(requirement_vid_to_update, 'TriggerDefinition')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('TriggerDefinition', requirement_vid_to_update, value_name, value)
        else:
            abort(400)
    elif varargs[2] == 'event_filter':
        abort(501)
        # update_event_filter_definition(requirement_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'constraint':
        abort(501)
        # update_condition_clause_definition(requirement_vid_to_update, value, value_name, varargs[2:])
    else:
        abort(400)


def add_trigger_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = TriggerDefinition('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False
