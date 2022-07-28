from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    get_all_vid_from_cluster_by_type, delete_vertex, add_in_vertex
from nebula_communication.update_template.Assignment.RequirementAssignment import form_result
from parser.parser.tosca_v_1_3.definitions.WorkflowStepDefinition import WorkflowStepDefinition


def start_workflow_step_definition(father_node_vid, varargs):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    workflow_step_vid_to_update = None
    for workflow_step_vid in destination:
        workflow_step_value = fetch_vertex(workflow_step_vid, 'WorkflowStepDefinition')
        workflow_step_value = workflow_step_value.as_map()
        if workflow_step_value.get('name').as_string() == varargs[1]:
            workflow_step_vid_to_update = workflow_step_vid
            break
    if workflow_step_vid_to_update is None:
        abort(400)
    return workflow_step_vid_to_update


def update_workflow_step_definition(service_template_vid, father_node_vid, value, value_name, varargs: list,
                                    type_update):
    workflow_step_vid_to_update = start_workflow_step_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + workflow_step_vid_to_update.as_string() + '"')
            return
        vertex_value = fetch_vertex(workflow_step_vid_to_update, 'WorkflowStepDefinition')
        vertex_value = vertex_value.as_map()
        topology_template = find_destination(service_template_vid, 'topology_template')
        if value_name == 'target_relationship':
            target_relationship_vertex = find_destination(workflow_step_vid_to_update, value_name)
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
                delete_edge(value_name, workflow_step_vid_to_update, target_relationship_vertex[0])
            add_edge(value_name, '', workflow_step_vid_to_update, new_target_relationship_vid, '')
        elif value_name == 'on_success' or value_name == 'on_failure':
            all_step = get_all_vid_from_cluster_by_type(service_template_vid, 'WorkflowStepDefinition')
            target_step_vertex = find_destination(workflow_step_vid_to_update, value_name)
            new_step_vid = None
            for step_vid in all_step:
                step_value = fetch_vertex(step_vid, 'WorkflowStepDefinition')
                step_value = step_value.as_map()
                if '"' + step_value.get('name').as_string() + '"' == value:
                    new_step_vid = step_vid
                    break
            if new_step_vid is None:
                abort(400)
            if target_step_vertex is not None:
                if len(target_step_vertex) > 1:
                    abort(500)
                delete_edge(value_name, workflow_step_vid_to_update, target_step_vertex[0])
            add_edge(value_name, '', workflow_step_vid_to_update, new_step_vid, '')
        elif value_name in vertex_value.keys():
            update_vertex('WorkflowStepDefinition', workflow_step_vid_to_update, value_name, value)
        else:
            abort(501)
    elif varargs[2] == 'filter':
        abort(501)
    elif varargs[2] == 'activities':
        abort(501)
    else:
        abort(400)


def add_workflow_step_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        data_type = WorkflowStepDefinition('"' + varargs[1] + '"')
        generate_uuid(data_type, cluster_name)
        add_in_vertex(data_type.vertex_type_system, 'name, vertex_type_system',
                      data_type.name + ',"' + data_type.vertex_type_system + '"', data_type.vid)
        add_edge(edge_name, '', parent_vid, data_type.vid, '')
        return True
    return False


def get_workflow_step_definition(father_node_vid, value, value_name, varargs: list):
    workflow_step_vid_to_update = start_workflow_step_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(workflow_step_vid_to_update, 'WorkflowStepDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'on_success' or value_name == 'on_failure':
            destination = find_destination(workflow_step_vid_to_update, value_name)
            if value is None:
                result = []
                for vid in destination:
                    result.append(vid.as_string())
                return result
            for vid in destination:
                destination_value = fetch_vertex(vid, 'WorkflowStepDefinition')
                destination_value = destination_value.as_map()
                if value == destination_value.get('name'):
                    return vid.as_string()
            return None
        elif value_name == 'target_relationship':
            return form_result(workflow_step_vid_to_update, value_name)
        elif value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return workflow_step_vid_to_update.as_string()
        else:
            abort(501)
    elif varargs[2] == 'filter':
        abort(501)
    elif varargs[2] == 'activities':
        abort(501)
    else:
        abort(400)
