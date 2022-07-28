from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, add_edge, \
    get_all_vid_from_cluster_by_type, delete_vertex, add_in_vertex
from nebula_communication.update_template.Assignment.PropertyAssignmentUpdater import update_property_assignment, \
    add_property_assignment, get_property_assignment
from nebula_communication.update_template.Definition.InterfaceDefinitionUpdater import return_all
from nebula_communication.update_template.Definition.OperationImplementationDefinitionUpdater import \
    update_operation_implementation_definition, add_operation_implementation_definition
from nebula_communication.update_template.Definition.PropertyDefinitionUpdater import update_property_definition, \
    add_property_definition, get_property_definition
from parser.parser.tosca_v_1_3.definitions.OperationDefinition import OperationDefinition


def start_operation_definition(father_node_vid, varargs):
    if len(varargs) < 2:
        abort(400)
    destination = find_destination(father_node_vid, varargs[0])
    if destination is None:
        abort(400)
    operation_vid_to_update = None
    for operation_type_vid in destination:
        operation_type_value = fetch_vertex(operation_type_vid, 'OperationDefinition')
        operation_type_value = operation_type_value.as_map()
        if operation_type_value.get('name').as_string() == varargs[1]:
            operation_vid_to_update = operation_type_vid
            break
    if operation_vid_to_update is None:
        abort(400)
    return operation_vid_to_update


def update_operation_definition(service_template_vid, father_node_vid, value, value_name, varargs: list,
                                type_update, cluster_name):
    operation_vid_to_update = start_operation_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        if type_update == 'delete':
            delete_vertex('"' + operation_vid_to_update.as_string() + '"')
            return
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
    elif len(varargs) > 2:
        if varargs[2] == 'implementation':
            implementation = find_destination(operation_vid_to_update, varargs[2])
            if implementation and fetch_vertex(implementation[0], 'ArtifactDefinition'):
                abort(400)
            elif implementation and fetch_vertex(implementation[0], 'OperationImplementationDefinition'):
                if not add_operation_implementation_definition(type_update, varargs, cluster_name,
                                                               operation_vid_to_update, varargs[2]):
                    update_operation_implementation_definition(service_template_vid, operation_vid_to_update, value,
                                                               value_name, varargs[2:], type_update, cluster_name)
            else:
                abort(400)
        elif varargs[2] == 'inputs':
            inputs_vertex = find_destination(operation_vid_to_update, varargs[2])
            if inputs_vertex and fetch_vertex(inputs_vertex[0], 'PropertyDefinition'):
                if not add_property_definition(type_update, varargs[2:], cluster_name, operation_vid_to_update,
                                               varargs[2]):
                    update_property_definition(service_template_vid, operation_vid_to_update, value, value_name,
                                               varargs[2:], type_update, cluster_name)
            elif inputs_vertex and fetch_vertex(inputs_vertex[0], 'PropertyAssignment'):
                if not add_property_assignment(type_update, varargs, value, value_name, cluster_name,
                                               operation_vid_to_update):
                    update_property_assignment(service_template_vid, operation_vid_to_update, value,
                                               value_name, varargs[2:], type_update)
        else:
            abort(400)
    else:
        abort(400)


def add_operation_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 2:
        import_definition = OperationDefinition('"' + varargs[1] + '"')
        generate_uuid(import_definition, cluster_name)
        add_in_vertex(import_definition.vertex_type_system, 'name, vertex_type_system',
                      import_definition.name + ',"' + import_definition.vertex_type_system + '"', import_definition.vid)
        add_edge(edge_name, '', parent_vid, import_definition.vid, '')
        return True
    return False


def get_operation_definition(father_node_vid, value, value_name, varargs: list):
    operation_vid_to_update = start_operation_definition(father_node_vid, varargs)
    if len(varargs) == 2:
        vertex_value = fetch_vertex(operation_vid_to_update, 'OperationDefinition')
        vertex_value = vertex_value.as_map()
        if value_name == 'implementation':
            implementation = find_destination(operation_vid_to_update, value_name)
            if implementation and fetch_vertex(implementation[0], 'OperationImplementationDefinition'):
                abort(400)
            elif implementation and fetch_vertex(implementation[0], 'ArtifactDefinition'):
                return implementation[0].as_string()
        elif value_name in vertex_value.keys():
            if value == vertex_value.get(value_name).as_string():
                return operation_vid_to_update.as_string()
        else:
            abort(501)
    elif varargs[2] == 'inputs':
        destination = find_destination(operation_vid_to_update, value_name)
        if destination is None:
            return None
        if fetch_vertex(destination[0], 'PropertyAssignment'):
            result, flag = return_all(value, value_name, destination)
            if flag:
                return result
            return get_property_assignment(father_node_vid, value, value_name, varargs[2:])
        if fetch_vertex(destination[0], 'PropertyDefinition'):
            result, flag = return_all(value, value_name, destination)
            if flag:
                return result
            return get_property_definition(father_node_vid, value, value_name, varargs[2:])
    elif varargs[2] == 'implementation':
        implementation = find_destination(operation_vid_to_update, varargs[2])
        if implementation and fetch_vertex(implementation[0], 'ArtifactDefinition'):
            abort(400)
        elif implementation and fetch_vertex(implementation[0], 'OperationImplementationDefinition'):
            if len(implementation) > 1:
                abort(500)
            return implementation
    else:
        abort(400)
