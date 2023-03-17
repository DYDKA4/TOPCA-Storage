from typing import Union

from pydantic import BaseModel


class Capability(BaseModel):
    attributes: dict[str, Union[str, None]] | None = {}
    properties: dict[str, Union[str, None]] | None = {}
    type: str | None = None


class ImplementationDefinition(BaseModel):
    primary: str
    dependencies: list[str] = []
    operation_host: str = 'SELF'


class Operation(BaseModel):
    implementation: ImplementationDefinition | None = None
    inputs: dict | None = {}
    outputs: dict | None = {}


class Interface(BaseModel):
    operations: dict[str, Operation] | None = {}
    type: str | None = None


class Relationship(BaseModel):
    attributes: dict[str, Union[str, None]] | None = {}
    interfaces: dict[str, Interface] | None = {}
    properties: dict[str, Union[str, None]] | None = {}
    type: str | None = None


class Requirement(BaseModel):
    capability: str | None = None
    node: str | None = None
    relationship: Relationship | None = None
    directives: list[Union[str, None]] = []


class Node(BaseModel):
    attributes: dict[str, Union[str, None]] | None = {}
    capabilities: dict[str, Capability] | None = {}
    directives: list[Union[str, None]] | None = []
    interfaces: dict[str, Interface] | None = {}
    metadata: dict[str, str] = {}
    properties: dict[str, Union[str, None]] | None = {}
    requirements: list[dict[str, Requirement]] | None = []
    artifacts: dict = {}
    type: str | None = None


class InstanceModel(BaseModel):
    inputs: dict[str, Union[str, None]] | None = {}
    nodes: dict[str, Node] | None = {}
    metadata: dict[str, str] = {}
    substitution_mappings: dict | None = None
