from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge
from nebula_communication.update_template.Definition.NotificationDefinitionUpdater import update_notification_definition
from nebula_communication.update_template.Definition.OperationDefinitionUpdater import update_operation_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata


def update_interface_type(father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    interface_type_vid_to_update = None
    for interface_type_vid in destination:
        interface_type_value = fetch_vertex(interface_type_vid, 'InterfaceType')
        interface_type_value = interface_type_value.as_map()
        if interface_type_value.get('name').as_string() == varargs[1]:
            interface_type_vid_to_update = interface_type_vid
            break
    if interface_type_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(interface_type_vid_to_update, 'InterfaceType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            derived_from_vertex = find_destination(interface_type_vid_to_update, value_name)
            new_derived_interface_vid = None
            for interface_type_vid in destination:
                interface_type_value = fetch_vertex(interface_type_vid, 'InterfaceType')
                interface_type_value = interface_type_value.as_map()
                if '"' + interface_type_value.get('name').as_string() + '"' == value:
                    new_derived_interface_vid = interface_type_vid
                    break
            if new_derived_interface_vid is None:
                abort(400)
            if derived_from_vertex is not None:
                if len(derived_from_vertex) > 1:
                    abort(500)
                delete_edge(value_name, interface_type_vid_to_update, derived_from_vertex[0])
            add_edge(value_name, '', interface_type_vid_to_update, new_derived_interface_vid, '')

        elif value_name in vertex_value.keys():
            update_vertex('InterfaceType', interface_type_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'inputs':
        update_property_definition(father_node_vid, interface_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'metadata':
        update_metadata(interface_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'operations':
        update_operation_definition(father_node_vid, interface_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'notifications':
        update_notification_definition(father_node_vid, interface_type_vid_to_update, value, value_name, varargs[2:])
    else:
        abort(400)
