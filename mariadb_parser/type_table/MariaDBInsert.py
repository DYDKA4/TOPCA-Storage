import mariadb
import os
import sys
from dotenv import load_dotenv

from mariadb_parser.type_table.TypeStorage import TOSCAType


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
def insert_TOSCAtype(tosca_types: TOSCAType):
    conn = open_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO employees (first_name,last_name) VALUES (?, ?)", ("Maria", "DB"))
    except mariadb.Error as e:
        print(f"Error: {e}")

