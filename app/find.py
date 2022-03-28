from app import communication_with_nebula


def search_by_type(value_name, session, search_by, cluster_name):
    answer = communication_with_nebula.find_destination_by_property(session, f'{cluster_name}', 'assignment',
                                                                    value_name, search_by,
                                                                    full_list=True)
    return answer


def find_node(varargs, search_by, cluster_name, find_cluster_name, requirement_name):
    session = communication_with_nebula.chose_of_space()
    varargs = varargs.split("/")
    if varargs[0] == 'all':
        list_of_clusters = communication_with_nebula.get_all_vertex(session, "ClusterName")
        if varargs[1] == 'node':
            answer = []
            if varargs[2] == 'properties':
                """
                curl -X GET 'http://127.0.0.1:5000/find/all/node/properties/snapshot_id?search_by=%7B%27get_input%27:%20%27storage_snapshot_id%27%7D'
                curl -X GET 'http://127.0.0.1:5000/find/all/node/properties/size?search_by=50%20GB'
                """
                for cluster in list_of_clusters:
                    vertexes = communication_with_nebula.find_destination(session, cluster, 'assignment',
                                                                          full_list=True)
                    for vertex in vertexes:
                        result = []
                        list_of_properties_1 = communication_with_nebula. \
                            find_destination_by_property(session, vertex, 'assignment_property', 'values', search_by,
                                                         full_list=True)
                        list_of_properties_2 = communication_with_nebula. \
                            find_destination_by_property(session, vertex, 'assignment_property', 'value_name',
                                                         varargs[3], full_list=True)
                        result += list(set(list_of_properties_1, ).intersection(set(list_of_properties_2)))
                        if result:
                            if find_cluster_name:
                                answer += [cluster]
                            else:
                                answer += [vertex]
                        print("ddd", list_of_properties_1, list_of_properties_2, answer, find_cluster_name)
                return f'{answer}'
            elif varargs[2] == 'type':
                """ curl -X GET 'http://127.0.0.1:5000/find/all/node/type?search_by=tosca.nodes.BlockStorage' """
                for cluster in list_of_clusters:
                    result = []
                    result += search_by_type(varargs[2], session, search_by, cluster)
                    if result:
                        if find_cluster_name:
                            answer += [cluster]
                        else:
                            answer += result
                return f'{answer}'
            elif varargs[2] == 'capabilities':
                for cluster in list_of_clusters:
                    vertexes = communication_with_nebula.find_destination(session, cluster, 'assignment',
                                                                          full_list=True)
                    for vertex in vertexes:
                        list_of_capabilities = communication_with_nebula. \
                            find_destination_by_property(session, vertex, 'assignment_capability', 'name', varargs[3],
                                                         full_list=True)
                        if varargs[4] == 'properties':
                            for capabilities in list_of_capabilities:
                                result = []
                                list_of_properties_1 = communication_with_nebula. \
                                    find_destination_by_property(session, capabilities, 'assignment_property',
                                                                 'values', search_by, full_list=True)
                                list_of_properties_2 = communication_with_nebula. \
                                    find_destination_by_property(session, capabilities, 'assignment_property',
                                                                 'value_name', varargs[5], full_list=True)
                                result += list(set(list_of_properties_1, ).intersection(set(list_of_properties_2)))
                                if result:
                                    if find_cluster_name:
                                        answer += [cluster]
                                    else:
                                        answer += [vertex]
                        else:
                            return "501 Not Implemented"
                return f'{answer}'
            else:
                return "501"
        else:
            return "501 Not Implemented"
    elif varargs[0] == 'node':
        answer = []
        if varargs[1] == 'properties':
            """
            curl -X GET 'http://127.0.0.1:5000/find/node/properties/snapshot_id?search_by=%7B%27get_input%27:%20%27storage_snapshot_id%27%7D&cluster_name=cluster_tosca_4'
            curl -X GET 'http://127.0.0.1:5000/find/node/properties/size?search_by=50%20GB&cluster_name=cluster_tosca_4'
            """
            vertexes = communication_with_nebula.find_destination(session, f'"{cluster_name}"', 'assignment',
                                                                  full_list=True)
            for vertex in vertexes:
                result = []
                list_of_properties_1 = communication_with_nebula. \
                    find_destination_by_property(session, vertex, 'assignment_property', 'values', search_by,
                                                 full_list=True)
                list_of_properties_2 = communication_with_nebula. \
                    find_destination_by_property(session, vertex, 'assignment_property', 'value_name',
                                                 varargs[2], full_list=True)
                result += list(set(list_of_properties_1, ).intersection(set(list_of_properties_2)))
                if result:
                    answer += [vertex]
                print(list_of_properties_1, list_of_properties_2, answer)
            return f'{answer}'
        elif varargs[1] == 'type':
            """ curl -X GET 'http://127.0.0.1:5000/find/node/type?search_by=tosca.nodes.BlockStorage&cluster_name=cluster_tosca_4' """
            answer += search_by_type(varargs[1], session, search_by, f'"{cluster_name}"')
            return f'{answer}'
        elif varargs[1] == 'capabilities':
            vertexes = communication_with_nebula.find_destination(session, f'"{cluster_name}"', 'assignment',
                                                                  full_list=True)
            for vertex in vertexes:
                list_of_capabilities = communication_with_nebula. \
                    find_destination_by_property(session, vertex, 'assignment_capability', 'name', varargs[2],
                                                 full_list=True)
                if varargs[3] == 'properties':
                    for capabilities in list_of_capabilities:
                        result = []
                        list_of_properties_1 = communication_with_nebula. \
                            find_destination_by_property(session, capabilities, 'assignment_property',
                                                         'values', search_by, full_list=True)
                        list_of_properties_2 = communication_with_nebula. \
                            find_destination_by_property(session, capabilities, 'assignment_property',
                                                         'value_name', varargs[4], full_list=True)
                        print(list_of_properties_1, list_of_properties_2)
                        result += list(set(list_of_properties_1, ).intersection(set(list_of_properties_2)))
                        if result:
                            answer += [vertex]
                else:
                    return "501 Not Implemented"
            return f'{answer}'
        else:
            return '501 Not Implemented'
    elif varargs[0] == 'destination_node':
        """ curl -X GET 'http://127.0.0.1:5000/find/destination_node?cluster_name=cluster_tosca_4&requirement_name=local_storage'
        """
        if cluster_name is None:
            return "400 Bad Request cluster name is None"
        if requirement_name is None:
            return "400 Bad Request node_vid is None"
        list_of_definition = communication_with_nebula.find_destination(session, f'"{cluster_name}"', 'definition',
                                                                        full_list=True)
        acceptable_definition = []
        type_acceptable = []
        for definition in list_of_definition:
            requirement_vid = communication_with_nebula.find_destination_by_property(session, definition,
                                                                                     'requirements', 'name',
                                                                                     requirement_name, full_list=True)
            if requirement_vid:
                for vid in requirement_vid:
                    dest_vertex = communication_with_nebula.find_destination(session, vid,
                                                                             'requirements_destination')
                    if dest_vertex:
                        type_acceptable.append(communication_with_nebula.fetch_vertex(session, f'"{dest_vertex}"',
                                                                                      'DefinitionVertex',
                                                                                      'vertex_type_tosca'))
        assignment_vertex = communication_with_nebula.find_destination(session, f'"{cluster_name}"', 'assignment',
                                                                       full_list=True)
        result = {}
        for node_type in type_acceptable:
            result_vertex = []
            for vertex in assignment_vertex:
                if 'AssignmentVertex' in vertex.as_string():
                    assignment_type = communication_with_nebula.fetch_vertex(session, vertex, 'AssignmentVertex',
                                                                             'type')
                    if assignment_type == node_type:
                        result_vertex.append(vertex)
            if result_vertex:
                result[node_type] = result_vertex
        return f'100 OK {result}'
    else:
        return "501 Not Implemented"
