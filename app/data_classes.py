from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config
import config


class Vertex:
    Config = Config()
    Config.max_connection_pool_size = 10
    # init connection pool
    connection_pool = ConnectionPool()
    # if the given servers are ok, return true, else return false
    ok = connection_pool.init([(config.IP_address, 9669)], Config)

    def __init__(self, name=None, typeOfVertex=None, requirements=None):
        self.vid = None
        self.session = None
        self.typeOfVertex = typeOfVertex
        self.name = name
        self.requirements = requirements

    def chose_of_space(self):
        # chose of working space session is still open
        self.session = self.connection_pool.get_session(config.UserName, config.UserPassword)
        result = self.session.execute(f'USE {config.WorkSpace}')
        assert result.is_succeeded(), result.error_msg()

    def generate_vid(self):
        result = self.session.execute(f'LOOKUP ON {self.typeOfVertex}')
        assert result.is_succeeded(), result.error_msg()
        result = result.column_values('VertexID')
        if result:
            amount = 0
            for index in result:
                index = index.as_string()
                if int(index[len(self.typeOfVertex):]) > amount:
                    amount = int(index[len(self.typeOfVertex):])
            self.vid = self.typeOfVertex + str(amount + 1)
            return
        else:
            self.vid = self.typeOfVertex + '1'


a = Vertex(name='YA', typeOfVertex='Compute')
a.generate_vid()
print(a.vid)