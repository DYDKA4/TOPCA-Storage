from werkzeug.exceptions import abort

from nebula_communication.nebula_functions import fetch_vertex, find_destination, fetch_edge
from nebula_communication.template_builder.definition.ArtifactDefinition import construct_artifact_definition
from parser.parser.tosca_v_1_3.definitions.OperationImplementationDefinition import OperationImplementationDefinition


def construct_operation_implementation_definition(list_of_vid, only) -> dict:
    result = {}

    operation_implementation = OperationImplementationDefinition().__dict__

    for vid in list_of_vid:
        print(vid)
        vertex_value = fetch_vertex(vid, 'OperationImplementationDefinition')
        vertex_value = vertex_value.as_map()
        vertex_keys = vertex_value.keys()
        edges = set(operation_implementation.keys()) - set(vertex_keys) - {'vid'} - {'implementation'}
        for edge in edges:
            destination = find_destination(vid, edge)
            if edge == 'primary':
                if destination:
                    value = fetch_edge(vid, destination[0], 'primary')
                    if value is None:
                        primary = fetch_vertex(destination[0], 'ArtifactDefinition')
                        primary = primary.as_map()
                        primary = primary['name'].as_string()
                        result['primary'] = primary
                    else:
                        result['primary'] = construct_artifact_definition(destination, only)
            elif edge == 'dependencies':
                dependencies = []
                for dependency in destination:
                    value = fetch_edge(vid, dependency, 'dependencies')
                    if value is None:
                        dependency = fetch_vertex(dependency, 'ArtifactDefinition')
                        dependency = dependency.as_map()
                        dependency = dependency['name'].as_string()
                        dependencies.append(dependency)
                    else:
                        dependencies.append(construct_artifact_definition([dependency], only))
                result['dependencies'] = dependencies
            else:
                print(edge, vid)
                abort(500)

    return result
