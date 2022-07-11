from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge
from nebula_communication.update_template.Definition.NotificationImplementationDefinition import \
    update_notification_implementation_definition


def update_notification_definition(service_template_vid, father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 1:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None or len(destination) > 1:
        abort(400)
    notification_vid_to_update = destination[0]
    if len(varargs) == 1:
        vertex_value = fetch_vertex(notification_vid_to_update, 'NotificationDefinition')
        vertex_value = vertex_value.as_map()
        if value_name not in vertex_value.keys():
            abort(400)
        update_vertex('NotificationDefinition', notification_vid_to_update, value_name, value)
    elif len(varargs) > 1:
        if varargs[1] == 'implementation':
            update_notification_implementation_definition(service_template_vid, notification_vid_to_update, value,
                                                          value_name, varargs[2:])
        else:
            abort(400)
    else:
        abort(400)
