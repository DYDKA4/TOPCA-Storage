from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Assignment.RequirementAssignment import form_result, return_all
from nebula_communication.update_template.Definition.NotificationDefinitionUpdater import \
    update_notification_definition, add_notification_definition, get_notification_definition
from nebula_communication.update_template.Definition.OperationDefinitionUpdater import update_operation_definition, \
    add_operation_definition, get_operation_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition, \
    add_property_definition, get_property_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata, add_metadata, get_metadata
from parser.parser.tosca_v_1_3.types.InterfaceType import InterfaceType


def start_interface_type(father_node_vid, varargs):
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
    return interface_type_vid_to_update


def update_interface_type(father_node_vid, value, value_name, varargs: list, type_update, cluster_name):
    interface_type_vid_to_update = start_interface_type(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + interface_type_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(interface_type_vid_to_update, 'InterfaceType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            derived_from_vertex = find_destination(interface_type_vid_to_update, value_name)
            new_derived_interface_vid = None
            destination = find_destination(father_node_vid, varargs[0])
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
        if not add_property_definition(type_update, varargs[2:], cluster_name, interface_type_vid_to_update,
                                       varargs[2]):
            update_property_definition(father_node_vid, interface_type_vid_to_update, value, value_name, varargs[2:],
                                       type_update, cluster_name)
    elif varargs[2] == 'metadata':
        if not add_metadata(type_update, varargs[2:], value, value_name, cluster_name, interface_type_vid_to_update):
            update_metadata(interface_type_vid_to_update, value, value_name, varargs[2:], type_update)
    elif varargs[2] == 'operations':
        if not add_operation_definition(type_update, varargs[2:], cluster_name, interface_type_vid_to_update,
                                        varargs[2]):
            update_operation_definition(father_node_vid, interface_type_vid_to_update, value, value_name, varargs[2:],
                                        type_update, cluster_name)
    elif varargs[2] == 'notifications':
        if not add_notification_definition(type_update, varargs[2:], cluster_name, interface_type_vid_to_update,
                                           varargs[2]):
            update_notification_definition(father_node_vid, interface_type_vid_to_update, value, value_name,
                                           varargs[2:], type_update, cluster_name)
    else:
        abort(400)


def add_interface_type(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = InterfaceType('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_interface_type(father_node_vid, value, value_name, varargs: list):
    interface_vid_to_update = start_interface_type(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(interface_vid_to_update, 'InterfaceType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            return form_result(interface_vid_to_update, value_name)
        elif value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return interface_vid_to_update.as_string()
        else:
            abort(501)
    elif varargs[2] == 'metadata':
        destination = find_destination(interface_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_metadata(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'inputs':
        destination = find_destination(interface_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_property_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'operations':
        destination = find_destination(interface_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_operation_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'notification':
        destination = find_destination(interface_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_notification_definition(father_node_vid, value, value_name, varargs[2:])
    else:
        abort(400)
