from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment, \
    add_property_assignment, get_property_assignment
from nebula_communication.update_template.Definition.NotificationDefinitionUpdater import \
    update_notification_definition, add_notification_definition
from nebula_communication.update_template.Definition.OperationDefinitionUpdater import update_operation_definition, \
    add_operation_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition, \
    add_property_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition


def start_interface_definition(father_node_vid, varargs):
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
    return interface_definition_vid_to_update


def update_interface_definition(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update,
                                cluster_name):
    interface_definition_vid_to_update = start_interface_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + interface_definition_vid_to_update.as_string() + '"')
            return
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
            if not add_property_assignment(type_update, varargs[2:], value, value_name, cluster_name,
                                           interface_definition_vid_to_update):
                update_property_assignment(service_template_vid, interface_definition_vid_to_update, value, value_name,
                                           varargs[2:], type_update)
        elif fetch_vertex(inputs_property[0], 'PropertyDefinition'):
            if not add_property_definition(type_update, varargs[2:], cluster_name, interface_definition_vid_to_update,
                                           varargs[2]):
                update_property_definition(service_template_vid, interface_definition_vid_to_update, value, value_name,
                                           varargs[2:], type_update, cluster_name)
    elif varargs[2] == 'operations':
        if not add_operation_definition(type_update, varargs[2:], cluster_name, interface_definition_vid_to_update,
                                        varargs[2]):
            update_operation_definition(service_template_vid, interface_definition_vid_to_update, value, value_name,
                                        varargs[2:], type_update, cluster_name)
    elif varargs[2] == 'notifications':
        if not add_notification_definition(type_update, varargs[2:], cluster_name, interface_definition_vid_to_update,
                                           varargs[2]):
            update_notification_definition(service_template_vid, interface_definition_vid_to_update, value, value_name,
                                           varargs[2:], type_update, cluster_name)
    else:
        abort(400)


def add_interface_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = InterfaceDefinition('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def return_all(value, value_name, destination):
    if destination is None:
        return True, None
    if not value or not value_name:
        result = []
        for vid in destination:
            result.append(vid.as_string())
        return True, result
    return False, None


def get_interface_definition(father_node_vid, value, value_name, varargs: list):
    interface_vid_to_update = start_interface_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(interface_vid_to_update, 'CapabilityAssignment')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return interface_vid_to_update.as_string()
        else:
            abort(501)
    elif varargs[2] == 'inputs':
        destination = find_destination(interface_vid_to_update, value_name)
        if destination is None:
            return None
        if fetch_vertex(destination[0], 'PropertyAssignment'):
            result, flag = return_all(value, value_name, destination)
            if flag:
                return result
            return get_property_assignment(father_node_vid, value, value_name, varargs[2:])
        if fetch_vertex(destination[0], 'PropertyDefinition'):
            result, flag = return_all(value, value_name, destination)
            if flag:
                return result
            return get_property_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'operations':
        destination = find_destination(interface_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination)
        if flag:
            return result
        return get_operation_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'notifications':
        destination = find_destination(interface_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination)
        if flag:
            return result
        return get_notification_definition(father_node_vid, value, value_name, varargs[2:])
    else:
        abort(400)