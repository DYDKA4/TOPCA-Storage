from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, update_vertex, find_destination


def update_attribute_assignment(service_template_vid, father_node_vid, value, value_name, varargs: list):
    if len(varargs) != 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    property_vid_to_update = None
    for property_vid in destination:
        property_value = fetch_vertex(property_vid, 'AttributeAssignment')
        property_value = property_value.as_map()
        if property_value.get('name').as_string() == varargs[1]:
            property_vid_to_update = property_vid
            break
    if property_vid_to_update is None:
        abort(400)
    if value_name == 'value':
        value_name = 'values'
    property_value = fetch_vertex(property_vid_to_update, 'AttributeAssignment')
    property_value = property_value.as_map()
    if value_name in property_value.keys():
        update_vertex('PropertyAssignment', property_vid_to_update, value_name, value)
    else:
        abort(400)