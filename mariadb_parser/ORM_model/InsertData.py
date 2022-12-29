import mariadb
import os

import yaml
from sqlalchemy import func
from sqlalchemy.orm import Session, DeclarativeMeta

from mariadb_parser.ORM_model.DataBase import Type, ArtifactDefinition, DependencyTypes
from mariadb_parser.type_table.TypeStorage import TOSCAType, TypeStorage
from EngineInit import engine

engine.connect()


def insert_type(tosca_types: dict, session: Session, max_size: int) -> None:
    tosca_objects = []
    for tosca_type in tosca_types.values():
        tosca_type: TOSCAType
        tosca_type.identifier += max_size
        tosca_object = Type(
            id=tosca_type.identifier,
            version=tosca_type.version,
            type_of_type=tosca_type.type_of_type,
            type_name=tosca_type.name,
            data=tosca_type.get_data_in_json())
        tosca_objects.append(tosca_object)
    session.bulk_save_objects(tosca_objects)
    return


def insert_dependency_derived_from(tosca_types: dict, session: Session):
    for data_type in tosca_types.values():
        for derived_from in data_type.derived_from:
            dependency = DependencyTypes(
                source_id=data_type.identifier,
                dependency_id=tosca_types[derived_from].identifier,
                dependency_type='derived_from')
            session.add(dependency)


def insert_dependency(type_storage: TypeStorage, session: Session):
    order_list = ['data_types', 'group_types', 'interface_types', 'capability_types', 'policy_types',
                  'artifact_types', 'relationship_types', 'node_types']
    for type_name in order_list:
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
            # for requirement_type, requirement_set in requirements.items():
            #     for requirement_name in requirement_set:
            #         destination_node = type_storage.__getattribute__(requirement_type)
            #         destination_node = destination_node[requirement_name]
            #         dependency = DependencyTypes(
            #             source_id=node.identifier,
            #             dependency_id=destination_node.identifier,
            #             dependency_type='requirement_dependency')
                    session.add(dependency)

def insert_type_storage(type_storage: TypeStorage):
    with Session(engine) as session:
        session.begin()
        try:
            max_identifier_type = session.query(func.max(Type.id))
            max_identifier_artifact = session.query(func.max(ArtifactDefinition.id))
            max_identifier_type = max_identifier_type[0][0] if max_identifier_type[0][0] is not None else 0
            max_identifier_artifact = max_identifier_artifact[0][0] if max_identifier_artifact[0][0] is not None else 0
            insert_type(type_storage.data_types, session, max_identifier_type)

            insert_type(type_storage.artifact_types, session, max_identifier_type)
            insert_dependency_derived_from(type_storage.artifact_types, session)

            insert_type(type_storage.capability_types, session, max_identifier_type)
            insert_dependency_derived_from(type_storage.capability_types, session)

            insert_type(type_storage.interface_types, session, max_identifier_type)
            insert_dependency_derived_from(type_storage.interface_types, session)

            insert_type(type_storage.relationship_types, session, max_identifier_type)
            insert_dependency_derived_from(type_storage.relationship_types, session)

            insert_type(type_storage.node_types, session, max_identifier_type)
            insert_dependency_derived_from(type_storage.node_types, session)

            insert_type(type_storage.group_types, session, max_identifier_type)
            insert_dependency_derived_from(type_storage.group_types, session)

            insert_type(type_storage.policy_types, session, max_identifier_type)
            insert_dependency_derived_from(type_storage.policy_types, session)

            for artifact_definition in type_storage.artifacts.values():
                artifact_definition.identifier += max_identifier_artifact
                session.add(
                    ArtifactDefinition(
                        artifact_definition.identifier,
                        artifact_definition.name,
                        artifact_definition.get_data_in_json()
                    ))

            insert_dependency(type_storage, session)
        except:
            session.rollback()
            raise
        else:
            session.commit()

    #
    #     for artifact_definition in type_storage.artifacts.values():
    #         session.execute("INSERT INTO type_templatesAPI.artifact_storage (id, data, name) "
    #                     "VALUES (?, ?, ?, ?, ?)",
    #                     (artifact_definition.identifier + max_identifier_type, artifact_definition.get_data_in_json(),
    #                      artifact_definition.name))
    # except mariadb.Error as e:
    #     print(f"Error: {e}")
    #
    # conn.commit()
    # print()


with open("../type_table/test.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)
    test = TypeStorage(data_loaded)
    insert_type_storage(test)
