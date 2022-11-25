import mariadb
import os
import sys

import yaml
from dotenv import load_dotenv

from mariadb_parser.type_table.TypeStorage import TOSCAType, TypeStorage


# Connect to MariaDB Platform\\
def open_connection():
    load_dotenv()
    try:
        conn = mariadb.connect(
            user=str(os.environ.get('MARIADB_USER')),
            password=str(os.environ.get('PASSWORD')),
            host=str(os.environ.get('HOST')),
            port=int(os.environ.get('PORT')),
            database=str(os.environ.get('DATABASE'))

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn


# Get Cursor
def get_max_identifier(table_name: str, cur) -> int:
    try:
        cur.execute(f"SELECT MAX(id) FROM {os.environ.get('DATABASE')}.{table_name};", ("Maria", "DB"))
    except mariadb.Error as e:
        print(f"Error: {e}")
    max_identifier = cur.fetchone()[0]
    if max_identifier is None:
        max_identifier = 0
    return max_identifier


def insert_type(tosca_types: dict, cur, max_size: int) -> None:
    for tosca_type in tosca_types.values():
        tosca_type: TOSCAType
        cur.execute("INSERT INTO type_templatesAPI.type (id, version, type_of_type, type_name, data) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (tosca_type.identifier + max_size, tosca_type.version,
                     tosca_type.type_of_type, tosca_type.name, tosca_type.get_data_in_json()))
        tosca_type.identifier += max_size
    return


def insert_dependency_derived_from(tosca_types: dict, cur):
    for data_type in tosca_types.values():
        for derived_from in data_type.derived_from:
            cur.execute("INSERT INTO type_templatesAPI.dependency_types"
                        "(source_id, dependency_id, dependency_type) VALUES (?, ?, ?)",
                        (data_type.identifier, tosca_types[derived_from].identifier, 'derived_from'))


def insert_type_storage(type_storage: TypeStorage):
    conn = open_connection()
    cur = conn.cursor()
    max_identifier_type = get_max_identifier('type', cur)
    max_identifier_artifact = get_max_identifier('artifact_storage', cur)

    try:
        insert_type(type_storage.data_types, cur, max_identifier_type)
        insert_dependency_derived_from(type_storage.data_types, cur)

        insert_type(type_storage.artifact_types, cur, max_identifier_type)
        insert_dependency_derived_from(type_storage.artifact_types, cur)

        insert_type(type_storage.capability_types, cur, max_identifier_type)
        insert_dependency_derived_from(type_storage.capability_types, cur)

        insert_type(type_storage.interface_types, cur, max_identifier_type)
        insert_dependency_derived_from(type_storage.interface_types, cur)

        insert_type(type_storage.relationship_types, cur, max_identifier_type)
        insert_dependency_derived_from(type_storage.relationship_types, cur)

        insert_type(type_storage.node_types, cur, max_identifier_type)
        insert_dependency_derived_from(type_storage.node_types, cur)

        insert_type(type_storage.group_types, cur, max_identifier_type)
        insert_dependency_derived_from(type_storage.group_types, cur)

        insert_type(type_storage.policy_types, cur, max_identifier_type)
        insert_dependency_derived_from(type_storage.policy_types, cur)

        for artifact_definition in type_storage.artifact_definition.values():
            cur.execute("INSERT INTO type_templatesAPI.artifact_storage (id, data, name) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (artifact_definition.identifier + max_identifier_type, artifact_definition.get_data_in_json(),
                         artifact_definition.name))
    except mariadb.Error as e:
        print(f"Error: {e}")

    conn.commit()
    print()


with open("test.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)
    test = TypeStorage(data_loaded)
    insert_type_storage(test)
