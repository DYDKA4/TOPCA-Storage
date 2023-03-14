import enum

from sqlalchemy import Column, Integer, String, JSON, Enum, ForeignKey, Index, Text, Boolean, BINARY
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

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    name = Column(String(length=255), nullable=False)
    data = Column(JSON, nullable=False)

    def __repr__(self):
        return "<artifact_storage(name='%s', data='%s')>" % (
            self.name,
            self.data
        )


class Capability(Base):
    __tablename__ = "capability"

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    name = Column(String(length=255), nullable=False)
    node_id = Column(BINARY(length=36), ForeignKey("node_template.id", ondelete='CASCADE'), nullable=False)
    value = Column(JSON)

    def __repr__(self):
        return "<capability(name='%s', data='%s')>" % (
            self.name,
            self.value
        )


class CapabilityAttributeAndProperty(Base):
    __tablename__ = "capability_attribute_and_property"

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    name = Column(String(length=255), nullable=False)
    type = Column(Enum(AttributeAndProperty), nullable=False)
    capability_id = Column(BINARY(length=36), ForeignKey("capability.id", ondelete='CASCADE'), nullable=False)
    value_storage_id = Column(BINARY(length=36), ForeignKey("value_storage.id", ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return "<attribute_and_property_from_capability(name='%s', data='%s')>" % (
            self.name,
            self.type
        )


class DependencyTypes(Base):
    __tablename__ = "dependency_types"

    source_id = Column(BINARY(length=36), ForeignKey("type.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    dependency_id = Column(BINARY(length=36), ForeignKey("type.id", ondelete='CASCADE'), primary_key=True,
                           nullable=False)
    dependency_type = Column(Enum(DependencyTypeEnum), primary_key=True, nullable=False)
    Index("type_dependency_types_dependency_id_index", "dependency_id")
    Index("type_dependency_types_source_id_index", "source_id")


class InstanceModel(Base):
    __tablename__ = "instance_model"

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    description = Column(Text)
    metadata_value = Column(JSON)


# class GetFunctions(Base):
#     __tablename__ = "get_functions"
#
#     source_id = Column(Integer, ForeignKey("value_storage.id", ondelete='CASCADE'), primary_key=True, nullable=False)
#     target_id = Column(Integer, ForeignKey("value_storage.id", ondelete='CASCADE'), primary_key=True, nullable=False)


class InstanceModelInputAndOutput(Base):
    __tablename__ = "instance_model_input_and_output_from"

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    instance_model_id = Column(BINARY(length=36), ForeignKey("instance_model.id", ondelete='CASCADE'), nullable=False)
    type = Column(Enum(InputAndOutput), nullable=False)
    value_storage_id = Column(BINARY(length=36), ForeignKey("value_storage.id", ondelete='CASCADE'), nullable=False)
    name = Column(String(length=255), nullable=False)
    type_name = Column(String(length=255))
    type_id = Column(BINARY(length=36), ForeignKey("type.id", ondelete='CASCADE'))
    description = Column(Text)
    mapping = Column(JSON)
    required = Column(Boolean)
    default = Column(JSON)
    key_schema = Column(JSON)
    entry_schema = Column(JSON)


class NodeAttributeAndProperty(Base):
    __tablename__ = "node_attribute_and_property"

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    name = Column(String(length=255), nullable=False)
    type = Column(Enum(AttributeAndProperty), nullable=False)
    node_id = Column(BINARY(length=36), ForeignKey("node_template.id", ondelete='CASCADE'), nullable=False)
    value_storage_id = Column(BINARY(length=36), ForeignKey("value_storage.id", ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return "<attribute_and_property_from_node(name='%s', data='%s')>" % (
            self.name,
            self.type
        )


class NodeInterface(Base):
    __tablename__ = "node_interface"

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    node_id = Column(BINARY(length=36), ForeignKey('node_template.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(length=255), nullable=False)


class NodeInterfaceOperation(Base):
    __tablename__ = "node_interface_operation"

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    node_interface_id = Column(BINARY(length=36), ForeignKey('node_interface.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(length=255), nullable=False)
    implementation = Column(JSON, nullable=False)


class NodeInterfaceOperationInputOutput(Base):
    __tablename__ = "node_interface_operation_input_output"

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    name = Column(String(length=255), nullable=False)
    operation_id = Column(BINARY(length=36),
                          ForeignKey('node_interface_operation.id', ondelete='CASCADE'),
                          nullable=False)
    type = Column(Enum(InputAndOutput), nullable=False)
    value_storage_id = Column(BINARY(length=36), ForeignKey('value_storage.id', ondelete='CASCADE'), nullable=False)


class NodeTemplate(Base):
    __tablename__ = "node_template"

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    instance_model_id = Column(BINARY(length=36), ForeignKey('instance_model.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(length=255), nullable=False)
    type_name = Column(String(length=255), nullable=False)
    type_id = Column(BINARY(length=36), ForeignKey('type.id', ondelete='CASCADE'))
    description = Column(Text)
    metadata_value = Column(JSON)
    copy_name = Column(String(length=255))
    copy_id = Column(BINARY(length=36), ForeignKey('node.id', ondelete='CASCADE'))
    # substitute = Column(BINARY(length=36), ForeignKey('instance_model.id'))


class RelationshipsAttributeAndProperty(Base):
    __tablename__ = 'relationships_property_and_attribute'

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    type = Column(Enum(AttributeAndProperty), nullable=False)
    relationship_id = Column(BINARY(length=36), ForeignKey('relationship.id', ondelete='CASCADE'), nullable=False)
    value_storage_id = Column(BINARY(length=36), ForeignKey('value_storage.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(length=255), nullable=False)


class RelationshipsInterface(Base):
    __tablename__ = 'relationships_interface'

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    relationship_id = Column(BINARY(length=36), ForeignKey('relationship.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(length=255), nullable=False)


class RelationshipsInterfaceOperation(Base):
    __tablename__ = 'relationships_interface_operation'

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    relationship_id = Column(BINARY(length=36), ForeignKey('relationships_interface.id',
                                                           ondelete='CASCADE'), nullable=False)
    name = Column(String(length=255), nullable=False)
    implementation = Column(String(length=255), nullable=False)


class RelationshipsInterfaceOperationInputOutput(Base):
    __tablename__ = "relationship_interface_operation_input_output"

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    name = Column(String(length=255), nullable=False)
    operation_id = Column(BINARY(length=36),
                          ForeignKey('relationships_interface_operation.id', ondelete='CASCADE'),
                          nullable=False)
    type = Column(Enum(InputAndOutput), nullable=False)
    value_storage_id = Column(BINARY(length=36), ForeignKey('value_storage.id', ondelete='CASCADE'), nullable=False)


class Requirement(Base):
    __tablename__ = 'requirement'

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    name = Column(String(length=255), nullable=False)
    node_link = Column(BINARY(length=36), ForeignKey('node_template.id', ondelete='CASCADE'), nullable=False)
    node = Column(String(length=255), nullable=False)
    node_id = Column(BINARY(length=36), ForeignKey('node_template.id', ondelete='CASCADE'), nullable=False)
    value = Column(JSON)
    capability = Column(String(length=255))


class Type(Base):
    __tablename__ = "type"

    id = Column(BINARY(length=36), primary_key=True, nullable=False)
    version = Column(String(length=32), nullable=False)
    type_of_type = Column(Enum(TypeOfTypeEnum), nullable=False)
    type_name = Column(String(length=32), nullable=False)
    data = Column(JSON, nullable=False)
    path_to_type = Column(String(length=255), nullable=False)
    tosca_definitions_version = Column(String(length=32), nullable=False)


class TypeStorageToArtifactStorage(Base):
    __tablename__ = "ts_to_as"

    artifact_storage_id = Column(BINARY(length=36), ForeignKey("artifact_storage.id"), primary_key=True, nullable=False)
    type_storage_id = Column(BINARY(length=36), ForeignKey("type.id"), primary_key=True, nullable=False)


class ValueStorage(Base):
    __tablename__ = "value_storage"

    id = Column(Integer, primary_key=True, nullable=False)
    data = Column(JSON)
