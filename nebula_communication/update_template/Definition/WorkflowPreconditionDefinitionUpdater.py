from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    delete_vertex, add_in_vertex
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment
from nebula_communication.update_template.Definition.InterfaceDefinitionUpdater import update_interface_definition
from nebula_communication.update_template.Definition.OperationImplementationDefinitionUpdater import \
    update_operation_implementation_definition
from nebula_communication.update_template.Other.MetadataUpdater import update_metadata
from nebula_communication.update_template.Other.OccurrencesUpdater import update_occurrences
from parser.parser.tosca_v_1_3.definitions.WorkflowPreconditionDefinition import WorkflowPreconditionDefinition


def update_workflow_precondition_definition(service_template_vid, father_node_vid, value, value_name, varargs: list,
                                            type_update):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    if len(destination) > 1:
        if type_update == 'delete':
            for destination_vid in destination:
                delete_vertex('"' + destination_vid.as_string() + '"')
            return
        else:
            abort(400)
    workflow_precondition_vid_to_update = destination[0]
    if workflow_precondition_vid_to_update is None:
        abort(400)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + workflow_precondition_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(workflow_precondition_vid_to_update, 'WorkflowPreconditionDefinition')
        vertex_value = vertex_value.as_map()
        topology_template = find_destination(service_template_vid, 'topology_template')
        if value_name == 'target':
            target_vertex = find_destination(workflow_precondition_vid_to_update, value_name)
            new_target_vid = None
            destination = find_destination(topology_template, 'groups')
            for group_definition_vid in destination:
                relationship_template_value = fetch_vertex(group_definition_vid, 'GroupDefinition')
                relationship_template_value = relationship_template_value.as_map()
                if '"' + relationship_template_value.get('name').as_string() + '"' == value:
                    new_target_vid = group_definition_vid
                    break
            if new_target_vid is None:
                destination = find_destination(topology_template, 'node_templates')
                for node_template_vid in destination:
                    node_template_value = fetch_vertex(node_template_vid, 'NodeTemplate')
                    node_template_value = node_template_value.as_map()
                    if '"' + node_template_value.get('name').as_string() + '"' == value:
                        new_target_vid = node_template_value
                        break
            if new_target_vid is None:
                abort(400)
            if target_vertex is not None:
                if len(target_vertex) > 1:
                    abort(500)
                delete_edge(value_name, workflow_precondition_vid_to_update, target_vertex[0])
            add_edge(value_name, '', workflow_precondition_vid_to_update, new_target_vid, '')
        elif value_name == 'target_relationship':
            target_relationship_vertex = find_destination(workflow_precondition_vid_to_update, value_name)
            new_target_relationship_vid = None
            destination = find_destination(topology_template, 'relationship_template')
            for relationship_template_vid in destination:
                relationship_template_value = fetch_vertex(relationship_template_vid, 'RelationshipTemplate')
                relationship_template_value = relationship_template_value.as_map()
                if '"' + relationship_template_value.get('name').as_string() + '"' == value:
                    new_target_relationship_vid = relationship_template_vid
                    break
            if new_target_relationship_vid is None:
                abort(400)
            if target_relationship_vertex is not None:
                if len(target_relationship_vertex) > 1:
                    abort(500)
                delete_edge(value_name, workflow_precondition_vid_to_update, target_relationship_vertex[0])
            add_edge(value_name, '', workflow_precondition_vid_to_update, new_target_relationship_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('WorkflowPreconditionDefinition', workflow_precondition_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'condition':
        abort(501)
    else:
        abort(400)


def add_workflow_precondition_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 1:
        schema_definition = WorkflowPreconditionDefinition()
        generate_uuid(schema_definition, cluster_name)
        add_in_vertex(schema_definition.vertex_type_system, 'vertex_type_system',
                      '"' + schema_definition.vertex_type_system + '"', schema_definition.vid)
        add_edge(edge_name, '', parent_vid, schema_definition.vid, '')
        return True
    return False
