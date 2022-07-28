from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Assignment.AttributeAssignmentUpdater import update_attribute_assignment, \
    add_attribute_assignment, get_attribute_assignment
from nebula_communication.update_template.Assignment.CapabilityAssignmentUpdater import update_capability_assignment, \
    add_capability_assignment, get_capability_assignment
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment, \
    add_property_assignment, get_property_assignment
from nebula_communication.update_template.Assignment.RequirementAssignment import update_requirement_assignment, \
    add_requirement_assignment, form_result, return_all, get_requirement_assignment
from nebula_communication.update_template.Definition.ArtifactDefinition import update_artifact_definition, \
    add_artifact_definition, get_artifact_definition
from nebula_communication.update_template.Definition.InterfaceDefinitionUpdater import update_interface_definition, \
    add_interface_definition, get_interface_definition
from nebula_communication.update_template.Definition.NodeFilterDefinitionUpdater import update_node_filter_definition, \
    add_node_filter_definition, get_node_filter_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata, add_metadata, get_metadata
from parser.parser.tosca_v_1_3.others.NodeTemplate import NodeTemplate


def start_node_template(father_node_vid, varargs):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    node_template_vid_to_update = None
    for node_template_vid in destination:
        node_template_value = fetch_vertex(node_template_vid, 'NodeTemplate')
        node_template_value = node_template_value.as_map()
        if node_template_value.get('name').as_string() == varargs[1]:
            node_template_vid_to_update = node_template_vid
            break
    if node_template_vid_to_update is None:
        abort(400)
    return node_template_vid_to_update


def update_node_template(service_template, father_node_vid, value, value_name, varargs: list, type_update,
                         cluster_name):
    node_template_vid_to_update = start_node_template(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + node_template_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(node_template_vid_to_update, 'NodeTemplate')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            type_vertex = find_destination(node_template_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template, 'node_types')
            for data_type_vid in destination:
                data_type_value = fetch_vertex(data_type_vid, 'NodeType')
                data_type_value = data_type_value.as_map()
                if '"' + data_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = data_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, node_template_vid_to_update, type_vertex[0])
            add_edge(value_name, '', node_template_vid_to_update, new_type_vid, '')
        elif value_name == 'copy':
            type_vertex = find_destination(node_template_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(find_destination(service_template, 'topology_template')[0], 'node_templates')
            for data_type_vid in destination:
                data_type_value = fetch_vertex(data_type_vid, 'NodeTemplate')
                data_type_value = data_type_value.as_map()
                if '"' + data_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = data_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, node_template_vid_to_update, type_vertex[0])
            add_edge(value_name, '', node_template_vid_to_update, new_type_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('NodeTemplate', node_template_vid_to_update, value_name, value)
        else:
            abort(400)
    elif varargs[2] == 'metadata':
        if not add_metadata(type_update, varargs[2:], value, value_name, cluster_name, node_template_vid_to_update):
            update_metadata(node_template_vid_to_update, value, value_name, varargs[2:], type_update)
    elif varargs[2] == 'attributes':
        if not add_attribute_assignment(type_update, varargs[2:], cluster_name, node_template_vid_to_update,
                                        varargs[2]):
            update_attribute_assignment(service_template, node_template_vid_to_update, value, value_name, varargs[2:],
                                        type_update)
    elif varargs[2] == 'properties':
        if not add_property_assignment(type_update, varargs[2:], value, value_name, cluster_name,
                                       node_template_vid_to_update):
            update_property_assignment(service_template, node_template_vid_to_update, value, value_name, varargs[2:],
                                       type_update)
    elif varargs[2] == 'requirements':
        if not add_requirement_assignment(type_update, varargs[2:], cluster_name, node_template_vid_to_update,
                                          varargs[2]):
            update_requirement_assignment(service_template, node_template_vid_to_update, value, value_name, varargs[2:],
                                          type_update, cluster_name)
    elif varargs[2] == 'capabilities':
        if not add_capability_assignment(type_update, varargs[2:], cluster_name, node_template_vid_to_update,
                                         varargs[2]):
            update_capability_assignment(service_template, node_template_vid_to_update, value, value_name, varargs[2:],
                                         type_update, cluster_name)
    elif varargs[2] == 'interfaces':
        if not add_interface_definition(type_update, varargs[2:], cluster_name, node_template_vid_to_update,
                                        varargs[2]):
            update_interface_definition(service_template, node_template_vid_to_update, value, value_name, varargs[2:],
                                        type_update, cluster_name)
    elif varargs[2] == 'artifacts':
        if not add_artifact_definition(type_update, varargs[2:], cluster_name, node_template_vid_to_update, varargs[2]):
            update_artifact_definition(service_template, node_template_vid_to_update, value, value_name, varargs[2:],
                                       type_update)
    elif varargs[2] == 'node_filter':
        if not add_node_filter_definition(type_update, varargs[2:], cluster_name, node_template_vid_to_update,
                                          varargs[2]):
            update_node_filter_definition(service_template, node_template_vid_to_update, value, value_name, varargs[2:],
                                          type_update, cluster_name)
    else:
        abort(400)


def add_node_template(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = NodeTemplate('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_node_template(father_node_vid, value, value_name, varargs: list):
    node_vid_to_update = start_node_template(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(node_vid_to_update, 'NodeTemplate')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            return form_result(node_vid_to_update, value_name)
        elif value_name == 'copy':
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
        return get_attribute_assignment(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'properties':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_property_assignment(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'requirements':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_requirement_assignment(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'capabilities':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_capability_assignment(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'interfaces':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_interface_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'artifacts':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_artifact_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'node_filter':
        destination = find_destination(node_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_node_filter_definition(father_node_vid, value, value_name, varargs[2:])
    else:
        abort(400)
