import redis
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config

import config

Config = Config()
Config.max_connection_pool_size = 10
connection_pool = ConnectionPool()
ok = connection_pool.init([('10.100.149.228', 9669)], Config)
session = connection_pool.get_session('root', 'password')
result = session.execute(f'USE {config.WorkSpace}')
assert result.is_succeeded(), result.error_msg()
r = redis.Redis(host='10.100.149.228', port=6380, db=0)
