from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment
from nebula_communication.update_template.Definition.NotificationDefinitionUpdater import update_notification_definition
from nebula_communication.update_template.Definition.OperationDefinitionUpdater import update_operation_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata


def update_interface_definition(service_template_vid, father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    interface_definition_vid_to_update = None
    for interface_definition_vid in destination:
        interface_definition_value = fetch_vertex(interface_definition_vid, 'InterfaceDefinition')
        interface_definition_value = interface_definition_value.as_map()
        if interface_definition_value.get('name').as_string() == varargs[1]:
            interface_definition_vid_to_update = interface_definition_vid
            break
    if interface_definition_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(interface_definition_vid_to_update, 'InterfaceDefinition')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('InterfaceDefinition', interface_definition_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'inputs':
        inputs_property = find_destination(interface_definition_vid_to_update, varargs[2])
        if inputs_property is None:
            abort(400)
        if fetch_vertex(inputs_property[0], 'PropertyAssignment'):
            update_property_assignment(service_template_vid, interface_definition_vid_to_update, value, value_name,
                                       varargs[2:])
        elif fetch_vertex(inputs_property[0], 'PropertyDefinition'):
            update_property_definition(service_template_vid, interface_definition_vid_to_update, value, value_name,
                                       varargs[2:])
    elif varargs[2] == 'operations':
        update_operation_definition(service_template_vid, interface_definition_vid_to_update, value, value_name,
                                    varargs[2:])
    elif varargs[2] == 'notifications':
        update_notification_definition(service_template_vid, interface_definition_vid_to_update, value, value_name,
                                       varargs[2:])
    else:
        abort(400)
