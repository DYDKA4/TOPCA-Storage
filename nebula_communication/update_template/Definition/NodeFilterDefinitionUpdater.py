from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge
from nebula_communication.update_template.Definition.CapabilityFilterDefinition import \
    update_capability_filter_definition
from nebula_communication.update_template.Definition.PropertyFilterDefinitionUpdater import \
    update_property_filter_definition


def update_node_filter_definition(service_template_vid, father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None or len(destination) > 1:
        abort(400)
    node_filter_vid_to_update = destination[0]
    if node_filter_vid_to_update is None:
        abort(400)
    elif varargs[1] == 'properties':
        update_property_filter_definition(service_template_vid, node_filter_vid_to_update, value, value_name,
                                          varargs[1:])
    elif varargs[1] == 'capability':
        update_capability_filter_definition(service_template_vid, node_filter_vid_to_update, value, value_name,
                                            varargs[1:])
    else:
        abort(400)
