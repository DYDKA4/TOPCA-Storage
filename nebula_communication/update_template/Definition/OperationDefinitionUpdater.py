from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    get_all_vid_from_cluster_by_type
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment
from nebula_communication.update_template.Definition.OperationImplementationDefinitionUpdater import \
    update_operation_implementation_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition


def update_operation_definition(service_template_vid, father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 1:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None or len(destination) > 1:
        abort(400)
    operation_vid_to_update = destination[0]
    if len(varargs) == 1:
        if value_name == 'implementation':
            implementation = find_destination(operation_vid_to_update, value_name)
            if implementation and fetch_vertex(implementation[0], 'OperationImplementationDefinition'):
                abort(400)
            elif implementation and fetch_vertex(implementation[0], 'ArtifactDefinition'):
                current_primary_vertex = find_destination(operation_vid_to_update, value_name)
                artifact_definitions = get_all_vid_from_cluster_by_type(service_template_vid, 'ArtifactDefinition')
                if artifact_definitions is None:
                    abort(500)
                add_vertex = None
                for artifact_definition in artifact_definitions:
                    artifact_definition_value = fetch_vertex(artifact_definition, 'ArtifactDefinition')
                    artifact_definition_value = artifact_definition_value.as_map()
                    if '"' + artifact_definition_value.get('name').as_string() + '"' == value:
                        add_vertex = artifact_definition
                        break
                if add_vertex is None:
                    abort(400)
                delete_edge(value_name, operation_vid_to_update, current_primary_vertex[0])
                add_edge(value_name, '', operation_vid_to_update, add_vertex, '')
        else:
            vertex_value = fetch_vertex(operation_vid_to_update, 'OperationDefinition')
            vertex_value = vertex_value.as_map()
            if value_name not in vertex_value.keys():
                abort(400)
            update_vertex('OperationDefinition', operation_vid_to_update, value_name, value)
    elif len(varargs) > 1:
        if varargs[1] == 'implementation':
            implementation = find_destination(operation_vid_to_update, varargs[2])
            if implementation and fetch_vertex(implementation[0], 'ArtifactDefinition'):
                abort(400)
            elif implementation and fetch_vertex(implementation[0], 'OperationImplementationDefinition'):
                update_operation_implementation_definition(service_template_vid, operation_vid_to_update, value,
                                                           value_name, varargs[2:])
            else:
                abort(400)
        elif varargs[1] == 'inputs':
            inputs_vertex = find_destination(operation_vid_to_update, varargs[2])
            if inputs_vertex and fetch_vertex(inputs_vertex[0], 'PropertyDefinition'):
                update_property_definition(service_template_vid, operation_vid_to_update, value, value_name,
                                           varargs[2:])
            elif inputs_vertex and fetch_vertex(inputs_vertex[0], 'PropertyAssignment'):
                update_property_assignment(service_template_vid, operation_vid_to_update, value, value_name,
                                           varargs[2:])

        else:
            abort(400)
    else:
        abort(400)
