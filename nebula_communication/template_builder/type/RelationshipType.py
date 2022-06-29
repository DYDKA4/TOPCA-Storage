from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.definition.AttributeDefinition import construct_attribute_definition
from nebula_communication.template_builder.definition.InterfaceDefinition import construct_interface_definition
from nebula_communication.template_builder.definition.MetadataDefinition import construct_metadata_definition
from nebula_communication.template_builder.definition.NotificationDefinition import construct_notification_definition
from nebula_communication.template_builder.definition.OperationDefinition import construct_operation_definition
from nebula_communication.template_builder.definition.ProperyDefinition import construct_property_definition

from parser.parser.tosca_v_1_3.types.RelationshipType import RelationshipType


def construct_relationship_type(list_of_vid) -> dict:
    result = {}
    relationship_type = RelationshipType('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'RelationshipType')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(relationship_type.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'derived_from':
                if destination:
                    derived_from = fetch_vertex(destination[0], 'RelationshipType')
                    derived_from = derived_from.as_map()
                    derived_from = derived_from['name'].as_string()
                    tmp_result['derived_from'] = derived_from
            elif edge == 'metadata':
                tmp_result['metadata'] = construct_metadata_definition(destination)
            elif edge == 'properties':
                tmp_result['properties'] = construct_property_definition(destination)
            elif edge == 'attributes':
                tmp_result['attributes'] = construct_attribute_definition(destination)
            elif edge == 'interfaces':
                tmp_result['interfaces'] = construct_interface_definition(destination)
            elif edge == 'valid_target_types':
                valid_target_types = []
                for valid_target in destination:
                    valid_target = fetch_vertex(valid_target, 'CapabilityType')
                    valid_target = valid_target.as_map()
                    valid_target = valid_target['name'].as_string()
                    valid_target_types.append(valid_target)
                tmp_result['valid_target_types'] = valid_target_types
            else:
                print(edge)
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result
