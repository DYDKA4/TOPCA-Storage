from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge
from nebula_communication.update_template.Definition.SchemaDefinitionUpdate import update_schema_definition


def update_attribute_definition(service_template_vid, father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    property_vid_to_update = None
    for attribute_vid in destination:
        attribute_value = fetch_vertex(attribute_vid, 'AttributeDefinition')
        attribute_value = attribute_value.as_map()
        if attribute_value.get('name').as_string() == varargs[1]:
            property_vid_to_update = attribute_vid
            break
    if property_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(property_vid_to_update, 'AttributeDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            type_vertex = find_destination(property_vid_to_update, value_name)
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
                delete_edge(value_name, property_vid_to_update, type_vertex[0])
            add_edge(value_name, '', property_vid_to_update, new_type_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('AttributeDefinition', property_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'key_schema':
        update_schema_definition(service_template_vid, property_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'entry_schema':
        update_schema_definition(service_template_vid, property_vid_to_update, value, value_name, varargs[2:])
    else:
        abort(400)
