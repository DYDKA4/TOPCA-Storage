from mariadb_parser.ORM_model.EngineInit import init_engine
from sqlalchemy.orm import Session
from mariadb_parser.ORM_model.DataBase import Type
import json


class DataGetter:
    def __init__(self, path):
        self.path = path
        self.engine = init_engine()
        self.engine.connect()
        self.result = {'artifact_types': {},
                       'data_types': {},
                       'capability_types': {},
                       'interface_types': {},
                       'relationship_types': {},
                       'node_types': {},
                       'group_types': {},
                       'policy_types': {}}

    def get_types(self):
        with Session(self.engine) as session:
            session.begin()
            try:
                for tosca_type in session.query(Type).filter_by(path_to_type=self.path):
                    self.result[
                        tosca_type.type_of_type._value_ + 's'][
                        tosca_type.type_name] = json.loads(tosca_type.data)
            except:
                session.rollback()
                raise
            else:
                session.commit()
