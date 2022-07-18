from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex
from nebula_communication.update_template.Other.ConstraintClauseUpdater import update_constraint_clause


def update_schema_definition(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update):
    if len(varargs) < 1:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None or len(destination) > 1:
        abort(400)
    schema_vid_to_update = destination[0]
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
            update_schema_definition(service_template_vid, schema_vid_to_update, value, value_name, varargs[1:],
                                     type_update)
        elif varargs[1] == 'entry_schema':
            update_schema_definition(service_template_vid, schema_vid_to_update, value, value_name, varargs[1:],
                                     type_update)
        elif varargs[1] == 'constraints':
            update_constraint_clause(schema_vid_to_update, value, value_name, varargs[1:], type_update)
        else:
            abort(400)
    else:
        abort(400)

