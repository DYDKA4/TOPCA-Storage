# import json

import yaml
from sqlalchemy import func
from sqlalchemy.orm import Session

from mariadb_parser.ORM_model.DataBase import Type, ArtifactStorage, DependencyTypes
from mariadb_parser.ORM_model.EngineInit import init_engine
from mariadb_parser.instance_model.instance_model import InstanceModel
from mariadb_parser.instance_model.parse_puccini import TopologyTemplateInstance
from mariadb_parser.instance_model.puccini_try import puccini_parse
from mariadb_parser.type_table.TypeStorage import TOSCAType, TypeStorage


# from tests.database_tests.yaml_data import test_data


class DataUploader:

    def __init__(self, tosca_definitions_version: str, path_to_type: str):
        self.engine = init_engine()
        self.engine.connect()
        self.path_to_type = path_to_type
        self.tosca_definitions_version = tosca_definitions_version
        self.type_list = ['data_types',
                          'group_types',
                          'interface_types',
                          'capability_types',
                          'policy_types',
                          'artifact_types',
                          'relationship_types',
                          'node_types']

    def __insert_type(self, tosca_types: dict, session: Session) -> None:
        tosca_objects = []
        for tosca_type in tosca_types.values():
            print(len(tosca_type.identifier))
            tosca_type: TOSCAType
            tosca_object = Type(
                id=tosca_type.identifier,
                version=tosca_type.version,
                type_of_type=tosca_type.type_of_type,
                type_name=tosca_type.name,
                data=tosca_type.get_data_in_json(),
                path_to_type=self.path_to_type,
                tosca_definitions_version=self.tosca_definitions_version)
            tosca_objects.append(tosca_object)
        session.bulk_save_objects(tosca_objects)
        return

    @staticmethod
    def __insert_dependency_derived_from(tosca_types: dict, session: Session):
        for data_type in tosca_types.values():
            for derived_from in data_type.derived_from:
                dependency = DependencyTypes(
                    source_id=data_type.identifier,
                    dependency_id=tosca_types[derived_from].identifier,
                    dependency_type='derived_from')
                session.add(dependency)

    def __insert_dependency(self, type_storage: TypeStorage, session: Session):
        for type_name in self.type_list:
            type_dict: dict = type_storage.__getattribute__(type_name)
            for node in type_dict.values():
                dependencies: dict = node.__getattribute__('dependencies')
                requirements: dict = node.__getattribute__('requirements')
                for dependency_type, dependency_set in dependencies.items():
                    for dependency_name in dependency_set:
                        destination_node = type_storage.__getattribute__(dependency_type)
                        destination_node = destination_node[dependency_name]
                        dependency = DependencyTypes(
                            source_id=node.identifier,
                            dependency_id=destination_node.identifier,
                            dependency_type='dependency')
                        session.add(dependency)
                for requirement_type, requirement_set in requirements.items():
                    for requirement_name in requirement_set:
                        destination_node = type_storage.__getattribute__(requirement_type)
                        destination_node = destination_node[requirement_name]
                        requirement = DependencyTypes(
                            source_id=node.identifier,
                            dependency_id=destination_node.identifier,
                            dependency_type='requirement_dependency')
                        session.add(requirement)

    def insert_type_storage(self, type_storage: TypeStorage):
        with Session(self.engine) as session:
            session.begin()
            try:

                for type_name in self.type_list:
                    type_dict: dict = type_storage.__getattribute__(type_name)
                    self.__insert_type(type_dict, session)
                    self.__insert_dependency_derived_from(type_dict, session)

                for artifact_definition in type_storage.artifacts.values():
                    session.add(
                        ArtifactStorage(
                            artifact_definition.identifier,
                            artifact_definition.name,
                            artifact_definition.get_data_in_json()
                        ))

                self.__insert_dependency(type_storage, session)
            except:
                session.rollback()
                raise
            else:
                session.commit()


class InstanceModelUploader:
    def __init__(self, instance_model: InstanceModel):
        self.engine = init_engine()
        self.engine.connect()
        self.instance_model = instance_model

        def insert_instance_model():
            with Session(self.engine) as session:
                session.begin()
                try:
                    print('try')
                except:
                    session.rollback()
                    raise
                else:
                    session.commit()


# with open("../instance_model/template.yaml", 'r') as stream:
#     data = yaml.safe_load(stream)
#     topology = puccini_parse(str(data).encode("utf-8"))
#     # topology = InstanceModel("None", topology)
#     topology = TopologyTemplateInstance("None", topology)
#     data = InstanceModel(topology.render())
#     data
#     # data_loaded = test_data
#     # test = TypeStorage(data_loaded)
#     # loader = DataUploader('1.3', 'ust/test')
#     # loader.insert_type_storage(test)
