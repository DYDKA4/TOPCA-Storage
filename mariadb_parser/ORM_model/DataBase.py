import enum

from sqlalchemy import Column, Integer, String, JSON, Enum, ForeignKey, Index, Text
from sqlalchemy.ext.declarative import declarative_base

from mariadb_parser.ORM_model.EngineInit import init_engine

Base = declarative_base()

engine = init_engine()
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


class AttributeAndProperty(enum.Enum):
    type_attribute = 'attribute'
    type_property = 'property'


class InputAndOutput(enum.Enum):
    output = 'output'
    input = 'input'


class ArtifactStorage(Base):
    __tablename__ = "artifact_storage"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=32), nullable=False)
    data = Column(JSON, nullable=False)

    def __repr__(self):
        return "<artifact_storage(name='%s', data='%s')>" % (
            self.name,
            self.data
        )


class AttributeAndPropertyFromCapability(Base):
    __tablename__ = "attribute_and_property_from_capability"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=32), nullable=False)
    type = Column(Enum(AttributeAndProperty), nullable=False)
    capability_id = Column(Integer, ForeignKey("capability.id", ondelete='CASCADE'), nullable=False)
    value_storage_id = Column(Integer, ForeignKey("value_storage.id", ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return "<attribute_and_property_from_capability(name='%s', data='%s')>" % (
            self.name,
            self.type
        )


class AttributeAndPropertyFromNode(Base):
    __tablename__ = "attribute_and_property_from_node"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=32), nullable=False)
    type = Column(Enum(AttributeAndProperty), nullable=False)
    node_id = Column(Integer, ForeignKey("node.id", ondelete='CASCADE'), nullable=False)
    value_storage_id = Column(Integer, ForeignKey("value_storage.id", ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return "<attribute_and_property_from_node(name='%s', data='%s')>" % (
            self.name,
            self.type
        )


class Capability(Base):
    __tablename__ = "capability"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=32), nullable=False)
    node_id = Column(Integer, ForeignKey("node.id", ondelete='CASCADE'), nullable=False)
    value = Column(JSON)

    def __repr__(self):
        return "<capability(name='%s', data='%s')>" % (
            self.name,
            self.value
        )


class DependencyTypes(Base):
    __tablename__ = "dependency_types"

    source_id = Column(Integer, ForeignKey("type.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    dependency_id = Column(Integer, ForeignKey("type.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    dependency_type = Column(Enum(DependencyTypeEnum), primary_key=True, nullable=False)
    Index("type_dependency_types_dependency_id_index", "dependency_id")
    Index("type_dependency_types_source_id_index", "source_id")

    def __repr__(self):
        return "<DependencyTypes(source_id='%d', dependency_id='%d', dependency_id='%d' )>" % (
            self.source_id,
            self.dependency_id,
            self.dependency_type
        )


class GetFunctions(Base):
    __tablename__ = "get_functions"

    source_id = Column(Integer, ForeignKey("value_storage.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    target_id = Column(Integer, ForeignKey("value_storage.id", ondelete='CASCADE'), primary_key=True, nullable=False)


class InputAndOutputFromInstanceModel(Base):
    __tablename__ = "input_and_output_from_instance_model"

    id = Column(Integer, primary_key=True, nullable=False)
    instance_model_id = Column(Integer, ForeignKey("instance_model.id", ondelete='CASCADE'), nullable=False)
    type = Column(Enum(InputAndOutput), nullable=False)
    value_storage_id = Column(Integer, ForeignKey("value_storage.id", ondelete='CASCADE'), nullable=False)


class InputFromInterfaceInNode(Base):
    __tablename__ = "input_from_interface_in_node"

    id = Column(Integer, primary_key=True, nullable=False)
    father_node_if = Column(Integer, ForeignKey('interface_from_node_template.id', ondelete='CASCADE'), nullable=False)
    value_storage_id = Column(Integer, ForeignKey('value_storage.id', ondelete='CASCADE'), nullable=False)


class InstanceModel(Base):
    __tablename__ = "instance_model"

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(Text)
    metadata_value = Column(JSON)


class InterfaceFromNodeTemplate(Base):
    __tablename__ = "table_name"

    id = Column(Integer, primary_key=True, nullable=False)
    node_id = Column(Integer, ForeignKey('node.id', ondelete='CASCADE'), nullable=False)
    implementation = Column(JSON)
    name = Column(String(length=32), nullable=False)


class InterfacesInputFromRelationship(Base):
    __tablename__ = "interfaces_input_from_relationship"

    id = Column(Integer, primary_key=True, nullable=False)
    interface_id = Column(Integer, ForeignKey('relationships_interface.id', ondelete='CASCADE'), nullable=False)
    value_storage_id = Column(Integer, ForeignKey('value_storage.id', ondelete='CASCADE'), nullable=False)


class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True, nullable=False)
    instance_model_id = Column(Integer, ForeignKey('instance_model.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(length=32), nullable=False)
    type_id = Column(Integer, ForeignKey('type.id', ondelete='CASCADE'), nullable=False)
    description = Column(Text)
    metadata_value = Column(JSON)
    copy = Column(Integer, ForeignKey('node.id', ondelete='CASCADE'))
    substitute = Column(Integer, ForeignKey('instance_model.id'))


class NodeToArtifactStorage(Base):
    __tablename__ = 'node_to_artifact_storage'

    node_id = Column(Integer, ForeignKey('node.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    artifact_storage_id = Column(Integer, ForeignKey('artifact_storage.id', ondelete='CASCADE'), primary_key=True,
                                 nullable=False)


class Relationship(Base):
    __tablename__ = 'relationship'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=32), nullable=False)
    instance_model_id = Column(Integer, ForeignKey('instance_model.id', ondelete='CASCADE'), nullable=False)
    description = Column(Text)
    metadata_value = Column(JSON)
    copy = Column(Integer, ForeignKey('relationship.id', ondelete='CASCADE'))
    type_id = Column(Integer, ForeignKey('type.id', ondelete='CASCADE'), nullable=False)


class RelationshipsInterface(Base):
    __tablename__ = 'relationships_interface'

    id = Column(Integer, primary_key=True, nullable=False)
    relationship_id = Column(Integer, ForeignKey('relationship.id', ondelete='CASCADE'), nullable=False)
    implementation = Column(JSON, nullable=False)


class RelationshipsPropertyAndAttribute(Base):
    __tablename__ = 'relationships_property_and_attribute'

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(Enum(AttributeAndProperty), nullable=False)
    relationship_id = Column(Integer, ForeignKey('relationship.id', ondelete='CASCADE'), nullable=False)
    value_storage_id = Column(Integer, ForeignKey('value_storage.id', ondelete='CASCADE'), nullable=False)


class Requirement(Base):
    __tablename__ = 'requirement'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=32), nullable=False)
    target_node_id = Column(Integer, ForeignKey('node.id', ondelete='CASCADE'))
    node_filter = Column(JSON)
    node_id = Column(Integer, ForeignKey('node.id', ondelete='CASCADE'), nullable=False)
    value = Column(JSON)
    relationship_id = Column(Integer, ForeignKey('relationship.id', ondelete='CASCADE'))


class Type(Base):
    __tablename__ = "type"

    id = Column(Integer, primary_key=True, nullable=False)
    version = Column(String(length=32), nullable=False)
    type_of_type = Column(Enum(TypeOfTypeEnum), nullable=False)
    type_name = Column(String(length=32), nullable=False)
    data = Column(JSON, nullable=False)
    path_to_type = Column(String(length=255), nullable=False)
    tosca_definitions_version = Column(String(length=10), nullable=False)



class TypeStorageToArtifactStorage(Base):
    __tablename__ = "type_storage_to_artifact_storage"

    artifact_storage_id = Column(Integer, ForeignKey("artifact_storage.id"), primary_key=True, nullable=False)
    type_storage_id = Column(Integer, ForeignKey("type.id"), primary_key=True, nullable=False)


class ValueStorage(Base):
    __tablename__ = "value_storage"

    id = Column(Integer, primary_key=True, nullable=False)
    data = Column(JSON)
