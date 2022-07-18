from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge
from nebula_communication.update_template.Definition.AttributeDefinitionUpdater import update_attribute_definition, \
    add_attribute_definition
from nebula_communication.update_template.Definition.CapabilityDefinitionUpdater import update_capability_definition
from nebula_communication.update_template.Definition.InterfaceDefinitionUpdater import update_interface_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition
from nebula_communication.update_template.Definition.RequirementDefinitionUpdater import update_requirement_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata


def update_node_type(father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    node_type_vid_to_update = None
    for node_type_vid in destination:
        node_type_value = fetch_vertex(node_type_vid, 'NodeType')
        node_type_value = node_type_value.as_map()
        if node_type_value.get('name').as_string() == varargs[1]:
            node_type_vid_to_update = node_type_vid
            break
    if node_type_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(node_type_vid_to_update, 'NodeType')
        vertex_value = vertex_value.as_map()
        if value_name == 'derived_from':
            derived_from_vertex = find_destination(node_type_vid_to_update, value_name)
            new_derived_relationship_vid = None
            for node_type_vid in destination:
                node_type_value = fetch_vertex(node_type_vid, 'NodeType')
                node_type_value = node_type_value.as_map()
                if '"' + node_type_value.get('name').as_string() + '"' == value:
                    new_derived_relationship_vid = node_type_vid
                    break
            if new_derived_relationship_vid is None:
                abort(400)
            if derived_from_vertex is not None:
                if len(derived_from_vertex) > 1:
                    abort(500)
                delete_edge(value_name, node_type_vid_to_update, derived_from_vertex[0])
            add_edge(value_name, '', node_type_vid_to_update, new_derived_relationship_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('InterfaceType', node_type_vid_to_update, value_name, value)
        else:
            abort(400)
    elif varargs[2] == 'metadata':
        update_metadata(node_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'attributes':
        if not add_attribute_definition(type_update, varargs[2:], cluster_name, node_type_vid_to_update,
                                        varargs[2]):
            update_attribute_definition(father_node_vid, node_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'properties':
        update_property_definition(father_node_vid, node_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'requirements':
        update_requirement_definition(father_node_vid, node_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'capabilities':
        update_capability_definition(father_node_vid, node_type_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'interfaces':
        update_interface_definition(father_node_vid, node_type_vid_to_update, value, value_name, varargs[2:])
    else:
        abort(400)
