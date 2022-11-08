# <node_type_name>:
#   derived_from: <parent_node_type_name>
#   version: <version_number>
#   metadata:
#     <map of string>
#   description: <node_type_description>
#   attributes:
#     <attribute_definitions>
#   properties:
#     <property_definitions>
#   requirements:
#     - <requirement_definitions>
#   capabilities:
#     <capability_definitions>
#   interfaces:
#     <interface_definitions>
#   artifacts:
#     <artifact_definitions>
import json


class NodeType:
    def __init__(self, name: str, value: dict):
        self.vid = None
        self.vertex_type_system = 'NodeType'
        self.name = name
        self.data = json.dumps(value)


def node_type_parser(data: dict) -> list[NodeType]:
    node_types = []
    raw_node_types: dict = data.get('node_types')
    if raw_node_types:
        for name, data in raw_node_types.items():
            node_types.append(NodeType(name, data))
    return node_types
