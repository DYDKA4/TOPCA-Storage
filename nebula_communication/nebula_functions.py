import logging

import config
from nebula_communication import connection_pool, r
from nebula_communication.redis_communication import del_by_vid, get_all_vid_from_cluster


def start_session():
    session = connection_pool.get_session('Administator', 'password')
    result = session.execute(f'USE {config.WorkSpace}')
    assert result.is_succeeded(), result.error_msg()
    return session


def number_of_entities(session, vertex_name):
    # return of new index of new entities
    result = session.execute(f'LOOKUP ON {vertex_name}')
    # print(f'LOOKUP ON {vertex_name}')
    assert result.is_succeeded(), result.error_msg()
    result = result.column_values('VertexID')
    if result:
        amount = 0
        for index in result:
            index = index.as_string()
            if int(index[len(vertex_name):]) > amount:
                amount = int(index[len(vertex_name):])
        return amount + 1
    else:
        return 1


def vid_getter(vertex_type):
    vertex_type = vertex_type
    session = start_session()
    vid = '"' + vertex_type + str(number_of_entities(session, vertex_type)) + '"'
    session.release()
    return vid


def add_in_vertex(vertex_name, name_of_key_value, key_value, vid):
    session = start_session()
    result = session.execute(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {vid}'
                             f':({key_value});')
    logging.info(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {vid}'
                 f':({key_value});')
    # print(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {vid}'
    #       f':({key_value});')
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return


def add_edge(edge_name, edge_params, source_vertex, destination_vertex, data):
    session = start_session()
    result = session.execute(f'INSERT EDGE {edge_name}({edge_params})'
                             f' VALUE {source_vertex}->{destination_vertex}:({data})')
    logging.info(f'INSERT EDGE {edge_name}({edge_params})'
                 f' VALUE {source_vertex}->{destination_vertex}:({data})')
    # print(f'INSERT EDGE {edge_name}({edge_params})'
    #       f' VALUE {source_vertex}->{destination_vertex}:({interface})')
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return


def fetch_vertex(vid, vertex_name):
    session = start_session()
    result = session.execute(f'FETCH PROP ON {vertex_name} {vid} YIELD properties(vertex)')
    logging.info(f'FETCH PROP ON {vertex_name} {vid} YIELD properties(vertex)')
    assert result.is_succeeded(), result.error_msg()
    if result.column_values('properties(VERTEX)'):
        return result.column_values('properties(VERTEX)')[0]
    return None


def fetch_edge(source_vid, destination_vid, edge_name):
    session = start_session()
    result = session.execute(f'FETCH PROP ON {edge_name} {source_vid} -> {destination_vid} '
                             f'YIELD properties(edge)')
    logging.info(f'FETCH PROP ON {edge_name} {source_vid} -> {destination_vid} '
                 f'YIELD properties(edge)')
    assert result.is_succeeded(), result.error_msg()
    if result.column_values('properties(EDGE)'):
        return result.column_values('properties(EDGE)')[0]
    return None


def find_destination(vid, edge_name):
    session = start_session()
    result = session.execute(f'GO FROM {vid} over {edge_name} YIELD dst(edge) as vid')
    logging.info(f'GO FROM {vid} over {edge_name} YIELD dst(edge) as vid')
    assert result.is_succeeded(), result.error_msg()
    return result.column_values('vid')


def get_all_tags():
    session = start_session()
    result = session.execute('SHOW TAGS')
    assert result.is_succeeded(), result.error_msg()
    return result.column_values('Name')


def delete_vertex(vertex):
    session = start_session()
    result = session.execute(f'DELETE VERTEX {vertex}')
    logging.info(f'DELETE VERTEX {vertex} ')
    assert result.is_succeeded(), result.error_msg()
    del_by_vid(vertex)
    session.release()
    return


def delete_edge(edge_type, source_vertex, destination_vertex):
    session = start_session()
    result = session.execute(f'DELETE EDGE {edge_type} {source_vertex} -> {destination_vertex}')
    logging.info(f'DELETE EDGE {edge_type} {source_vertex} -> {destination_vertex}')
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return


def update_vertex(vertex_name, vid, value_name, value):
    session = start_session()
    result = session.execute(f"{'UPDATE'} VERTEX ON {vertex_name} {vid} SET {value_name} = {value}")
    logging.info(f"{'UPDATE'} VERTEX ON {vertex_name} {vid} SET {value_name} = {value}")
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return


def get_all_vid_from_cluster_by_type(cluster_name, vertex_type_system):
    clusters_vid = get_all_vid_from_cluster(cluster_name)
    session = start_session()
    result = session.execute(f'LOOKUP ON {vertex_type_system}')
    logging.info(f'LOOKUP ON {vertex_type_system}')
    assert result.is_succeeded(), result.error_msg()
    session.release()
    result = result.column_values("VertexID")
    vertex_type_system_vid = []
    for vid in result:
        vertex_type_system_vid.append(vid.as_string())
    result = list(set(clusters_vid) & set(vertex_type_system_vid))
    session.release()
    return result


def get_all_vertex(tag):
    session = start_session()
    result = session.execute(f'LOOKUP ON {tag}')
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return result.column_values('VertexID')


def go_from_over(vertex_id, edge_name):
    session = start_session()
    result = session.execute(f"GO FROM {vertex_id} OVER {edge_name} YIELD dst(edge) as id")
    logging.info(f"DST GO FROM {vertex_id} OVER {edge_name} YIELD dst(edge) as id")
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return result.column_values('id')


def go_from_over_dst_params(vertex_id, edge_name, **params):
    condition = ''
    for name, value in params.items():
        if not condition:
            condition = f"WHERE properties($$).{name} == '{value}'"
        else:
            condition += f"and properties($$).{name} == '{value}'"
    session = start_session()
    result = session.execute(f"GO FROM {vertex_id} OVER {edge_name} {condition} "
                             f"YIELD id($$) as id, properties($$) as props")
    logging.info(f"GO FROM {vertex_id} OVER {edge_name} {condition} "
                 f"YIELD id($$) as id, properties($$) as props")
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return result


def complex_go_from_over_2dst_vertex_param(vertex_id, edge_name_1, edge_name_2, param):
    session = start_session()
    result = session.execute(f"GO FROM {vertex_id} OVER {edge_name_1} YIELD dst(edge) "
                             f"AS id | GO FROM $-.id OVER {edge_name_2} WHERE properties($$).name == '{param}'"
                             f" YIELD id($^) as id, id($$) as id2")
    logging.info(f"GO FROM {vertex_id} OVER {edge_name_1} YIELD dst(edge) "
                 f"AS id | GO FROM $-.id OVER {edge_name_2} WHERE properties($$).name == '{param}'"
                 f" YIELD id($^) as id, id($$) as id2")
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return result


def complex_go_from_over_1dst_vertex_param(vertex_id, edge_name_1, edge_name_2, edge_param):
    session = start_session()
    result = session.execute(f"GO FROM {vertex_id} OVER {edge_name_1} WHERE properties($$).name == '{edge_param}'"
                             f"YIELD id($$) AS id  | GO FROM $-.id OVER {edge_name_2}"
                             f" YIELD id($^) as id, id($$) as id2 , properties($$) as props")
    logging.info(f"GO FROM {vertex_id} OVER {edge_name_1} WHERE properties($$).name == '{edge_param}'"
                 f"YIELD id($$) AS id  | GO FROM $-.id OVER {edge_name_2}"
                 f" YIELD id($^) as id, id($$) as id2, properties($$) as props")
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return result


def delete_all():
    on_delete = ''
    count = 0
    for it in r.scan_iter('*'):
        if on_delete == '':
            on_delete = '"' + it.decode("utf-8") + '"'
            count += 1
        else:
            on_delete += ', "' + it.decode("utf-8") + '"'
            count += 1
    delete_vertex(on_delete)
    logging.info(f'Success of deleting {count}')
    for it in r.scan_iter('*'):
        r.delete(it)
