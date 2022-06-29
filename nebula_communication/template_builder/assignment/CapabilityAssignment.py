from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from nebula_communication.template_builder.assignment.AttributeAssignment import construct_attribute_assignment
from nebula_communication.template_builder.assignment.PropertyAssignment import construct_property_assignment
from parser.parser.tosca_v_1_3.assignments.CapabilityAssignment import CapabilityAssignment


def construct_capability_assignment(list_of_vid) -> dict:
    result = {}
    capability_definition = CapabilityAssignment('name').__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'CapabilityAssignment')
        vertex_value = vertex_value.as_map()
        tmp_result = {}
        vertex_keys = vertex_value.keys()
        edges = set(capability_definition.keys()) - set(vertex_keys) - {'vid'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'properties':
                tmp_result['properties'] = construct_property_assignment(destination)
            elif edge == 'attributes':
                tmp_result['attributes'] = construct_attribute_assignment(destination)
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
            else:
                abort(500)
        result[vertex_value['name'].as_string()] = tmp_result

    return result
