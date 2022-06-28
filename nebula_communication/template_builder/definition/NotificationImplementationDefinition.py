from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination
from parser.parser.tosca_v_1_3.definitions.NotificationImplementationDefinition import \
    NotificationImplementationDefinition


def construct_notification_implementation_definition(list_of_vid) -> dict:
    result = {}

    constraint_clause = NotificationImplementationDefinition().__dict__

    for vid in list_of_vid:
        vertex_value = fetch_vertex(vid, 'NotificationImplementationDefinition')
        vertex_value = vertex_value.as_map()
        vertex_keys = vertex_value.keys()
        edges = set(constraint_clause.keys()) - set(vertex_keys) - {'vid'} - {'implementation'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'primary':
                if destination:
                    primary = fetch_vertex(destination[0], 'ArtifactDefinition')
                    primary = primary.as_map()
                    primary = primary['name'].as_string()
                    result['primary'] = primary
            elif edge == 'dependencies':
                dependencies = []
                for dependency in destination:
                    dependency = dependency.as_map()
                    dependency = dependency['name'].as_string()
                    dependencies.append(dependency)
                result['dependencies'] = dependencies
            else:
                print(edge, vid)
                abort(500)

        # result.append({vertex_value['operator'].as_string(): value})
    return result
