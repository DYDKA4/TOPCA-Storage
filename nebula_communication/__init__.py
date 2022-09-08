import redis
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config

import config

Config = Config()
Config.max_connection_pool_size = 10
connection_pool = ConnectionPool()
ok = connection_pool.init([(config.IP_address, config.DataBasePort)], Config)
session = connection_pool.get_session(config.UserName, config.UserPassword)
result = session.execute(f'USE {config.WorkSpace}')
assert result.is_succeeded(), result.error_msg()
r = redis.Redis(host=config.IP_address, port=config.RedisPort, db=0)
