from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition
from nebula_communication.update_template.Definition.SchemaDefinitionUpdate import update_schema_definition
from nebula_communication.update_template.Other.ConstraintClauseUpdater import update_constraint_clause
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata


def update_data_type(father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    data_type_vid_to_update = None
    for data_type_vid in destination:
        data_type_value = fetch_vertex(data_type_vid, 'DataType')
        data_type_value = data_type_value.as_map()
        if data_type_value.get('name').as_string() == varargs[1]:
            data_type_vid_to_update = data_type_vid
            break
    if data_type_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(data_type_vid_to_update, 'DataType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            derived_from_vertex = find_destination(data_type_vid_to_update, value_name)
            new_derived_artifact_vid = None
            for data_type_vid in destination:
                data_type_value = fetch_vertex(data_type_vid, 'DataType')
                data_type_value = data_type_value.as_map()
                if '"' + data_type_value.get('name').as_string() + '"' == value:
                    new_derived_artifact_vid = data_type_vid
                    break
            if new_derived_artifact_vid is None:
                abort(400)
            if derived_from_vertex is not None:
                if len(derived_from_vertex) > 1:
                    abort(500)
                delete_edge(value_name, data_type_vid_to_update, derived_from_vertex[0])
            add_edge(value_name, '', data_type_vid_to_update, new_derived_artifact_vid, '')

        elif value_name in vertex_value.keys():
            update_vertex('DataType', data_type_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'properties':
        update_property_definition(father_node_vid, data_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'constraints':
        update_constraint_clause(data_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'metadata':
        update_metadata(data_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'key_schema':
        update_schema_definition(father_node_vid, data_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'entry_schema':
        update_schema_definition(father_node_vid, data_type_vid_to_update, value, value_name, varargs[2:])
    else:
        abort(400)
