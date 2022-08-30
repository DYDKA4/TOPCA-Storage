from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.DeepUpdate import deep_update_dict
from nebula_communication.template_builder.assignment.PropertyAssignment import construct_property_assignment
from nebula_communication.template_builder.definition.InterfaceDefinition import construct_interface_definition
from nebula_communication.template_builder.definition.NodeFilterDefinition import construct_node_filter_definition
from parser.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment


def construct_requirement_assignment(list_of_vid, only) -> list:
    result = []
    requirement_assignment = RequirementAssignment('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'RequirementAssignment')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        for vertex_key in vertex_keys:
            if not vertex_value[vertex_key].is_null() and vertex_key not in {'vertex_type_system', 'name'}:
                tmp_result[vertex_key] = vertex_value[vertex_key].as_string()
        edges = set(requirement_assignment.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'capability':
                if destination:
                    capability = None
                    if fetch_vertex(destination[0], 'CapabilityType'):
                        capability = fetch_vertex(destination[0], 'CapabilityType')
                    elif fetch_vertex(destination[0], 'CapabilityDefinition'):
                        capability = fetch_vertex(destination[0], 'CapabilityDefinition')
                    else:
                        abort(500)
                    capability = capability.as_map()
                    capability = capability['name'].as_string()
                    tmp_result['capability'] = capability
            elif edge == 'node':
                if destination:
                    node = None
                    if fetch_vertex(destination[0], 'NodeType'):
                        node = fetch_vertex(destination[0], 'NodeType')
                    elif fetch_vertex(destination[0], 'NodeTemplate'):
                        node = fetch_vertex(destination[0], 'NodeTemplate')
                    else:
                        abort(500)
                    node = node.as_map()
                    node = node['name'].as_string()
                    tmp_result['node'] = node
            elif edge == 'relationship':
                if destination:
                    relationship = None
                    if fetch_vertex(destination[0], 'RelationshipType'):
                        relationship = fetch_vertex(destination[0], 'RelationshipType')
                    elif fetch_vertex(destination[0], 'RelationshipTemplate'):
                        relationship = fetch_vertex(destination[0], 'RelationshipTemplate')
                    else:
                        abort(500)
                    relationship = relationship.as_map()
                    relationship = relationship['name'].as_string()
                    if tmp_result.get('relationship'):
                        deep_update_dict(tmp_result['relationship'], {'type': relationship})
                    else:
                        tmp_result['relationship'] = {'type': relationship}
            elif edge == 'properties':
                if destination:
                    properties = construct_property_assignment(destination, only)
                    if tmp_result.get('relationship'):
                        deep_update_dict(tmp_result['relationship'], {'properties': properties})
                    else:
                        tmp_result['relationship'] = {'properties': properties}
            elif edge == 'interfaces':
                interfaces = construct_interface_definition(destination, only)
                if tmp_result.get('relationship'):
                    deep_update_dict(tmp_result['relationship'], {'interfaces': interfaces})
                else:
                    tmp_result['relationship'] = {'interfaces': interfaces}
            elif edge == 'occurrences':
                if destination:
                    relationship = fetch_vertex(destination[0], 'Occurrences')
                    relationship = relationship.as_map()
                    minimum: str = relationship['minimum'].as_string()
                    maximum: str = relationship['maximum'].as_string()
                    if minimum.isnumeric():
                        minimum: int = int(minimum)
                    elif minimum.replace('.', '', 1).isdigit():
                        minimum: float = float(minimum)

                    if maximum.isnumeric():
                        maximum: int = int(maximum)
                    elif maximum.replace('.', '', 1).isdigit():
                        maximum: float = float(maximum)
                    tmp_result['occurrences'] = [minimum, maximum]
            elif edge == 'node_filter':
                tmp_result['node_filter'] = construct_node_filter_definition(destination)
            else:
                print(edge)
                abort(500)
        requirement = {vertex_value['name'].as_string():  tmp_result}
        result.append(requirement)

    return result
