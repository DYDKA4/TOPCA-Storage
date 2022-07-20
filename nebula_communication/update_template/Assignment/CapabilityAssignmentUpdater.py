from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment, \
    add_property_assignment


def update_capability_assignment(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update,
                                 cluster_name):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None or len(destination) > 1:
        abort(400)
    capability_vid_to_update = None
    for capability_vid in destination:
        capability_value = fetch_vertex(capability_vid, 'CapabilityAssignment')
        capability_value = capability_value.as_map()
        if capability_value.get('name').as_string() == varargs[1]:
            capability_vid_to_update = capability_vid
            break
    if capability_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(capability_vid_to_update, 'CapabilityAssignment')
        vertex_value = vertex_value.as_map()
        if value_name in vertex_value.keys():
            update_vertex('CapabilityAssignment', capability_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'properties':
        if not add_property_assignment(type_update, varargs, value, value_name, cluster_name, capability_vid_to_update):
            update_property_assignment(service_template_vid, capability_vid_to_update, value, value_name,
                                       varargs[2:], type_update)
    else:
        abort(400)
