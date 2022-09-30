import inspect

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template import NebulaCommunicationUpdateTemplateException
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import add_property_assignment, \
    update_property_assignment, get_property_assignment
from nebula_communication.update_template.Definition.InterfaceDefinitionUpdater import update_interface_definition, \
    add_interface_definition, get_interface_definition
from nebula_communication.update_template.Definition.NodeFilterDefinitionUpdater import update_node_filter_definition, \
    add_node_filter_definition, get_node_filter_definition
from nebula_communication.update_template.Other.OccurrencesUpdater import update_occurrences, add_occurrences, \
    get_occurrences
from nebula_communication.update_template.find_functions import return_all, form_result
from parser.parser.tosca_v_1_3.assignments.RequirementAssignment import RequirementAssignment


def start_requirement_assignment(father_node_vid, varargs):
    if len(varargs) < 2:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: varargs is too short')
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: destination is None')
    requirement_vid_to_update = None
    for requirement_vid in destination:
        requirement_value = fetch_vertex(requirement_vid, 'RequirementAssignment')
        requirement_value = requirement_value.as_map()
        if requirement_value.get('name').as_string() == varargs[1]:
            requirement_vid_to_update = requirement_vid
            break
    if requirement_vid_to_update is None:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: requirement_vid_to_update '
                                                              'is None')
    return requirement_vid_to_update


def update_requirement_assignment(service_template_vid, father_node_vid, value, value_name, varargs: list, type_update,
                                  cluster_name):
    requirement_vid_to_update = start_requirement_assignment(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + requirement_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(requirement_vid_to_update, 'RequirementAssignment')
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
                destination = find_destination(service_template_vid, 'topology_template')
                if destination is None:
                    raise NebulaCommunicationUpdateTemplateException(400,
                                                                     f'{inspect.stack()[0][3]}: destination is None')
                if len(destination) > 1:
                    raise NebulaCommunicationUpdateTemplateException(400,
                                                                     f'{inspect.stack()[0][3]}: destination len > 1')

                topology_template_vid = destination[0]
                destination = find_destination(topology_template_vid, 'relationship_templates')
                for relationship_template_vid in destination:
                    relationship_template_value = fetch_vertex(relationship_template_vid, 'RelationshipTemplate')
                    relationship_template_value = relationship_template_value.as_map()
                    if '"' + relationship_template_value.get('name').as_string() + '"' == value:
                        new_type_vid = relationship_template_vid
                        break
            if new_type_vid is None:
                raise NebulaCommunicationUpdateTemplateException(400,
                                                                 f'{inspect.stack()[0][3]}: new_type_vid is None')
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    raise NebulaCommunicationUpdateTemplateException(500,
                                                                     f'{inspect.stack()[0][3]}: type_vertex > 1')
                delete_edge(value_name, requirement_vid_to_update, type_vertex[0])
            add_edge(value_name, '', requirement_vid_to_update, new_type_vid, '')
        elif value_name == 'node':
            type_vertex = find_destination(requirement_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template_vid, 'node_types')
            for capability_type_vid in destination:
                capability_type_value = fetch_vertex(capability_type_vid, 'NodeType')
                capability_type_value = capability_type_value.as_map()
                if '"' + capability_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = capability_type_vid
                    break
            if new_type_vid is None:
                destination = find_destination(service_template_vid, 'topology_template')
                if destination is None:
                    raise NebulaCommunicationUpdateTemplateException(400,
                                                                     f'{inspect.stack()[0][3]}: destination is None')
                if len(destination) > 1:
                    raise NebulaCommunicationUpdateTemplateException(400,
                                                                     f'{inspect.stack()[0][3]}: destination len > 1')
                topology_template_vid = destination[0]
                destination = find_destination(topology_template_vid, 'node_templates')
                for relationship_template_vid in destination:
                    relationship_template_value = fetch_vertex(relationship_template_vid, 'NodeTemplate')
                    relationship_template_value = relationship_template_value.as_map()
                    if '"' + relationship_template_value.get('name').as_string() + '"' == value:
                        new_type_vid = relationship_template_vid
                        break
            if new_type_vid is None:
                raise NebulaCommunicationUpdateTemplateException(400,
                                                                 f'{inspect.stack()[0][3]}: destination is None')
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    raise NebulaCommunicationUpdateTemplateException(500,
                                                                     f'{inspect.stack()[0][3]}: type_vertex > 1')
                delete_edge(value_name, requirement_vid_to_update, type_vertex[0])
            add_edge(value_name, '', requirement_vid_to_update, new_type_vid, '')
        elif value_name == 'capability':
            type_vertex = find_destination(requirement_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template_vid, 'capability_types')
            for node_type_vid in destination:
                node_type_value = fetch_vertex(node_type_vid, 'CapabilityType')
                node_type_value = node_type_value.as_map()
                if '"' + node_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = node_type_vid
                    break
            if new_type_vid is None:
                node_vid = find_destination(requirement_vid_to_update, 'node')
                if node_vid is None:
                    raise NebulaCommunicationUpdateTemplateException(400,
                                                                     f'{inspect.stack()[0][3]}: node_vid is None')
                node_name = fetch_vertex(node_vid[0], 'NodeTemplate')
                node_name = node_name.as_map().get('name').as_string()

                destination = find_destination(service_template_vid, 'topology_template')
                if destination is None or len(destination) > 1:
                    raise NebulaCommunicationUpdateTemplateException(500,
                                                                     f'{inspect.stack()[0][3]}: destination is None '
                                                                     f'or len(destination) > 1')
                topology_template_vid = destination[0]
                destination = find_destination(topology_template_vid, 'node_templates')
                for node_template_vid in destination:
                    node_template_value = fetch_vertex(node_template_vid, 'NodeTemplate')
                    node_template_value = node_template_value.as_map()
                    if node_template_value.get('name').as_string() == node_name:
                        destination_capability = find_destination(node_template_vid, 'capabilities')
                        if destination_capability is None:
                            raise NebulaCommunicationUpdateTemplateException(400,
                                                                             f'{inspect.stack()[0][3]}: '
                                                                             f'destination_capability is None')
                        for capability_vid in destination_capability:
                            capability_value = fetch_vertex(capability_vid, 'CapabilityAssignment')
                            capability_value = capability_value.as_map()
                            if '"' + capability_value.get('name').as_string() + '"' == value:
                                new_type_vid = capability_vid
                                break
                        if new_type_vid:
                            break
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    raise NebulaCommunicationUpdateTemplateException(500,
                                                                     f'{inspect.stack()[0][3]}: type_vertex > 1')
                delete_edge(value_name, requirement_vid_to_update, type_vertex[0])
            add_edge(value_name, '', requirement_vid_to_update, new_type_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('RequirementAssignment', requirement_vid_to_update, value_name, value)
        else:
            raise NebulaCommunicationUpdateTemplateException(501, f'{inspect.stack()[0][3]}: Not implemented')
    elif varargs[2] == 'occurrences':
        if add_occurrences(type_update, varargs[2:], cluster_name, requirement_vid_to_update, varargs[2]):
            update_occurrences(requirement_vid_to_update, value, value_name, varargs[2:], type_update)
    elif varargs[2] == 'interfaces':
        if not add_interface_definition(type_update, varargs[2:], cluster_name, requirement_vid_to_update, varargs[2]):
            update_interface_definition(service_template_vid, requirement_vid_to_update, value, value_name, varargs[2:],
                                        type_update, cluster_name)
    elif varargs[2] == 'properties':
        if not add_property_assignment(type_update, varargs[2:], cluster_name, requirement_vid_to_update, varargs[2]):
            update_property_assignment(service_template_vid, requirement_vid_to_update, value, value_name, varargs[2:],
                                       type_update)
    elif varargs[2] == 'node_filter':
        if not add_node_filter_definition(type_update, varargs[2:], cluster_name, requirement_vid_to_update,
                                          varargs[2]):
            update_node_filter_definition(service_template_vid, requirement_vid_to_update, value, value_name,
                                          varargs[2:], type_update, cluster_name)
    else:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: wrong arguments')


def add_requirement_assignment(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = RequirementAssignment('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_requirement_assignment(father_node_vid, value, value_name, varargs: list):
    requirement_vid_to_update = start_requirement_assignment(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(requirement_vid_to_update, 'RequirementAssignment')
        vertex_value = vertex_value.as_map()
        if value_name == 'relationship':
            return form_result(requirement_vid_to_update, value_name)
        elif value_name == 'node':
            return form_result(requirement_vid_to_update, value_name)
        elif value_name == 'capability':
            return form_result(requirement_vid_to_update, value_name)
        elif value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return requirement_vid_to_update.as_string()
        else:
            raise NebulaCommunicationUpdateTemplateException(501, f'{inspect.stack()[0][3]}: Not implemented')
    elif varargs[2] == 'occurrences':
        destination = find_destination(requirement_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 3)
        if flag:
            return result
        return get_occurrences(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'interfaces':
        destination = find_destination(requirement_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_interface_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'properties':
        destination = find_destination(requirement_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_property_assignment(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'node_filter':
        destination = find_destination(requirement_vid_to_update, value_name)
        result, flag = return_all(value, value_name, destination, varargs, 4)
        if flag:
            return result
        return get_node_filter_definition(father_node_vid, value, value_name, varargs[2:])
    else:
        raise NebulaCommunicationUpdateTemplateException(400, f'{inspect.stack()[0][3]}: wrong arguments')
