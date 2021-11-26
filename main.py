from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config
import functions
import config
# define a Config
Config = Config()
Config.max_connection_pool_size = 10
# init connection pool
connection_pool = ConnectionPool()
# if the given servers are ok, return true, else return false
ok = connection_pool.init([(config.IP_address, 9669)], Config)

# option 2 with session_context, session will be released automatically
functions.hello_world()
with connection_pool.session_context(config.UserName, config.UserPassword) as session:
    result = session.execute('SHOW SPACES')
    print(result)
    print(result.keys())
    print(result.column_values('Name'))

# close the pool
connection_pool.close()
