from sqlalchemy import create_engine, exc, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

try:
    engine = create_engine(
        "mariadb+mariadbconnector://root:password@localhost:3306/type_templatesAPI?charset=utf8mb4")
    engine.connect()
except exc.SQLAlchemyError as e:
    print(f"Error connecting to Database: {e}")

Base = declarative_base()


class ArtifactDefinition(Base):
    __tablename__ = "artifact_storage"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=32))
    data = Column(JSON)

    def __repr__(self):
        return "<artifact_storage(name='%s', data='%s')>" % (
            self.name,
            self.data
        )
class DependencyTypes(Base):
    __tablename__ = "dependency_types"

    id = Column(Integer)