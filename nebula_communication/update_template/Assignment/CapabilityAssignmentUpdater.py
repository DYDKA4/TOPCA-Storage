from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template import NebulaCommunicationUpdateTemplateException
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment, \
    add_property_assignment, get_property_assignment
from parser.parser.tosca_v_1_3.assignments.CapabilityAssignment import CapabilityAssignment


def start_attribute_assignment(father_node_vid, varargs):
    if len(varargs) < 2:
        raise NebulaCommunicationUpdateTemplateException(400, 'start_attribute_assignment: varargs is too short')
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        raise NebulaCommunicationUpdateTemplateException(400, 'start_attribute_assignment: destination is None')
    capability_vid_to_update = None
    for capability_vid in destination:
        capability_value = fetch_vertex(capability_vid, 'CapabilityAssignment')
        capability_value = capability_value.as_map()
        if capability_value.get('name').as_string() == varargs[1]:
            capability_vid_to_update = capability_vid
            break
    if capability_vid_to_update is None:
        raise NebulaCommunicationUpdateTemplateException(400, 'start_attribute_assignment: capability_vid_to_update '
                                                              'is None')
    return capability_vid_to_update


def update_capability_assignment(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update,
                                 cluster_name):
    capability_vid_to_update = start_attribute_assignment(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + capability_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(capability_vid_to_update, 'CapabilityAssignment')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('CapabilityAssignment', capability_vid_to_update, value_name, value)
        else:
            raise NebulaCommunicationUpdateTemplateException(501, 'update_capability_assignment: not implemented yet')
    elif varargs[2] == 'properties':
        if not add_property_assignment(type_update, varargs, value, value_name, cluster_name, capability_vid_to_update):
            update_property_assignment(service_template_vid, capability_vid_to_update, value, value_name,
                                       varargs[2:], type_update)
    else:
        raise NebulaCommunicationUpdateTemplateException(400, 'update_capability_assignment: unexpected behaviour')


def add_capability_assignment(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = CapabilityAssignment('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_capability_assignment(father_node_vid, value, value_name, varargs: list):
    capability_vid_to_update = start_attribute_assignment(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(capability_vid_to_update, 'CapabilityAssignment')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return capability_vid_to_update.as_string()
        else:
            raise NebulaCommunicationUpdateTemplateException(501, 'update_capability_assignment: not implemented yet')
    elif varargs[2] == 'properties':
        return get_property_assignment(capability_vid_to_update, value, value_name, varargs[2:])
    else:
        raise NebulaCommunicationUpdateTemplateException(400, 'update_capability_assignment: unexpected behaviour')


