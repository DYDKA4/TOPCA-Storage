from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Assignment.RequirementAssignment import form_result, return_all
from nebula_communication.update_template.Definition.AttributeDefinitionUpdater import update_attribute_definition, \
    add_attribute_definition, get_attribute_definition
from nebula_communication.update_template.Definition.CapabilityDefinitionUpdater import update_capability_definition, \
    add_capability_definition, get_capability_definition
from nebula_communication.update_template.Definition.InterfaceDefinitionUpdater import update_interface_definition, \
    add_interface_definition, get_interface_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition, \
    add_property_definition, get_property_definition
from nebula_communication.update_template.Definition.RequirementDefinitionUpdater import update_requirement_definition, \
    add_requirement_definition, get_requirement_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata, add_metadata, get_metadata
from parser.parser.tosca_v_1_3.types.NodeType import NodeType


def start_node_type(father_node_vid, varargs):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    node_type_vid_to_update = None
    for node_type_vid in destination:
        node_type_value = fetch_vertex(node_type_vid, 'NodeType')
        node_type_value = node_type_value.as_map()
        if node_type_value.get('name').as_string() == varargs[1]:
            node_type_vid_to_update = node_type_vid
            break
    if node_type_vid_to_update is None:
        abort(400)
    return node_type_vid_to_update


def update_node_type(father_node_vid, value, value_name, varargs: list, type_update, cluster_name):
    node_type_vid_to_update = start_node_type(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + node_type_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(node_type_vid_to_update, 'NodeType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            derived_from_vertex = find_destination(node_type_vid_to_update, value_name)
            new_derived_relationship_vid = None
            destination = find_destination(father_node_vid, varargs[0])
            for node_type_vid in destination:
                node_type_value = fetch_vertex(node_type_vid, 'NodeType')
                node_type_value = node_type_value.as_map()
                if '"' + node_type_value.get('name').as_string() + '"' == value:
                    new_derived_relationship_vid = node_type_vid
                    break
            if new_derived_relationship_vid is None:
                abort(400)
            if derived_from_vertex is not None:
                if len(derived_from_vertex) > 1:
                    abort(500)
                delete_edge(value_name, node_type_vid_to_update, derived_from_vertex[0])
            add_edge(value_name, '', node_type_vid_to_update, new_derived_relationship_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('InterfaceType', node_type_vid_to_update, value_name, value)
        else:
            abort(400)
    elif varargs[2] == 'metadata':
        if not add_metadata(type_update, varargs[2:], value, value_name, cluster_name, node_type_vid_to_update):
            update_metadata(node_type_vid_to_update, value, value_name, varargs[2:], type_update)
    elif varargs[2] == 'attributes':
        if not add_attribute_definition(type_update, varargs[2:], cluster_name, node_type_vid_to_update,
                                        varargs[2]):
            update_attribute_definition(father_node_vid, node_type_vid_to_update, value, value_name, varargs[2:],
                                        type_update, cluster_name)
    elif varargs[2] == 'properties':
        if not add_property_definition(type_update, varargs[2:], cluster_name, node_type_vid_to_update,
                                       varargs[2]):
            update_property_definition(father_node_vid, node_type_vid_to_update, value, value_name, varargs[2:],
                                       type_update, cluster_name)
    elif varargs[2] == 'requirements':
        if not add_requirement_definition(type_update, varargs[2:], cluster_name, node_type_vid_to_update, varargs[2]):
            update_requirement_definition(father_node_vid, node_type_vid_to_update, value, value_name, varargs[2:],
                                          type_update, cluster_name)
    elif varargs[2] == 'capabilities':
        if not add_capability_definition(type_update, varargs[2:], cluster_name, node_type_vid_to_update, varargs[2]):
            update_capability_definition(father_node_vid, node_type_vid_to_update, value, value_name, varargs[2:],
                                         type_update, cluster_name)
    elif varargs[2] == 'interfaces':
        if not add_interface_definition(type_update, varargs[2:], cluster_name, node_type_vid_to_update, varargs[2]):
            update_interface_definition(father_node_vid, node_type_vid_to_update, value, value_name, varargs[2:],
                                        type_update, cluster_name)
    else:
        abort(400)


def add_node_type(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = NodeType('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_node_type(father_node_vid, value, value_name, varargs: list):
    node_vid_to_update = start_node_type(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(node_vid_to_update, 'NodeType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            return form_result(node_vid_to_update, value_name)
        elif value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return node_vid_to_update.as_string()
        else:
            abort(501)
    elif varargs[2] == 'metadata':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_metadata(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'attributes':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_attribute_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'properties':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_property_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'requirements':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_requirement_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'capabilities':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_capability_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'interfaces':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_interface_definition(father_node_vid, value, value_name, varargs[2:])
    else:
        abort(400)
