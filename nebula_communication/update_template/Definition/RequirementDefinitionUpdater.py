from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge
from nebula_communication.update_template.Definition.InterfaceDefinitionUpdater import update_interface_definition, \
    add_interface_definition
from nebula_communication.update_template.Other.OccurrencesUpdater import update_occurrences


def update_requirement_definition(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update,
                                  cluster_name):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    requirement_vid_to_update = None
    for requirement_vid in destination:
        requirement_value = fetch_vertex(requirement_vid, 'RequirementDefinition')
        requirement_value = requirement_value.as_map()
        if requirement_value.get('name').as_string() == varargs[1]:
            requirement_vid_to_update = requirement_vid
            break
    if requirement_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(requirement_vid_to_update, 'RequirementDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'relationship':
            type_vertex = find_destination(requirement_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template_vid, 'relationship_types')
            for relationship_type_vid in destination:
                relationship_type_value = fetch_vertex(relationship_type_vid, 'RelationshipType')
                relationship_type_value = relationship_type_value.as_map()
                if '"' + relationship_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = relationship_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, requirement_vid_to_update, type_vertex[0])
            add_edge(value_name, '', requirement_vid_to_update, new_type_vid, '')
        elif value_name == 'capability':
            type_vertex = find_destination(requirement_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template_vid, 'capability_types')
            for capability_type_vid in destination:
                capability_type_value = fetch_vertex(capability_type_vid, 'CapabilityType')
                capability_type_value = capability_type_value.as_map()
                if '"' + capability_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = capability_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, requirement_vid_to_update, type_vertex[0])
            add_edge(value_name, '', requirement_vid_to_update, new_type_vid, '')
        elif value_name == 'node':
            type_vertex = find_destination(requirement_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template_vid, 'node_types')
            for node_type_vid in destination:
                node_type_value = fetch_vertex(node_type_vid, 'NodeType')
                node_type_value = node_type_value.as_map()
                if '"' + node_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = node_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, requirement_vid_to_update, type_vertex[0])
            add_edge(value_name, '', requirement_vid_to_update, new_type_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('RequirementDefinition', requirement_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'occurrences':
        update_occurrences(requirement_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'interfaces':
        if not add_interface_definition(type_update, varargs[2:], cluster_name, requirement_vid_to_update, varargs[2]):
            update_interface_definition(service_template_vid, requirement_vid_to_update, value, value_name, varargs[2:],
                                        type_update, cluster_name)
    else:
        abort(400)
