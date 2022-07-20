from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Assignment.AttributeAssignmentUpdater import update_attribute_assignment, \
    add_attribute_assignment
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment, \
    add_property_assignment
from nebula_communication.update_template.Definition.InterfaceDefinitionUpdater import update_interface_definition, \
    add_interface_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata, add_metadata
from parser.parser.tosca_v_1_3.others.RelationshipTemplate import RelationshipTemplate


def update_relationship_template(service_template, father_node_vid, value, value_name, varargs: list, type_update,
                                 cluster_name):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    relationship_template_vid_to_update = None
    for relationship_template_vid in destination:
        relationship_template_value = fetch_vertex(relationship_template_vid, 'RelationshipTemplate')
        relationship_template_value = relationship_template_value.as_map()
        if relationship_template_value.get('name').as_string() == varargs[1]:
            relationship_template_vid_to_update = relationship_template_vid
            break
    if relationship_template_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + relationship_template_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(relationship_template_vid_to_update, 'RelationshipTemplate')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            type_vertex = find_destination(relationship_template_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template, 'relationship_types')
            for data_type_vid in destination:
                data_type_value = fetch_vertex(data_type_vid, 'RelationshipType')
                data_type_value = data_type_value.as_map()
                if '"' + data_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = data_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, relationship_template_vid_to_update, type_vertex[0])
            add_edge(value_name, '', relationship_template_vid_to_update, new_type_vid, '')
        elif value_name == 'copy':
            copy_from_vertex = find_destination(relationship_template_vid_to_update, value_name)
            new_derived_relationship_vid = None
            for relationship_template_vid in destination:
                relationship_template_value = fetch_vertex(relationship_template_vid, 'RelationshipTemplate')
                relationship_template_value = relationship_template_value.as_map()
                if '"' + relationship_template_value.get('name').as_string() + '"' == value:
                    new_derived_relationship_vid = relationship_template_vid
                    break
            if new_derived_relationship_vid is None:
                abort(400)
            if copy_from_vertex is not None:
                if len(copy_from_vertex) > 1:
                    abort(500)
                delete_edge(value_name, relationship_template_vid_to_update, copy_from_vertex[0])
            add_edge(value_name, '', relationship_template_vid_to_update, new_derived_relationship_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('InterfaceType', relationship_template_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'properties':
        if not add_property_assignment(type_update, varargs, value, value_name, cluster_name,
                                       relationship_template_vid_to_update):
            update_property_assignment(service_template, relationship_template_vid_to_update, value, value_name,
                                       varargs[2:], type_update)
    elif varargs[2] == 'metadata':
        if not add_metadata(type_update, varargs[2:], value, value_name, cluster_name,
                            relationship_template_vid_to_update):
            update_metadata(relationship_template_vid_to_update, value, value_name, varargs[2:], type_update)
    elif varargs[2] == 'interfaces':
        if not add_interface_definition(type_update, varargs[2:], cluster_name, relationship_template_vid_to_update,
                                        varargs[2]):
            update_interface_definition(service_template, relationship_template_vid_to_update, value, value_name,
                                        varargs[2:], type_update, cluster_name)
    elif varargs[2] == 'attributes':
        if not add_attribute_assignment(type_update, varargs[2:], cluster_name, relationship_template_vid_to_update,
                                        varargs[2]):
            update_attribute_assignment(service_template, relationship_template_vid_to_update, value, value_name,
                                        varargs[2:], type_update)
    else:
        abort(400)


def add_relationship_template(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = RelationshipTemplate('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False
