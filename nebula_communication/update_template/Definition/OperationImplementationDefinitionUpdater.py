import warnings

from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, \
    add_edge, fetch_edge, delete_vertex, get_all_vid_from_cluster_by_type, add_in_vertex
from nebula_communication.update_template.Definition.ArtifactDefinition import update_artifact_definition
from nebula_communication.update_template.find_functions import form_result
from parser.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition


def update_operation_implementation_definition(service_template_vid, father_node_vid, value, value_name, varargs: list,
                                               type_update, cluster_name):
    if len(varargs) < 1:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    elif len(destination) > 1:
        if type_update == 'delete':
            for destination_vid in destination:
                delete_vertex('"' + destination_vid.as_string() + '"')
            return
        else:
            abort(400)
    operation_implementation_vid_to_update = destination[0]
    if type_update == 'delete':
        delete_vertex('"' + operation_implementation_vid_to_update.as_string() + '"')
        return

    if len(varargs) == 1:
        if value_name == 'dependencies':
            dependencies_vertexes = find_destination(operation_implementation_vid_to_update, value_name)
            to_delete_vertex = None
            for valid_source_type_vid in dependencies_vertexes:
                valid_source_value = fetch_vertex(valid_source_type_vid, 'ArtifactDefinition')
                valid_source_value = valid_source_value.as_map()
                if '"' + valid_source_value.get('name').as_string() + '"' == value:
                    to_delete_vertex = valid_source_type_vid
                    break
            if to_delete_vertex:
                value = fetch_edge(operation_implementation_vid_to_update, to_delete_vertex, 'dependencies')
                if value is not None:
                    warnings.warn(f'DELETE dependencies in OperationImplementation, with definition in edge, could '
                                  f'cause critical error')
                    delete_vertex(to_delete_vertex)
                delete_edge(value_name, operation_implementation_vid_to_update, to_delete_vertex)

            else:
                add_vertex = None
                artifact_definitions = get_all_vid_from_cluster_by_type(service_template_vid, 'ArtifactDefinition')
                if artifact_definitions is None:
                    abort(500)
                for artifact_definition in artifact_definitions:
                    artifact_definition_value = fetch_vertex(artifact_definition, 'ArtifactDefinition')
                    artifact_definition_value = artifact_definition_value.as_map()
                    if '"' + artifact_definition_value.get('name').as_string() + '"' == value:
                        add_vertex = artifact_definition
                        break
                if add_vertex is None:
                    abort(400)
                add_edge(value_name, '', operation_implementation_vid_to_update, add_vertex, '')
        elif value_name == 'primary':
            current_primary_vertex = find_destination(operation_implementation_vid_to_update, value_name)
            if current_primary_vertex is None:
                abort(500)
            if fetch_edge(operation_implementation_vid_to_update, current_primary_vertex[0], 'primary'):
                abort(400)
            add_vertex = None
            artifact_definitions = get_all_vid_from_cluster_by_type(service_template_vid, 'ArtifactDefinition')
            if artifact_definitions is None:
                abort(500)
            for artifact_definition in artifact_definitions:
                artifact_definition_value = fetch_vertex(artifact_definition, 'ArtifactDefinition')
                artifact_definition_value = artifact_definition_value.as_map()
                if '"' + artifact_definition_value.get('name').as_string() + '"' == value:
                    add_vertex = artifact_definition
                    break
            if add_vertex is None:
                abort(400)
            delete_edge(value_name, operation_implementation_vid_to_update, current_primary_vertex[0])
            add_edge(value_name, '', operation_implementation_vid_to_update, add_vertex, '')
        else:
            vertex_value = fetch_vertex(operation_implementation_vid_to_update, 'OperationImplementationDefinition')
            vertex_value = vertex_value.as_map()
            if value_name not in vertex_value.keys():
                abort(400)
            update_vertex('OperationImplementationDefinition', operation_implementation_vid_to_update, value_name,
                          value)
    elif len(varargs) > 1:
        if varargs[1] == 'primary':
            primary_vertex = find_destination(operation_implementation_vid_to_update, value_name)
            if len(primary_vertex) > 2:
                abort(500)
            if fetch_edge(operation_implementation_vid_to_update, primary_vertex[0], 'dependencies') is None:
                abort(400)
            else:
                update_artifact_definition(service_template_vid, operation_implementation_vid_to_update, value,
                                           value_name, varargs[2:])
        elif varargs[1] == 'dependencies':
            dependencies_vertexes = find_destination(operation_implementation_vid_to_update, value_name)
            target = None
            for artifact_definition in dependencies_vertexes:
                artifact_definition_value = fetch_vertex(artifact_definition, 'ArtifactDefinition')
                artifact_definition_value = artifact_definition_value.as_map()
                if artifact_definition_value.get('name').as_string() == varargs[2]:
                    target = artifact_definition
                    break
            if target is None:
                abort(400)
            if fetch_edge(operation_implementation_vid_to_update, target, 'dependencies') is None:
                abort(400)
            else:
                update_artifact_definition(service_template_vid, operation_implementation_vid_to_update, value,
                                           value_name, varargs[2:])
        else:
            abort(400)
    else:
        abort(400)


def add_operation_implementation_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 1:
        import_definition = OperationImplementationDefinition()
        generate_uuid(import_definition, cluster_name)
        add_in_vertex(import_definition.vertex_type_system, 'vertex_type_system',
                      '"' + import_definition.vertex_type_system + '"', import_definition.vid)
        add_edge(edge_name, '', parent_vid, import_definition.vid, '')
        return True
    return False


def get_operation_implementation_definition(father_node_vid, value, value_name, varargs: list):
    if len(varargs) < 1:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    elif len(destination) > 1:
        abort(400)
    operation_implementation_vid_to_update = destination[0]
    if len(varargs) == 2:
        vertex_value = fetch_vertex(operation_implementation_vid_to_update, 'WorkflowStepDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'dependencies':
            destination = find_destination(operation_implementation_vid_to_update, value_name)
            if value is None:
                result = []
                for vid in destination:
                    result.append(vid.as_string())
                return result
            for vid in destination:
                destination_value = fetch_vertex(vid, 'ArtifactDefinition')
                destination_value = destination_value.as_map()
                if value == destination_value.get('name'):
                    return vid.as_string()
        elif value_name == 'primary':
            return form_result(operation_implementation_vid_to_update, value_name)
        elif value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return operation_implementation_vid_to_update.as_string()
        else:
            abort(501)
    else:
        abort(400)
