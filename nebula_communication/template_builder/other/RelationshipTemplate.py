from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.assignment.AttributeAssignment import construct_attribute_assignment
from nebula_communication.template_builder.assignment.PropertyAssignment import construct_property_assignment
from nebula_communication.template_builder.definition.InterfaceDefinition import construct_interface_definition
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from parser.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate


def construct_relationship_template(list_of_vid, only) -> dict:
    result = {}
    relationship_type = RelationshipTemplate('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'RelationshipTemplate')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(relationship_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'type':
                derived_from = fetch_vertex(destination[0], 'RelationshipType')
                derived_from = derived_from.as_map()
                derived_from = derived_from['name'].as_string()
                tmp_result['type'] = derived_from
            elif edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            elif edge == 'properties':
                tmp_result['properties'] = construct_property_assignment(destination, only)
            elif edge == 'attributes':
                tmp_result['attributes'] = construct_attribute_assignment(destination, only)
            elif edge == 'interfaces':
                tmp_result['interfaces'] = construct_interface_definition(destination, only)
            elif edge == 'copy':
                if destination:
                    copy = fetch_vertex(destination[0], 'RelationshipTemplate')
                    copy = copy.as_map()
                    copy = copy['name'].as_string()
                    tmp_result['copy'] = copy
            else:
                print(edge)
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result
