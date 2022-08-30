import redis
from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config

import config

Config = Config()
Config.max_connection_pool_size = 10
connection_pool = ConnectionPool()
ok = connection_pool.init([('10.100.151.128', 9669)], Config)
session = connection_pool.get_session('Administator', 'password')
result = session.execute(f'USE {config.WorkSpace}')
assert result.is_succeeded(), result.error_msg()
r = redis.Redis(host='10.100.151.128', port=6380, db=0)
