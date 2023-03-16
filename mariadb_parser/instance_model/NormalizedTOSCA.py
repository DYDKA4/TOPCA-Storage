from typing import Union

from pydantic import BaseModel


class Capability(BaseModel):
    attributes: dict[str, Union[str, None]] | None = {}
    properties: dict[str, Union[str, None]] | None = {}
    type: str | None = None


class Operation(BaseModel):
    implementation: str | None = None
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


class Node(BaseModel):
    attributes: dict[str, Union[str, None]] | None = {}
    capabilities: dict[str, Capability] | None = {}
    directives: list[Union[str, None]] | None = []
    interfaces: dict[str, Interface] | None = {}
    metadata: dict[str, str] | None = None
    properties: dict[str, Union[str, None]] | None = {}
    requirements: list[dict[str, Requirement]] | None = []
    type: str | None = None


class InstanceModel(BaseModel):
    inputs: dict[str, Union[str, None]] | None = {}
    nodes: dict[str, Node] | None = {}
    substitution_mappings: dict | None = None


