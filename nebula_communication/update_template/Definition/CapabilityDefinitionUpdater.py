from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    add_in_vertex, delete_vertex
from nebula_communication.update_template.Assignment.RequirementAssignment import form_result, return_all
from nebula_communication.update_template.Definition.AttributeDefinitionUpdater import update_attribute_definition, \
    add_attribute_definition, get_attribute_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition, \
    add_property_definition, get_property_definition
from nebula_communication.update_template.Definition.SchemaDefinitionUpdate import get_schema_definition
from nebula_communication.update_template.Other.ConstraintClauseUpdater import get_constraint_clause
from nebula_communication.update_template.Other.OccurrencesUpdater import update_occurrences, add_occurrences, \
    get_occurrences
from parser.parser.tosca_v_1_3.definitions.CapabilityDefinition import CapabilityDefinition


def start_capability_definition(father_node_vid, varargs):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    capability_vid_to_update = None
    for capability_vid in destination:
        capability_value = fetch_vertex(capability_vid, 'CapabilityDefinition')
        capability_value = capability_value.as_map()
        if capability_value.get('name').as_string() == varargs[1]:
            capability_vid_to_update = capability_vid
            break
    if capability_vid_to_update is None:
        abort(400)
    return capability_vid_to_update


def update_capability_definition(service_template_vid, father_node_vid, value, value_name, varargs: list,
                                 type_update, cluster_name):
    capability_vid_to_update = start_capability_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + capability_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(capability_vid_to_update, 'CapabilityDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            type_vertex = find_destination(capability_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template_vid, 'capability_types')
            for data_type_vid in destination:
                data_type_value = fetch_vertex(data_type_vid, 'CapabilityType')
                data_type_value = data_type_value.as_map()
                if '"' + data_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = data_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, capability_vid_to_update, type_vertex[0])
            add_edge(value_name, '', capability_vid_to_update, new_type_vid, '')
        elif value_name == 'valid_source_type':
            valid_source_type_vertexes = find_destination(capability_vid_to_update, value_name)
            delete_vertex_vid = None
            for valid_source_type_vid in valid_source_type_vertexes:
                valid_source_value = fetch_vertex(valid_source_type_vid, 'NodeType')
                valid_source_value = valid_source_value.as_map()
                if '"' + valid_source_value.get('name').as_string() + '"' == value:
                    delete_vertex_vid = valid_source_type_vid
                    break
            if delete_vertex_vid:
                delete_edge(value_name, capability_vid_to_update, delete_vertex_vid)
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
                add_edge(value_name, '', capability_vid_to_update, add_vertex, '')
        elif value_name in vertex_value.keys():
            update_vertex('PropertyDefinition', capability_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'properties':
        if add_property_definition(type_update, varargs[2:], cluster_name, capability_vid_to_update, varargs[2]):
            update_property_definition(service_template_vid, capability_vid_to_update, value, value_name, varargs[2:],
                                       type_update, cluster_name)
    elif varargs[2] == 'attributes':
        if add_attribute_definition(type_update, varargs[2:], cluster_name, capability_vid_to_update, varargs[2]):
            update_attribute_definition(service_template_vid, capability_vid_to_update, value, value_name, varargs[2:],
                                        type_update, cluster_name)
    elif varargs[2] == 'occurrences':
        if add_occurrences(type_update, varargs[2:], cluster_name, capability_vid_to_update, varargs[2]):
            update_occurrences(capability_vid_to_update, value, value_name, varargs[2:], type_update, )
    else:
        abort(400)


def add_capability_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = CapabilityDefinition('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_capability_definition(father_node_vid, value, value_name, varargs: list):
    capability_vid_to_update = start_capability_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(capability_vid_to_update, 'CapabilityDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            return form_result(capability_vid_to_update, value_name)
        elif value_name == 'valid_source_type':
            destination = find_destination(capability_vid_to_update, value_name)
            if value is None:
                result = []
                for vid in destination:
                    result.append(vid.as_string())
                return result
            for vid in destination:
                destination_value = fetch_vertex(vid, 'NodeType')
                destination_value = destination_value.as_map()
                if value == destination_value.get('name'):
                    return vid.as_string()
            return None
        elif value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return capability_vid_to_update.as_string()
        else:
            abort(501)
    elif varargs[2] == 'properties':
        destination = find_destination(capability_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination)
        if flag:
            return result
        return get_property_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'attributes':
        destination = find_destination(capability_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination)
        if flag:
            return result
        return get_attribute_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'occurrences':
        destination = find_destination(capability_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination)
        if flag:
            return result
        return get_occurrences(father_node_vid, value, value_name, varargs[2:])
    else:
        abort(400)
