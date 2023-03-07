# from __future__ import annotations
from typing import Any, Match, Union
from pydantic import BaseModel, constr
import re


class TypeStorageAnswer(BaseModel):
    user: str
    dir: str | None = None
    file_namew: str
    result: dict[str, Any]


class ServiceTemplateDefinitionMetadata(BaseModel):
    template_name: str | None = None
    template_author: str | None = None
    template_version: constr(regex=r"^[0-9]+\.[0-9]+(\.[0-9]+(\.[a-zA-Z]+(-[0-9]+)?)?)?$") | None = None


class ImportDefinition(BaseModel):
    file: str
    namespace_prefix: str | None = None


class SchemaDefinition(BaseModel):
    type: str
    description: str | None = None
    constraints: list[Any] | None = None

    key_schema: 'SchemaDefinition'  # NOTE UPDATE LATER
    entry_schema: 'SchemaDefinition'  # NOTE UPDATE LATER


class PropertyDefinition(BaseModel):
    type: str
    description: str | None = None
    required: bool | None = None
    default: Any | None = None
    # status NS
    constraints: list[Any] | None = None  # NOTE UPDATE LATER
    key_schema: SchemaDefinition | None = None  # NOTE UPDATE LATER
    entry_schema: SchemaDefinition | None = None  # NOTE UPDATE LATER
    metadata: dict[str, str] | None = None


class ArtifactType(BaseModel):
    derived_from: str
    version: constr(regex=r"^[0-9]+\.[0-9]+(\.[0-9]+(\.[a-zA-Z]+(-[0-9]+)?)?)?$") | None = None
    metadata: dict[str, str] | None = None
    description: str | None = None
    mime_type: str | None = None
    file_ext: list[str] | None = None
    properties: dict[str, PropertyDefinition] | None = None


class DataType(BaseModel):
    derived_from: str
    version: constr(regex=r"^[0-9]+\.[0-9]+(\.[0-9]+(\.[a-zA-Z]+(-[0-9]+)?)?)?$") | None = None
    metadata: dict[str, str] | None = None
    description: str | None = None
    constraints: list[Any] | None = None  # NOTE UPDATE LATER
    properties: dict[str, PropertyDefinition] | None = None
    key_schema: SchemaDefinition | None = None  # NOTE UPDATE LATER
    entry_schema: SchemaDefinition | None = None  # NOTE UPDATE LATER


class AttributeDefinition(BaseModel):
    type: str
    description: str | None = None
    default: Any | None = None
    # status NS
    key_schema: SchemaDefinition | None = None  # NOTE UPDATE LATER
    entry_schema: SchemaDefinition | None = None  # NOTE UPDATE LATER


class CapabilityType(BaseModel):
    derived_from: str
    version: constr(regex=r"^[0-9]+\.[0-9]+(\.[0-9]+(\.[a-zA-Z]+(-[0-9]+)?)?)?$") | None = None
    metadata: dict[str, str] | None = None
    description: str | None = None
    properties: dict[str, PropertyDefinition] | None = None
    attributes: dict[str, AttributeDefinition] | None = None
    valid_source_types: list[str] | None = None


class ParameterDefinition(BaseModel):
    type: str
    description: str | None = None
    value: Any | None = None
    required: bool | None = None
    default: Any | None = None
    # status NS
    # validation NS
    key_schema: SchemaDefinition | None = None  # NOTE UPDATE LATER
    entry_schema: SchemaDefinition | None = None  # NOTE UPDATE LATER
    mapping: list[str] | None = None  # TODO LATED


class ArtifactDefinition(BaseModel):
    type: str
    file: str
    # repository NS
    description: str
    deploy_path: str
    artifact_version: str
    checksum: str
    checksum_algorithm: str
    properties: dict[str, Any]


class OperationImplementationDefinition(BaseModel):
    primary: ArtifactDefinition | None = None
    dependencies: list[ArtifactDefinition] | None = None
    timeout: int | None = None


class OperationDefinition(BaseModel):
    description: str | None = None
    implementation: Union[OperationImplementationDefinition, str] | None = None
    inputs: dict[str, Union[ParameterDefinition, Any]] | None = None
    outputs: dict[str, Union[ParameterDefinition, Any]] | None = None


class InterfaceType(BaseModel):
    derived_from: str
    version: constr(regex=r"^[0-9]+\.[0-9]+(\.[0-9]+(\.[a-zA-Z]+(-[0-9]+)?)?)?$") | None = None
    metadata: dict[str, str] | None = None
    description: str | None = None
    inputs: dict[str, Union[ParameterDefinition, Any]] | None = None
    operations: dict[str, Union[OperationDefinition, str]] | None = None
    # notifications NS


class InterfaceDefinition(BaseModel):
    type: str
    description: str | None = None
    inputs: dict[str, Union[ParameterDefinition, Any]]
    operations: dict[str, Union[OperationDefinition, str]]


class RelationshipType(BaseModel):
    derived_from: str
    version: constr(regex=r"^[0-9]+\.[0-9]+(\.[0-9]+(\.[a-zA-Z]+(-[0-9]+)?)?)?$") | None = None
    metadata: dict[str, str] | None = None
    description: str | None = None
    properties: dict[str, PropertyDefinition] | None = None
    attributes: dict[str, AttributeDefinition] | None = None
    interfaces: dict[str, InterfaceDefinition] | None = None
    valid_target_types: list[str] | None = None


class RequirementDefinition(BaseModel):
    description: str | None = None
    capability: str
    node: str | None = None
    relationship: str | None = None
    # node_filter NS
    occurrences: constr(regex=r"^\[(\d+|UNBOUNDED),(\d+|UNBOUNDED)\]$")


class CapabilityDefinition(BaseModel):
    type: str
    description: str | None = None
    properties: dict[str, PropertyDefinition] | None = None
    attributes: dict[str, AttributeDefinition] | None = None
    valid_source_types: list[str] | None = None
    occurrences: constr(regex=r"^\[(\d+|UNBOUNDED),(\d+|UNBOUNDED)\]$")


class NodeType(BaseModel):
    derived_from: str
    version: constr(regex=r"^[0-9]+\.[0-9]+(\.[0-9]+(\.[a-zA-Z]+(-[0-9]+)?)?)?$") | None = None
    metadata: dict[str, str] | None = None
    description: str | None = None
    attributes: dict[str, AttributeDefinition] | None = None
    properties: dict[str, PropertyDefinition] | None = None
    requirements: list[RequirementDefinition] | None = None
    capabilities: dict[str, Union[CapabilityDefinition, str]] | None = None
    interfaces: dict[str, InterfaceDefinition] | None = None
    artifacts: dict[str, ArtifactDefinition] | None = None


class AttributeAssignment(BaseModel):
    description: str | None = None
    value: Any | None = None


class OperationAssignment(BaseModel):
    implementation: OperationImplementationDefinition | None = None
    inputs: dict[str, Any] | None = None
    # outputs NS


class InterfaceAssignment(BaseModel):
    inputs: dict[str, Any] | None = None
    operations: dict[str, OperationAssignment] | None = None
    # notifications: NS


class RequirementAssignmentRelationship(BaseModel):
    type: str | None = None
    properties: dict[str, Any] | None = None
    attributes: dict[str, Union[AttributeAssignment, Any]] | None = None
    interfaces: dict[str, InterfaceAssignment] | None = None


class RequirementAssignment(BaseModel):
    capability: str | None = None
    node: str | None = None
    relationship: str | RequirementAssignmentRelationship | None = None
    # node_filter NS
    occurrences: constr(regex=r"^\[(\d+|UNBOUNDED),(\d+|UNBOUNDED)\]$") | None = None


class CapabilityAssignment(BaseModel):
    properties: dict[str, Any] | None = None
    attributes: dict[str, Union[AttributeAssignment, Any]] | None = None
    occurrences: constr(regex=r"^\[(\d+|UNBOUNDED),(\d+|UNBOUNDED)\]$") | None = None


class NodeTemplate(BaseModel):
    type: str
    description: str | None = None
    metadata: dict[str, str] | None = None
    # directives NS | None = None
    properties: dict[str, Any] | None = None
    attributes: dict[str, Union[AttributeAssignment, Any]] | None = None
    requirements: list[RequirementAssignment] | None = None
    capabilities: dict[str, CapabilityAssignment] | None = None
    interfaces: dict[str, InterfaceAssignment] | None = None
    artifacts: dict[str, ArtifactDefinition] | None = None
    # node_filter NS | None = None
    # copy NS | None = None


class RelationshipTemplate(BaseModel):
    type: str
    description: str | None = None
    metadata: dict[str, str] | None = None
    properties: dict[str, Any] | None = None
    attributes: dict[str, Union[AttributeAssignment, Any]] | None = None
    interfaces: dict[str, InterfaceAssignment] | None = None
    # copy NS


class TopologyTemplate(BaseModel):
    description: str | None = None
    inputs: dict[str, Union[ParameterDefinition, Any]] | None = None
    node_templates: dict[str, NodeTemplate] | None = None
    relationship_templates: dict[str, RelationshipTemplate] | None = None
    # groups NS
    # policies NS
    outputs: dict[str, Union[ParameterDefinition, Any]] | None = None
    # substitution_mappings NS
    # workflows NS


class ServiceTemplateDefinition(BaseModel):
    tosca_definitions_version = "tosca_simple_yaml_1_3"
    # namespace NS
    # dsl_definitions NS
    metadata: ServiceTemplateDefinitionMetadata | None = None
    description: str | None = None
    imports: list[Union[ImportDefinition | str]] | None = None
    artifact_types: dict[str, ArtifactType] | None = None
    data_types: dict[str, DataType] | None = None
    capability_types: dict[str, CapabilityType] | None = None
    interface_types: dict[str, InterfaceType] | None = None
    relationship_types: dict[str, RelationshipType] | None = None
    # group_types NS
    # policy_types NS
    node_types: dict[str, NodeType] | None = None
    topology_template: TopologyTemplate | None = None
