import inspect

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import fetch_vertex, update_vertex, find_destination, delete_vertex, \
    add_in_vertex, add_edge
from nebula_communication.update_template import NebulaCommunicationUpdateTemplateException
from parser.parser.tosca_v_1_3.assignments.AttributeAssignment import AttributeAssignment


def start_attribute_assignment(father_node_vid, varargs):
    if len(varargs) != 2:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: varargs != 2')
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: destination is None')
    property_vid_to_update = None
    for property_vid in destination:
        property_value = fetch_vertex(property_vid, 'AttributeAssignment')
        property_value = property_value.as_map()
        if property_value.get('name').as_string() == varargs[1]:
            property_vid_to_update = property_vid
            break
    if property_vid_to_update is None:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: property_vid_to_update '
                                                              'is None')
    return property_vid_to_update


def update_attribute_assignment(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update):
    property_vid_to_update = start_attribute_assignment(father_node_vid, varargs)
    if type_update == 'delete':
        delete_vertex('"' + property_vid_to_update.as_string() + '"')
        return
    if value_name == 'value':
        value_name = 'values'
    property_value = fetch_vertex(property_vid_to_update, 'AttributeAssignment')
    property_value = property_value.as_map()
    if value_name in property_value.keys():
        update_vertex('PropertyAssignment', property_vid_to_update, value_name, value)
    else:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: wrong arguments')


def add_attribute_assignment(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = AttributeAssignment('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_attribute_assignment(father_node_vid, value, value_name, varargs: list):
    property_vid_to_update = start_attribute_assignment(father_node_vid, varargs)
    property_value = fetch_vertex(property_vid_to_update, 'AttributeAssignment')
    property_value = property_value.as_map()
    if value_name in property_value.keys():
        if value == property_value.get(value_name).as_string():
            return property_vid_to_update.as_string()
    else:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: wrong arguments')
