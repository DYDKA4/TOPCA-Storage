# define a Config
from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config
import config

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
    amount = result.column_values('VertexID')
    if not amount:
        return 1
    return amount[-1].as_int() + 1


def is_already_recorded(session, vertex_name, name_of_key_value, key_value):
    # return is this already recorded
    result = session.execute(f'LOOKUP ON {vertex_name} WHERE {vertex_name}.{name_of_key_value} == "{key_value}";')
    assert result.is_succeeded(), result.error_msg()
    result = result.column_values('VertexID')

    return bool(result)


def add_in_vertex(session, vertex_name, name_of_key_value, key_value, amount):
    # add into vertex value
    result = session.execute(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {amount}'
                             f':("{key_value}");')
    print(f'INSERT VERTEX {vertex_name} ({name_of_key_value}) VALUES {amount}'
                             f':({key_value});')
    assert result.is_succeeded(), result.error_msg()
    return 0


def add_server(cpu, ram, mem, owner, date):
    session = chose_of_space()
    # search for an existing user
    is_recorded = is_already_recorded(session, config.NameOfUserVertex, config.NameOfKeyValueUser, owner)
    if not is_recorded:
        amount = number_of_entities(session, config.NameOfUserVertex)
        owner = '"' + owner + '"'
        add_in_vertex(session, config.NameOfUserVertex, config.NameOfKeyValueUser, owner, amount)

    amount = number_of_entities(session, config.NameOfServerVertex)
    add_in_vertex(session, config.NameOfServerVertex, config.NameOfKeyValueServer, f'"NoName",{cpu},{ram},{mem}', amount)
    # session.release()
