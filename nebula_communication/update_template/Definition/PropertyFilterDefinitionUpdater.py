from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Definition.SchemaDefinitionUpdate import update_schema_definition
from nebula_communication.update_template.Other.ConstraintClauseUpdater import update_constraint_clause, \
    add_constraint_clause
from parser.parser.tosca_v_1_3.definitions.PropertyFilterDefinition import PropertyFilterDefinition


def update_property_filter_definition(service_template_vid, father_node_vid, value, value_name, varargs: list,
                                      type_update, cluster_name):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None or len(destination) > 1:
        abort(400)
    property_filter_vid_to_update = None
    for property_vid in destination:
        property_filter_value = fetch_vertex(property_vid, 'PropertyFilterDefinition')
        property_filter_value = property_filter_value.as_map()
        if property_filter_value.get('name').as_string() == varargs[1]:
            property_filter_vid_to_update = property_vid
            break
    if property_filter_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + property_filter_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(property_filter_vid_to_update, 'PropertyFilterDefinition')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('PropertyFilterDefinition', property_filter_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'property_constraint':
        if not add_constraint_clause(type_update, varargs[2:], cluster_name, property_filter_vid_to_update, varargs[2]):
            update_constraint_clause(property_filter_vid_to_update, value, value_name,
                                     varargs[2:],type_update)
    else:
        abort(400)


def add_property_filter_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = PropertyFilterDefinition('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False
