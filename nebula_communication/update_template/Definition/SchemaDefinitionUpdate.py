from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Other.ConstraintClauseUpdater import update_constraint_clause, \
    add_constraint_clause
from parser.parser.tosca_v_1_3.definitions.SchemaDefinition import SchemaDefinition


def update_schema_definition(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update,
                             cluster_name):
    if len(varargs) < 1:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    if len(destination) > 1:
        if type_update == 'delete':
            for destination_vid in destination:
                delete_vertex('"' + destination_vid.as_string() + '"')
            return
        else:
            abort(400)
    schema_vid_to_update = destination[0]
    if type_update == 'delete':
        delete_vertex('"' + schema_vid_to_update.as_string() + '"')
        return
    if len(varargs) == 1:
        vertex_value = fetch_vertex(schema_vid_to_update, 'SchemaDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            type_vertex = find_destination(schema_vid_to_update, value_name)
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
                delete_edge(value_name, schema_vid_to_update, type_vertex[0])
            add_edge(value_name, '', schema_vid_to_update, new_type_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('SchemaDefinition', schema_vid_to_update, value_name, value)
        else:
            abort(501)
    elif len(varargs) > 1:
        if varargs[1] == 'key_schema':
            if not add_schema_definition(type_update, varargs[1:], cluster_name, schema_vid_to_update, varargs[0]):
                update_schema_definition(service_template_vid, schema_vid_to_update, value, value_name, varargs[1:],
                                         type_update, cluster_name)
        elif varargs[1] == 'entry_schema':
            if not add_schema_definition(type_update, varargs[1:], cluster_name, schema_vid_to_update, varargs[0]):
                update_schema_definition(service_template_vid, schema_vid_to_update, value, value_name, varargs[1:],
                                         type_update, cluster_name)
        elif varargs[1] == 'constraints':
            if not add_constraint_clause(type_update, varargs[1:], cluster_name, schema_vid_to_update, varargs[0]):
                update_constraint_clause(schema_vid_to_update, value, value_name, varargs[1:], type_update)
        else:
            abort(400)
    else:
        abort(400)


def add_schema_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 1:
        schema_definition = SchemaDefinition()
        generate_uuid(schema_definition, cluster_name)
        add_in_vertex(schema_definition.vertex_type_system, 'vertex_type_system',
                      '"' + schema_definition.vertex_type_system + '"', schema_definition.vid)
        add_edge(edge_name, '', parent_vid, schema_definition.vid, '')
        return True
    return False
