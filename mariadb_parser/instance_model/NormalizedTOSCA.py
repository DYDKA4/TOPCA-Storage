from typing import Union

from pydantic import BaseModel


class Capability(BaseModel):
    attributes: dict[str, Union[str, None]] | None = None
    properties: dict[str, Union[str, None]] | None = None
    type: str | None = None


class Operation(BaseModel):
    implementation: str | None = None
    inputs: dict | None = None
    outputs: dict | None = None


class Interface(BaseModel):
    operations: dict[str, Operation] | None = None
    type: str | None = None


class Relationship(BaseModel):
    attributes: dict[str, Union[str, None]] | None = None
    interfaces: dict[str, Interface] | None = None
    properties: dict[str, Union[str, None]] | None = None
    type: str | None = None


class Requirement(BaseModel):
    capability: str | None = None
    node: str | None = None
    relationship: Relationship | None = None


class Node(BaseModel):
    attributes: dict[str, Union[str, None]] | None = None
    capabilities: dict[str, Capability] | None = None
    directives: list[Union[str, None]] | None = None
    interfaces: dict[str, Interface] | None = None
    metadata: dict[str, str] | None = None
    properties: dict[str, Union[str, None]] | None = None
    requirements: list[dict[str, Requirement]] | None = None
    type: str | None = None


class InstanceModel(BaseModel):
    inputs: dict[str, Union[str, None]] | None = None
    nodes: dict[str, Node] | None = None
    substitution_mappings: dict | None = None


