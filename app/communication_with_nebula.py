# a set of functions for processing requests
# from nebula2.gclient.net import ConnectionPool
# from nebula2.Config import Config

def hello_world():
    print('hello world')


def add_server(cpu, ram, mem, owner, date):
    with connection_pool.session_context(config.UserName, config.UserPassword) as session:
        session.execute('INSERT VERTEX IF NOT EXISTS person(name) VALUES "'+owner+'": ("'+owner+'")')
        session.execute('INSERT VERTEX IF NOT EXISTS server(CPU, RAM, memory) VALUES "asd": ('+cpu+','+ram+','+mem+')')

