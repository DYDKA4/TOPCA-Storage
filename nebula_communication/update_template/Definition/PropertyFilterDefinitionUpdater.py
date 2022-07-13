from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge
from nebula_communication.update_template.Definition.SchemaDefinitionUpdate import update_schema_definition
from nebula_communication.update_template.Other.ConstraintClauseUpdater import update_constraint_clause


def update_property_filter_definition(service_template_vid, father_node_vid, value, value_name, varargs: list):
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
        vertex_value = fetch_vertex(property_filter_vid_to_update, 'PropertyFilterDefinition')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('PropertyFilterDefinition', property_filter_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'property_constraint':
        update_constraint_clause(property_filter_vid_to_update, value, value_name,
                                 varargs[2:])
    else:
        abort(400)
