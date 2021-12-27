# define a Config
from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config
import config
import time

Config = Config()
Config.max_connection_pool_size = 10
# init connection pool
connection_pool = ConnectionPool()
# if the given servers are ok, return true, else return false
ok = connection_pool.init([(config.IP_address, 9669)], Config)


def hello_world():
    print('hello world')


def chose_of_space():
    # chose of working space session is still open
    session = connection_pool.get_session(config.UserName, config.UserPassword)
    result = session.execute(f'USE {config.WorkSpace}')
    assert result.is_succeeded(), result.error_msg()
    return session


def number_of_entities(session, vertex_name):
    # return of new index of new entities
    result = session.execute(f'LOOKUP ON {vertex_name}')
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


def is_updated(session, vertex_name):
    result = session.execute(f'LOOKUP ON {vertex_name}')
    while not result.is_succeeded():
        print(result.is_succeeded(), result.error_msg())
        result = session.execute(f'LOOKUP ON {vertex_name}')
        session.release()
        session = chose_of_space()
    return session


def is_already_recorded(session, vertex_name, name_of_key_value, key_value):
    # return is this already recorded
    result = session.execute(f'LOOKUP ON {vertex_name} WHERE {vertex_name}.{name_of_key_value} == "{key_value}";')
    assert result.is_succeeded(), result.error_msg()
    result = result.column_values('VertexID')
    if result:
        result = result[0]
    return result


def create_vertex_if_nox_exist(session, type_of_node):
    result = session.execute(f'CREATE TAG IF NOT EXISTS {type_of_node} (name fixed_string(256) NOT NULL)')
    # print(f'CREATE TAG IF NOT EXISTS {type_of_node} (name fixed_string(256) NOT NULL)')
    assert result.is_succeeded(), result.error_msg()
    result = session.execute(f'CREATE TAG INDEX IF NOT EXISTS Index{type_of_node} on {type_of_node}(name)')
    assert result.is_succeeded(), result.error_msg()
    return


def add_in_vertex(session, vertex_name, name_of_key_value, key_value, amount):
    # add into vertex value
    result = session.execute(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {amount}'
                             f':({key_value});')
    print(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {amount}'
          f':({key_value});')
    assert result.is_succeeded(), result.error_msg()
    return


def create_edge_if_nox_exist(session, type_of_link):
    result = session.execute(f'CREATE EDGE IF NOT EXISTS {type_of_link} ()')
    # print(f'CREATE TAG IF NOT EXISTS {type_of_link} ()')
    assert result.is_succeeded(), result.error_msg()
    result = session.execute(f'CREATE EDGE INDEX IF NOT EXISTS Index{type_of_link} on {type_of_link}()')
    print(f'CREATE EDGE INDEX IF NOT EXISTS Index{type_of_link} on {type_of_link}()')
    assert result.is_succeeded(), result.error_msg()
    return


def add_edge(session, edge_name, edge_params, source_vertex, destination_vertex, data):
    result = session.execute(f'INSERT EDGE {edge_name}({edge_params})'
                             f' VALUE {source_vertex}->{destination_vertex}:({data})')
    print(f'INSERT EDGE {edge_name}({edge_params})'
                             f' VALUE {source_vertex}->{destination_vertex}:({data})')
    assert result.is_succeeded(), result.error_msg()
    return


def add_server(cpu, ram, mem, owner, date):
    session = chose_of_space()
    # search for an existing user
    is_recorded = is_already_recorded(session, config.NameOfUserVertex, config.NameOfKeyValueUser, owner)
    if not is_recorded:
        source_vertex = number_of_entities(session, config.NameOfUserVertex)
        owner = '"' + owner + '"'
        source_vertex = f'"{config.NameOfUserVertex}{source_vertex}"'
        add_in_vertex(session, config.NameOfUserVertex, config.NameOfKeyValueUser, owner, source_vertex)
    else:
        source_vertex = is_recorded
    destination_vertex = number_of_entities(session, config.NameOfServerVertex)
    destination_vertex = f'"{config.NameOfServerVertex}{destination_vertex}"'
    add_in_vertex(session, config.NameOfServerVertex, config.NameOfKeyValueServer, f'{cpu},{ram},{mem}',
                  destination_vertex)
    date = list(date)
    date[10] = 'T'
    date = "".join(date)
    date = f'datetime("{date}")'
    add_edge(session, config.NameOfOwnerEdge, config.NameOfKeyValueOwner, source_vertex, destination_vertex, date)

    session.release()


def find_server(cpu, ram, mem, owner):
    # return list of this servers with owner
    session = chose_of_space()
    owner = is_already_recorded(session, config.NameOfUserVertex, config.NameOfKeyValueUser, owner)
    if not owner:
        return 0
    assert owner, "such owner not existed"
    result = session.execute(f'GO FROM {owner} over owner'
                             f' WHERE properties($$).cpu == {cpu} AND properties($$).ram == {ram} AND'
                             f' properties($$).mem == {mem} '
                             'YIELD properties($^).name as name, properties($$).cpu as cpu,'
                             ' properties($$).ram as ram, properties($$).mem as mem,'
                             ' properties(edge).date_of_creation as date_of_creation')

    assert result.is_succeeded(), result.error_msg()
    answer = []
    for key in result.keys():

        tmp_answer = []
        if not result.column_values(key):
            return 0
        for value in result.column_values(key):
            if value.is_int():
                tmp_answer += [{
                    f'{key}': value.as_int()}]
            elif value.is_string():
                tmp_answer += [{
                    f'{key}': value.as_string()}]
            elif value.is_datetime():
                tmp_answer += [{
                    'year': value.as_datetime().get_year(),
                    'month': value.as_datetime().get_month(),
                    'day': value.as_datetime().get_day(),
                    'hour': value.as_datetime().get_hour(),
                    'minute': value.as_datetime().get_minute(),
                    'sec': value.as_datetime().get_sec(),
                    'microsecond': value.as_datetime().get_microsec()}]
        answer += [tmp_answer]

    session.release()
    return answer


def name_to_index(rename, data):
    for node in data:
        node[0] = rename[node[0]]
        if len(node) > 2:
            print(node)
            if type(node[2]) == list and node[2]:
                for link in node[2]:
                    print(node[2])
                    print(link, link in rename.keys())
                    if link in rename.keys():
                        link = rename[link]
            else:
                node[2][1] = rename[node[2][1]]
    return data


def yaml_deploy(data):
    """ программа за два прохода создает щаблон в бд,
    за первый проход она размещается все узлы в бд, за второй создаёт соотвествующие связи
    """
    session = chose_of_space()
    rename = {}

    for node in data:
        type_of_node = node[1]
        create_vertex_if_nox_exist(session, type_of_node)
    session.release()

    session = chose_of_space()
    for node in data:
        name = node[0]
        type_of_node = node[1]
        name = '"' + name + '"'
        session = is_updated(session, type_of_node)
        vid = number_of_entities(session, type_of_node)
        rename[node[0]] = type_of_node + str(vid)
        add_in_vertex(session, type_of_node, 'name', name, f'"{type_of_node}{vid}"')

    print(rename)
    data = name_to_index(rename, data)
    session.release()

    time.sleep(1)

    session = chose_of_space()
    for node in data:
        if len(node) > 2:
            if type(node[2]) == list:
                for link in node[2]:
                    link_type = link[0]
                    create_edge_if_nox_exist(session, link_type)
            else:
                link_type = node[2][0]
                create_edge_if_nox_exist(session, link_type)
    session.release()

    session = chose_of_space()
    for node in data:
        source = '"' + node[0] + '"'
        if len(node) > 2:
            if type(node[2]) == list:
                for link in node[2]:
                    destination = '"' + link[1] + '"'
                    link_type = link[0]
                    session = is_updated(session, link_type)
                    add_edge(session, link_type, '', source, destination, '')
            else:
                destination = '"' + node[2][1] + '"'
                link_type = node[2][0]
                session = is_updated(session, link_type)
                add_edge(session, link_type, '', source, destination, '')
    print(data)
    session.release()
