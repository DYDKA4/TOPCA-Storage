from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Definition.NotificationImplementationDefinition import \
    update_notification_implementation_definition, add_notification_implementation_definition
from parser.parser.tosca_v_1_3.definitions.NotificationDefinition import NotificationDefinition


def start_notification_definition(father_node_vid, varargs):
    if len(varargs) < 1:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    notification_vid_to_update = None
    for notification_type_vid in destination:
        notification_value = fetch_vertex(notification_type_vid, 'NotificationDefinition')
        notification_value = notification_value.as_map()
        if notification_value.get('name').as_string() == varargs[1]:
            notification_vid_to_update = notification_type_vid
            break
    if notification_vid_to_update is None:
        abort(400)
    return notification_vid_to_update


def update_notification_definition(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update,
                                   cluster_name):
    notification_vid_to_update = start_notification_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + notification_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(notification_vid_to_update, 'NotificationDefinition')
        vertex_value = vertex_value.as_map()
        if value_name not in vertex_value.keys():
            abort(400)
        update_vertex('NotificationDefinition', notification_vid_to_update, value_name, value)
    elif len(varargs) > 2:
        if varargs[2] == 'implementation':
            if add_notification_implementation_definition(type_update, varargs, cluster_name,
                                                          notification_vid_to_update, varargs[2]):
                update_notification_implementation_definition(service_template_vid, notification_vid_to_update, value,
                                                              value_name, varargs[2:], type_update, cluster_name)
        else:
            abort(400)
    else:
        abort(400)


def add_notification_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        import_definition = NotificationDefinition('"' + varargs[1] + '"')
        generate_uuid(import_definition, cluster_name)
        add_in_vertex(import_definition.vertex_type_system, 'name, vertex_type_system',
                      import_definition.name + ',"' + import_definition.vertex_type_system + '"', import_definition.vid)
        add_edge(edge_name, '', parent_vid, import_definition.vid, '')
        return True
    return False


def get_notification_definition(father_node_vid, value, value_name, varargs: list):
    notification_vid_to_update = start_notification_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(notification_vid_to_update, 'NotificationDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'implementation':
            implementation = find_destination(notification_vid_to_update, value_name)
            if implementation and fetch_vertex(implementation[0], 'NotificationImplementationDefinition'):
                abort(400)
            elif implementation and fetch_vertex(implementation[0], 'ArtifactDefinition'):
                return implementation[0].as_string()
        elif value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return notification_vid_to_update.as_string()
        else:
            abort(501)
    elif varargs[2] == 'implementation':
        implementation = find_destination(notification_vid_to_update, varargs[2])
        if implementation and fetch_vertex(implementation[0], 'ArtifactDefinition'):
            abort(400)
        elif implementation and fetch_vertex(implementation[0], 'NotificationImplementationDefinition'):
            if len(implementation) > 1:
                abort(500)
            return implementation
    else:
        abort(400)
