from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge, \
    add_in_vertex, delete_vertex
from nebula_communication.update_template.Definition.AttributeDefinitionUpdater import update_attribute_definition, \
    add_attribute_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition, \
    add_property_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata, add_metadata
from parser.parser.tosca_v_1_3.types.GroupType import GroupType


def update_group_type(father_node_vid, value, value_name, varargs: list, type_update, cluster_name):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    group_type_vid_to_update = None
    for group_type_vid in destination:
        group_type_value = fetch_vertex(group_type_vid, 'GroupType')
        group_type_value = group_type_value.as_map()
        if group_type_value.get('name').as_string() == varargs[1]:
            group_type_vid_to_update = group_type_vid
            break
    if group_type_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + group_type_vid_to_update.as_string() + '"')
            return

        vertex_value = fetch_vertex(group_type_vid_to_update, 'GroupType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            derived_from_vertex = find_destination(group_type_vid_to_update, value_name)
            new_derived_group_vid = None
            for group_type_vid in destination:
                group_type_value = fetch_vertex(group_type_vid, 'GroupType')
                group_type_value = group_type_value.as_map()
                if '"' + group_type_value.get('name').as_string() + '"' == value:
                    new_derived_group_vid = group_type_vid
                    break
            if new_derived_group_vid is None:
                abort(400)
            if derived_from_vertex is not None:
                if len(derived_from_vertex) > 1:
                    abort(500)
                delete_edge(value_name, group_type_vid_to_update, derived_from_vertex[0])
            add_edge(value_name, '', group_type_vid_to_update, new_derived_group_vid, '')
        elif value_name == 'members':
            members_type_vertexes = find_destination(group_type_vid_to_update, value_name)
            delete_vertex_vid = None
            for valid_source_type_vid in members_type_vertexes:
                valid_source_value = fetch_vertex(valid_source_type_vid, 'NodeType')
                valid_source_value = valid_source_value.as_map()
                if '"' + valid_source_value.get('name').as_string() + '"' == value:
                    delete_vertex_vid = valid_source_type_vid
                    break
            if delete_vertex_vid:
                delete_edge(value_name, group_type_vid_to_update, delete_vertex_vid)
            else:
                add_vertex = None
                node_types_vertexes = find_destination(father_node_vid, 'node_types')
                if node_types_vertexes is None:
                    abort(500)
                for node_types_vertex in node_types_vertexes:
                    node_types_value = fetch_vertex(node_types_vertex, 'NodeType')
                    node_types_value = node_types_value.as_map()
                    if '"' + node_types_value.get('name').as_string() + '"' == value:
                        add_vertex = node_types_vertex
                        break
                if add_vertex is None:
                    abort(400)
                add_edge(value_name, '', group_type_vid_to_update, add_vertex, '')

        elif value_name in vertex_value.keys():
            update_vertex('GroupType', group_type_vid_to_update, value_name, value)
        else:
            abort(400)
    elif varargs[2] == 'properties':
        if not add_property_definition(type_update, varargs[2:], value,group_type_vid_to_update,varargs[2]):
            update_property_definition(father_node_vid, group_type_vid_to_update, value, value_name, varargs[2:],
                                       type_update, cluster_name)
    elif varargs[2] == 'metadata':
        if not add_metadata(type_update, varargs[2:], value, value_name, cluster_name, group_type_vid_to_update):
            update_metadata(group_type_vid_to_update, value, value_name, varargs[2:], type_update)
    elif varargs[2] == 'attributes':
        if not add_attribute_definition(type_update, varargs[2:], cluster_name, group_type_vid_to_update,
                                        varargs[2]):
            update_attribute_definition(father_node_vid, group_type_vid_to_update, value, value_name, varargs[2:],
                                        type_update, cluster_name)
    else:
        abort(400)


def add_group_type(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = GroupType('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False
