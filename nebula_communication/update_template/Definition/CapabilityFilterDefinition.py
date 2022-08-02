from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Definition.PropertyFilterDefinitionUpdater import \
    update_property_filter_definition, add_property_filter_definition, get_property_filter_definition
from nebula_communication.update_template.find_functions import return_all
from parser.parser.tosca_v_1_3.definitions.CapabilityFilterDefinition import CapabilityFilterDefinition


def start_capability_filter_definition(father_node_vid, varargs):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None or len(destination) > 1:
        abort(400)
    capability_filter_vid_to_update = None
    for capability_vid in destination:
        capability_filter_value = fetch_vertex(capability_vid, 'CapabilityFilterDefinition')
        capability_filter_value = capability_filter_value.as_map()
        if capability_filter_value.get('name').as_string() == varargs[1]:
            capability_filter_vid_to_update = capability_vid
            break
    if capability_filter_vid_to_update is None:
        abort(400)
    return capability_filter_vid_to_update


def update_capability_filter_definition(service_template_vid, father_node_vid, value, value_name, varargs: list,
                                        type_update, cluster_name):
    capability_filter_vid_to_update = start_capability_filter_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + capability_filter_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(capability_filter_vid_to_update, 'CapabilityFilterDefinition')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('CapabilityFilterDefinition', capability_filter_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'properties':
        if not add_property_filter_definition(type_update, varargs[2:], cluster_name, capability_filter_vid_to_update,
                                              varargs[2]):
            update_property_filter_definition(service_template_vid, capability_filter_vid_to_update, value, value_name,
                                              varargs[2:], type_update, cluster_name)
    else:
        abort(400)


def add_capability_filter_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = CapabilityFilterDefinition('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_capability_filter_definition(father_node_vid, value, value_name, varargs: list):
    capability_vid_to_update = start_capability_filter_definition(father_node_vid, varargs)
    property_value = fetch_vertex(capability_vid_to_update, 'CapabilityFilterDefinition')
    property_value = property_value.as_map()
    if value_name in property_value.keys():
        if value == property_value.get(value_name).as_string():
            return capability_vid_to_update.as_string()
    elif varargs[2] == 'properties':
        destination = find_destination(capability_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_property_filter_definition(father_node_vid, value, value_name, varargs[2:])
    else:
        abort(400)
