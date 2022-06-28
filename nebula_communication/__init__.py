from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config


Config = Config()
Config.max_connection_pool_size = 10
connection_pool = ConnectionPool()
ok = connection_pool.init([('10.100.151.128', 9669)], Config)