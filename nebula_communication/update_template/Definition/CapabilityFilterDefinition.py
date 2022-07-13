from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge
from nebula_communication.update_template.Definition.PropertyFilterDefinitionUpdater import \
    update_property_filter_definition


def update_capability_filter_definition(service_template_vid, father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None or len(destination) > 1:
        abort(400)
    capability_filter_vid_to_update = None
    for capability_vid in destination:
        capability_filter_value = fetch_vertex(capability_vid, 'CapabilityFilterDefinition')
        capability_filter_value = capability_filter_value.as_map()
        if capability_filter_value.get('name').as_string() == varargs[1]:
            capability_filter_vid_to_update = capability_vid
            break
    if capability_filter_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(capability_filter_vid_to_update, 'CapabilityFilterDefinition')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('CapabilityFilterDefinition', capability_filter_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'properties':
        update_property_filter_definition(service_template_vid, capability_filter_vid_to_update, value, value_name,
                                          varargs[2:])
    else:
        abort(400)
