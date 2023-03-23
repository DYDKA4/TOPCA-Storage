import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, exc
from sqlalchemy.engine import URL


def init_engine():
    try:
        load_dotenv()
        url = URL.create(
            "mysql+pymysql",
            username="root",
            password="example",
            host="DataBase",
            database="TOPCA_storage",
            port=32000)
        print(url)
        engine = create_engine(url)
    except exc.SQLAlchemyError as e:
        print(f"Error connecting to Database: {e}")
    return engine
