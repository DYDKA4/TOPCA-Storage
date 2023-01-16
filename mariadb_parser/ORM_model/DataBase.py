import enum

from sqlalchemy import Column, Integer, String, JSON, Enum, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base

from mariadb_parser.ORM_model.EngineInit import engine

Base = declarative_base()

engine.connect()


class DependencyTypeEnum(enum.Enum):
    derived_from = 'derived_from'
    requirement_dependency = 'requirement_dependency'
    dependency = 'dependency'


class TypeOfTypeEnum(enum.Enum):
    artifact_type = 'artifact_type'
    data_type = 'data_type'
    capability_type = 'capability_type'
    interface_type = 'interface_type'
    relationship_type = 'relationship_type'
    node_type = 'node_type'
    group_type = 'group_type'
    policy_type = 'policy_type'


class ArtifactDefinition(Base):
    __tablename__ = "artifact_storage"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=32), nullable=False)
    data = Column(JSON, nullable=False)

    def __repr__(self):
        return "<artifact_storage(name='%s', data='%s')>" % (
            self.name,
            self.data
        )


class DependencyTypes(Base):
    __tablename__ = "dependency_types"

    source_id = Column(Integer, ForeignKey("type.id"), primary_key=True, nullable=False)
    dependency_id = Column(Integer, ForeignKey("type.id"), primary_key=True, nullable=False)
    dependency_type = Column(Enum(DependencyTypeEnum), primary_key=True, nullable=False)
    Index("type_dependency_types_dependency_id_index", "dependency_id")
    Index("type_dependency_types_source_id_index", "source_id")

    def __repr__(self):
        return "<DependencyTypes(source_id='%d', dependency_id='%d', dependency_id='%d' )>" % (
            self.source_id,
            self.dependency_id,
            self.dependency_type
        )


class Type(Base):
    __tablename__ = "type"

    id = Column(Integer, primary_key=True, nullable=False)
    version = Column(String(length=32), nullable=False)
    type_of_type = Column(Enum(TypeOfTypeEnum), nullable=False)
    type_name = Column(String(length=32), nullable=False)
    data = Column(JSON, nullable=False)


class TypeStorageToArtifactStorage(Base):
    __tablename__ = "type_storage_to_artifact_storage"

    artifact_storage_id = Column(Integer, ForeignKey("artifact_storage.id"), primary_key=True, nullable=False)
    type_storage_id = Column(Integer, ForeignKey("type.id"), primary_key=True, nullable=False)
