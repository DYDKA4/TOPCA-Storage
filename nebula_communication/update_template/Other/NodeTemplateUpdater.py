from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, add_edge, delete_edge
from nebula_communication.update_template.Assignment.AttributeAssignmentUpdater import update_attribute_assignment
from nebula_communication.update_template.Assignment.CapabilityAssignmentUpdater import update_capability_assignment
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment, \
    add_property_assignment
from nebula_communication.update_template.Definition.ArtifactDefinition import update_artifact_definition
from nebula_communication.update_template.Definition.AttributeDefinitionUpdater import update_attribute_definition
from nebula_communication.update_template.Definition.CapabilityDefinitionUpdater import update_capability_definition
from nebula_communication.update_template.Definition.InterfaceDefinitionUpdater import update_interface_definition
from nebula_communication.update_template.Definition.NodeFilterDefinitionUpdater import update_node_filter_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition
from nebula_communication.update_template.Definition.RequirementDefinitionUpdater import update_requirement_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata


def update_node_template(service_template, father_node_vid, value, value_name, varargs: list, type_update,
                         cluster_name):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    node_template_vid_to_update = None
    for node_template_vid in destination:
        node_template_value = fetch_vertex(node_template_vid, 'NodeTemplate')
        node_template_value = node_template_value.as_map()
        if node_template_value.get('name').as_string() == varargs[1]:
            node_template_vid_to_update = node_template_vid
            break
    if node_template_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(node_template_vid_to_update, 'NodeTemplate')
        vertex_value = vertex_value.as_map()
        if value_name == 'type':
            type_vertex = find_destination(node_template_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(service_template, 'node_types')
            for data_type_vid in destination:
                data_type_value = fetch_vertex(data_type_vid, 'NodeType')
                data_type_value = data_type_value.as_map()
                if '"' + data_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = data_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, node_template_vid_to_update, type_vertex[0])
            add_edge(value_name, '', node_template_vid_to_update, new_type_vid, '')
        elif value_name == 'copy':
            type_vertex = find_destination(node_template_vid_to_update, value_name)
            new_type_vid = None
            destination = find_destination(find_destination(service_template, 'topology_template')[0], 'node_templates')
            for data_type_vid in destination:
                data_type_value = fetch_vertex(data_type_vid, 'NodeTemplate')
                data_type_value = data_type_value.as_map()
                if '"' + data_type_value.get('name').as_string() + '"' == value:
                    new_type_vid = data_type_vid
                    break
            if new_type_vid is None:
                abort(400)
            if type_vertex is not None:
                if len(type_vertex) > 1:
                    abort(500)
                delete_edge(value_name, node_template_vid_to_update, type_vertex[0])
            add_edge(value_name, '', node_template_vid_to_update, new_type_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('NodeTemplate', node_template_vid_to_update, value_name, value)
        else:
            abort(400)
    elif varargs[2] == 'metadata':
        update_metadata(node_template_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'attributes':
        update_attribute_assignment(service_template, node_template_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'properties':
        if not add_property_assignment(type_update, varargs, value, value_name, cluster_name,
                                       node_template_vid_to_update):
            update_property_assignment(service_template, node_template_vid_to_update, value, value_name, varargs[2:],
                                       type_update)
    elif varargs[2] == 'requirements':
        update_requirement_definition(service_template, node_template_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'capabilities':
        update_capability_assignment(service_template, node_template_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'interfaces':
        update_interface_definition(service_template, node_template_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'artifacts':
        update_artifact_definition(service_template, node_template_vid_to_update, value, value_name, varargs[2:])
    elif varargs[2] == 'node_filter':
        update_node_filter_definition(service_template, node_template_vid_to_update, value, value_name, varargs[2:])
    else:
        abort(400)
