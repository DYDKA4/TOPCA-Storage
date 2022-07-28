from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Assignment.RequirementAssignment import return_all, form_result
from nebula_communication.update_template.Definition.SchemaDefinitionUpdate import update_schema_definition, \
    add_schema_definition, get_schema_definition
from parser.parser.tosca_v_1_3.definitions.ParameterDefinition import ParameterDefinition


def start_parameter_definition(father_node_vid, varargs):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    property_vid_to_update = None
    for property_vid in destination:
        artifact_value = fetch_vertex(property_vid, 'ParameterDefinition')
        artifact_value = artifact_value.as_map()
        if artifact_value.get('name').as_string() == varargs[1]:
            property_vid_to_update = property_vid
            break
    if property_vid_to_update is None:
        abort(400)
    return property_vid_to_update


def update_parameter_definition(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update,
                                cluster_name):
    property_vid_to_update = start_parameter_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + property_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(property_vid_to_update, 'ParameterDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'value':
            value_name = 'values'
        if value_name == 'type':
            type_vertex = find_destination(property_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template_vid, 'data_types')
            for data_type_vid in destination:
                data_type_value = fetch_vertex(data_type_vid, 'DataType')
                data_type_value = data_type_value.as_map()
                if '"' + data_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = data_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, property_vid_to_update, type_vertex[0])
            add_edge(value_name, '', property_vid_to_update, new_type_vid, '')

        elif value_name in vertex_value.keys():
            update_vertex('ParameterDefinition', property_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'key_schema':
        if not add_schema_definition(type_update, varargs[2:], cluster_name, property_vid_to_update, varargs[2]):
            update_schema_definition(service_template_vid, property_vid_to_update, value, value_name, varargs[2:],
                                     type_update, cluster_name)
    elif varargs[2] == 'entry_schema':
        if not add_schema_definition(type_update, varargs[2:], cluster_name, property_vid_to_update, varargs[2]):
            update_schema_definition(service_template_vid, property_vid_to_update, value, value_name, varargs[2:],
                                     type_update, cluster_name)
    else:
        abort(400)


def add_parameter_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = ParameterDefinition('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_parameter_definition(father_node_vid, value, value_name, varargs: list):
    parameter_vid_to_update = start_parameter_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(parameter_vid_to_update, 'ParameterDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            return form_result(parameter_vid_to_update, value_name)
        elif value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return parameter_vid_to_update.as_string()
        else:
            abort(501)
    elif varargs[2] == 'key_schema':
        destination = find_destination(parameter_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 3)
        if flag:
            return result
        return get_schema_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'entry_schema':
        destination = find_destination(parameter_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 3)
        if flag:
            return result
        return get_schema_definition(father_node_vid, value, value_name, varargs[2:])
    else:
        abort(400)
