import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, exc


try:
    load_dotenv()
    engine = create_engine(str(os.environ.get('CONNECTION_STRING')))
except exc.SQLAlchemyError as e:
    print(f"Error connecting to Database: {e}")