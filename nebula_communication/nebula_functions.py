import logging

import config
from nebula_communication import connection_pool


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


def is_unique_vid(vid):
    # return true if unique else false
    tags = get_all_tags()

    session = start_session()
    for tag_name in tags:
        tag_name = tag_name.as_string()
        result = session.execute(f'MATCH (v:{tag_name}) WHERE id(v) == "{vid}" RETURN v')
        # logging.info(f'MATCH (v:{tag_name}) WHERE id(v) == "{vid}" RETURN v')
        assert result.is_succeeded(), result.error_msg()
        if result.column_values('v'):
            return False
    return True


def delete_vertex(session, vertex):
    result = session.execute(f'DELETE VERTEX {vertex}')
    logging.info(f'DELETE VERTEX {vertex} ')
    assert result.is_succeeded(), result.error_msg()
    session.release()
    return
