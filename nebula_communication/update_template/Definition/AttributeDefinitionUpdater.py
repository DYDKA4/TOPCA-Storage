from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    add_in_vertex, delete_vertex
from nebula_communication.update_template.Definition.SchemaDefinitionUpdate import update_schema_definition, \
    add_schema_definition
from parser.parser.tosca_v_1_3.definitions.AttributeDefinition import AttributeDefinition


def update_attribute_definition(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update,
                                cluster_name):
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
        if type_update == 'delete':
            delete_vertex('"' + property_vid_to_update.as_string() + '"')
            return
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
        if not add_schema_definition(type_update, varargs[2:], cluster_name, property_vid_to_update, varargs[2]):

            update_schema_definition(service_template_vid, property_vid_to_update, value, value_name, varargs[2:],
                                     type_update, cluster_name)
    elif varargs[2] == 'entry_schema':
        if not add_schema_definition(type_update, varargs[2:], cluster_name, property_vid_to_update, varargs[2]):

            update_schema_definition(service_template_vid, property_vid_to_update, value, value_name, varargs[2:],
                                     type_update, cluster_name)
    else:
        abort(400)


def add_attribute_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        import_definition = AttributeDefinition('"' + varargs[1] + '"')
        generate_uuid(import_definition, cluster_name)
        add_in_vertex(import_definition.vertex_type_system, 'name, vertex_type_system',
                      import_definition.name + ',"' + import_definition.vertex_type_system + '"', import_definition.vid)
        add_edge(edge_name, '', parent_vid, import_definition.vid, '')
        return True
    return False
