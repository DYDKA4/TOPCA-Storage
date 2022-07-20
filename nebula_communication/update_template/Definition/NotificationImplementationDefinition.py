import warnings

from werkzeug.exceptions import abort

from nebula_communication.generate_uuid import generate_uuid
from nebula_communication.nebula_functions import find_destination, fetch_vertex, update_vertex, delete_edge, \
    add_edge, fetch_edge, delete_vertex, get_all_vid_from_cluster_by_type, add_in_vertex
from nebula_communication.update_template.Definition.ArtifactDefinition import update_artifact_definition
from parser.parser.tosca_v_1_3.definitions.NotificationImplementationDefinition import \
    NotificationImplementationDefinition


def update_notification_implementation_definition(service_template_vid, father_node_vid, value, value_name,
                                                  varargs: list, type_update, cluster_name):
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
    notification_implementation_vid_to_update = destination[0]
    if type_update == 'delete':
        delete_vertex('"' + notification_implementation_vid_to_update.as_string() + '"')
        return
    if len(varargs) == 1:
        if value_name == 'dependencies':
            dependencies_vertexes = find_destination(notification_implementation_vid_to_update, value_name)
            to_delete_vertex = None
            for valid_source_type_vid in dependencies_vertexes:
                valid_source_value = fetch_vertex(valid_source_type_vid, 'ArtifactDefinition')
                valid_source_value = valid_source_value.as_map()
                if '"' + valid_source_value.get('name').as_string() + '"' == value:
                    to_delete_vertex = valid_source_type_vid
                    break
            if to_delete_vertex:
                delete_edge(value_name, notification_implementation_vid_to_update, to_delete_vertex)

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
                add_edge(value_name, '', notification_implementation_vid_to_update, add_vertex, '')
        elif value_name == 'primary':
            primary_vertex = find_destination(notification_implementation_vid_to_update, value_name)
            new_primary_vid = None
            dependencies_vertexes = find_destination(notification_implementation_vid_to_update, value_name)
            for primary_vid in dependencies_vertexes:
                data_type_value = fetch_vertex(primary_vid, 'ArtifactDefinition')
                data_type_value = data_type_value.as_map()
                if '"' + data_type_value.get('name').as_string() + '"' == value:
                    new_primary_vid = primary_vid
                    break
            if new_primary_vid is None:
                abort(400)
            if primary_vertex is not None:
                if len(primary_vertex) > 1:
                    abort(500)
                delete_edge(value_name, notification_implementation_vid_to_update, primary_vertex[0])
            add_edge(value_name, '', notification_implementation_vid_to_update, new_primary_vid, '')
        else:
            vertex_value = fetch_vertex(notification_implementation_vid_to_update,
                                        'NotificationImplementationDefinition')
            vertex_value = vertex_value.as_map()
            if value_name not in vertex_value.keys():
                abort(400)
            update_vertex('NotificationImplementationDefinition', notification_implementation_vid_to_update,
                          value_name, value)
    else:
        abort(400)


def add_notification_implementation_definition(type_update, varargs, cluster_name, parent_vid, edge_name):
    if type_update == 'add' and len(varargs) == 1:
        import_definition = NotificationImplementationDefinition()
        generate_uuid(import_definition, cluster_name)
        add_in_vertex(import_definition.vertex_type_system, 'vertex_type_system',
                      '"' + import_definition.vertex_type_system + '"', import_definition.vid)
        add_edge(edge_name, '', parent_vid, import_definition.vid, '')
        return True
    return False
