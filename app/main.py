# from nebula2.gclient.net import ConnectionPool
# from nebula2.Config import Config
# import communication_with_nebula
# import Config
# # define a Config
# Config = Config()
# Config.max_connection_pool_size = 10
# # init connection pool
# connection_pool = ConnectionPool()
# # if the given servers are ok, return true, else return false
# ok = connection_pool.init([(Config.IP_address, 9669)], Config)
#
# # option 2 with session_context, session will be released automatically
# communication_with_nebula.hello_world()
# with connection_pool.session_context(Config.UserName, Config.UserPassword) as session:
#     result = session.execute('SHOW SPACES')
#     print(result)
#     print(result.keys())
#     print(result.column_values('Name'))
#
# # close the pool
# connection_pool.close()
