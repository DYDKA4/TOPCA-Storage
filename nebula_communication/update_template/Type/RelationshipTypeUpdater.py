from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge
from nebula_communication.update_template.Definition.InterfaceDefinitionUpdater import update_interface_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata


def update_relationship_type(father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    relationship_type_vid_to_update = None
    for relationship_type_vid in destination:
        relationship_type_value = fetch_vertex(relationship_type_vid, 'RelationshipType')
        relationship_type_value = relationship_type_value.as_map()
        if relationship_type_value.get('name').as_string() == varargs[1]:
            relationship_type_vid_to_update = relationship_type_vid
            break
    if relationship_type_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(relationship_type_vid_to_update, 'RelationshipType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            derived_from_vertex = find_destination(relationship_type_vid_to_update, value_name)
            new_derived_relationship_vid = None
            for relationship_type_vid in destination:
                relationship_type_value = fetch_vertex(relationship_type_vid, 'RelationshipType')
                relationship_type_value = relationship_type_value.as_map()
                if '"' + relationship_type_value.get('name').as_string() + '"' == value:
                    new_derived_relationship_vid = relationship_type_vid
                    break
            if new_derived_relationship_vid is None:
                abort(400)
            if derived_from_vertex is not None:
                if len(derived_from_vertex) > 1:
                    abort(500)
                delete_edge(value_name, relationship_type_vid_to_update, derived_from_vertex[0])
            add_edge(value_name, '', relationship_type_vid_to_update, new_derived_relationship_vid, '')
        elif value_name == 'valid_source_type':
            valid_source_type_vertexes = find_destination(relationship_type_vid_to_update, value_name)
            delete_vertex = None
            for valid_source_type_vid in valid_source_type_vertexes:
                valid_source_value = fetch_vertex(valid_source_type_vid, 'NodeType')
                valid_source_value = valid_source_value.as_map()
                if '"' + valid_source_value.get('name').as_string() + '"' == value:
                    delete_vertex = valid_source_type_vid
                    break
            if delete_vertex:
                delete_edge(value_name, relationship_type_vid_to_update, delete_vertex)
            else:
                add_vertex = None
                node_types_vertexes = find_destination(father_node_vid, 'node_types')
                if node_types_vertexes is None:
                    abort(500)
                for node_types_vertex in node_types_vertexes:
                    node_types_value = fetch_vertex(node_types_vertex, 'NodeType')
                    node_types_value = node_types_value.as_map()
                    if '"' + node_types_value.get('name').as_string() + '"' == value:
                        add_vertex = node_types_vertex
                        break
                if add_vertex is None:
                    abort(400)
                add_edge(value_name, '', relationship_type_vid_to_update, add_vertex, '')
        elif value_name in vertex_value.keys():
            update_vertex('InterfaceType', relationship_type_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'properties':
        update_property_definition(father_node_vid, relationship_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'metadata':
        update_metadata(relationship_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'interfaces':
        update_interface_definition(father_node_vid, relationship_type_vid_to_update, value, value_name, varargs[2:])
    else:
        abort(400)
