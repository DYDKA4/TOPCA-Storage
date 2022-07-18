from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition, \
    add_property_definition
from nebula_communication.update_template.Definition.SchemaDefinitionUpdate import update_schema_definition
from nebula_communication.update_template.Other.ConstraintClauseUpdater import update_constraint_clause, \
    add_constraint_clause
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata, add_metadata
from parser.parser.tosca_v_1_3.types.DataType import DataType


def update_data_type(father_node_vid, value, value_name, varargs: list, type_update, cluster_name):
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
        if len(varargs) == 2:
            if type_update == 'delete':
                delete_vertex('"' + data_type_vid_to_update.as_string() + '"')
                return
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
        if not add_property_definition(type_update, varargs[2:], cluster_name, data_type_vid_to_update, varargs[2]):
            update_property_definition(father_node_vid, data_type_vid_to_update, value, value_name, varargs[2:],
                                       type_update, cluster_name)
    elif varargs[2] == 'constraints':
        if not add_constraint_clause(type_update, varargs[3:], cluster_name, data_type_vid_to_update, varargs[2]):
            update_constraint_clause(data_type_vid_to_update, value, value_name, varargs[2:], type_update)
    elif varargs[2] == 'metadata':
        if not add_metadata(type_update, varargs[2:], value, value_name, cluster_name, data_type_vid_to_update):
            update_metadata(data_type_vid_to_update, value, value_name, varargs[2:], type_update)
    elif varargs[2] == 'key_schema':
        update_schema_definition(father_node_vid, data_type_vid_to_update, value, value_name, varargs[2:], type_update)
    elif varargs[2] == 'entry_schema':
        update_schema_definition(father_node_vid, data_type_vid_to_update, value, value_name, varargs[2:], type_update)
    else:
        abort(400)


def add_artifact_type(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = DataType('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False
