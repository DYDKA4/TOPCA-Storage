from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge
from nebula_communication.update_template.Definition.InterfaceDefinitionUpdater import update_interface_definition
from nebula_communication.update_template.Other.OccurrencesUpdater import update_occurrences


def update_trigger_definition(service_template_vid, father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    requirement_vid_to_update = None
    for requirement_vid in destination:
        requirement_value = fetch_vertex(requirement_vid, 'TriggerDefinition')
        requirement_value = requirement_value.as_map()
        if requirement_value.get('name').as_string() == varargs[1]:
            requirement_vid_to_update = requirement_vid
            break
    if requirement_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(requirement_vid_to_update, 'RequirementDefinition')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('RequirementDefinition', requirement_vid_to_update, value_name, value)
        else:
            abort(400)
    elif varargs[2] == 'event_filter':
        abort(501)
        # update_event_filter_definition(requirement_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'constraint':
        abort(501)
        # update_condition_clause_definition(requirement_vid_to_update, value, value_name, varargs[2:])
    else:
        abort(400)
