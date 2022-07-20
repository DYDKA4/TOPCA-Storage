from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge
from nebula_communication.update_template.Assignment.AttributeAssignmentUpdater import update_attribute_assignment, \
    add_attribute_assignment
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment, \
    add_property_assignment
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata


def update_group_definition(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update,
                            cluster_name):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    group_vid_to_update = None
    for group_vid in destination:
        group_value = fetch_vertex(group_vid, 'GroupDefinition')
        group_value = group_value.as_map()
        if group_value.get('name').as_string() == varargs[1]:
            group_vid_to_update = group_vid
            break
    if group_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(group_vid_to_update, 'GroupDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            type_vertex = find_destination(group_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template_vid, 'group_types')
            for group_type_vid in destination:
                group_type_value = fetch_vertex(group_type_vid, 'GroupType')
                group_type_value = group_type_value.as_map()
                if '"' + group_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = group_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, group_vid_to_update, type_vertex[0])
            add_edge(value_name, '', group_vid_to_update, new_type_vid, '')
        elif value_name == 'members':
            valid_source_type_vertexes = find_destination(group_vid_to_update, value_name)
            delete_vertex = None
            for valid_source_type_vid in valid_source_type_vertexes:
                valid_source_value = fetch_vertex(valid_source_type_vid, 'NodeTemplate')
                valid_source_value = valid_source_value.as_map()
                if '"' + valid_source_value.get('name').as_string() + '"' == value:
                    delete_vertex = valid_source_type_vid
                    break
            if delete_vertex:
                delete_edge(value_name, group_vid_to_update, delete_vertex)
            else:
                add_vertex = None
                node_template_vertexes = find_destination(
                    find_destination(service_template_vid, 'topology_template')[0],
                    'node_templates')
                if node_template_vertexes is None:
                    abort(500)
                for node_types_vertex in node_template_vertexes:
                    node_types_value = fetch_vertex(node_types_vertex, 'NodeType')
                    node_types_value = node_types_value.as_map()
                    if '"' + node_types_value.get('name').as_string() + '"' == value:
                        add_vertex = node_types_vertex
                        break
                if add_vertex is None:
                    abort(400)
                add_edge(value_name, '', group_vid_to_update, add_vertex, '')
        elif value_name in vertex_value.keys():
            update_vertex('GroupDefinition', group_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'metadata':
        update_metadata(group_vid_to_update, value, value_name, varargs[2:], type_update)
    elif varargs[2] == 'attributes':
        if not add_attribute_assignment(type_update, varargs[2:], cluster_name, group_vid_to_update, varargs[2]):
            update_attribute_assignment(service_template_vid, group_vid_to_update, value, value_name, varargs[2:],
                                        type_update)
    elif varargs[2] == 'properties':
        if not add_property_assignment(type_update, varargs, value, value_name, cluster_name, group_vid_to_update):
            update_property_assignment(service_template_vid, group_vid_to_update, value, value_name, varargs[2:],
                                       type_update)
    else:
        abort(400)
