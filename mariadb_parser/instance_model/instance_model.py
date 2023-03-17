import json
import uuid
from typing import Union

import yaml

from mariadb_parser.instance_model.parse_puccini import TopologyTemplateInstance
from mariadb_parser.instance_model.puccini_try import puccini_parse


# import yaml
#
# from mariadb_parser.instance_model.parse_puccini import TopologyTemplateInstance
# from mariadb_parser.instance_model.puccini_try import puccini_parse


class ToscaTemplateObject:

    def __init__(self, name: str):
        self.name = name
        self.database_id: str = str(uuid.uuid4())


class ParameterDefinition(ToscaTemplateObject):

    def __init__(self, name: str, type_of_parameter, instance_model: "InstanceModelInternal", value_storage: "ValueStorage"):
        super().__init__(name)
        self.instance_model: InstanceModelInternal = instance_model
        self.type_name: str = ""
        self.type_link: str = ""
        # todo realisation of data_type_linking
        self.description: str = ""
        self.required: bool = True
        self.default: dict = {}
        self.key_schema: dict = {}
        self.entry_schema: dict = {}
        self.type_of_parameter: str = type_of_parameter
        self.value_storage: ValueStorage = value_storage
        self.mapping: dict = {}


class NodeTemplate(ToscaTemplateObject):

    def __init__(self, name: str, instance_model: "InstanceModelInternal", type_name: str, directives: list[str]):
        super().__init__(name)
        self.instance_model: InstanceModelInternal = instance_model
        self.type_name: str = type_name
        self.type_link: str = ""
        self.description: str = ""
        self.metadata_value: dict = {}
        self.copy_name: str = ""
        self.copy_link: object = None
        self.properties: dict[str, AttributeAndPropertyFromNode] = {}
        self.attributes: dict[str, AttributeAndPropertyFromNode] = {}
        self.capabilities: dict[str, Capability] = {}
        self.interfaces: dict[str, NodeInterface] = {}
        self.requirements: list[Requirement] = []
        self.directives: list[str] = directives


class AttributeAndPropertyFromNode(ToscaTemplateObject):

    def __init__(self, name: str, type_of_parameter: str, node: NodeTemplate, value_storage: "ValueStorage"):
        super().__init__(name)
        self.node: NodeTemplate = node
        self.value_storage: ValueStorage = value_storage
        self.type_of_parameter = type_of_parameter


class Capability(ToscaTemplateObject):

    def __init__(self, name: str, node: NodeTemplate, type_name: str):
        super().__init__(name)
        self.node: NodeTemplate = node
        self.value: dict = {}
        self.attributes: dict[str, AttributeAndPropertyFromCapability] = {}
        self.properties: dict[str, AttributeAndPropertyFromCapability] = {}
        self.type_name: str | None = type_name


class AttributeAndPropertyFromCapability(ToscaTemplateObject):
    def __init__(self, name: str, type_of_parameter: str, capability: Capability, value_storage: "ValueStorage"):
        super().__init__(name)
        self.capability_object: Capability = capability
        self.value_storage: ValueStorage = value_storage
        self.type_of_parameter = type_of_parameter


class NodeInterface(ToscaTemplateObject):
    def __init__(self, name: str, node: NodeTemplate, type_name: str):
        super().__init__(name)
        self.node: NodeTemplate = node
        self.operations: dict[str, NodeInterfaceOperation] = {}
        self.type_name: str = type_name


class NodeInterfaceOperation(ToscaTemplateObject):
    def __init__(self, name: str, interface: NodeInterface, implementation: dict):
        super().__init__(name)
        self.interface: NodeInterface = interface
        self.implementation: dict = implementation
        self.inputs: dict[str, NodeInterfaceOperationInputOutput] = {}
        self.outputs: dict[str, NodeInterfaceOperationInputOutput] = {}


class NodeInterfaceOperationInputOutput(ToscaTemplateObject):
    def __init__(self, name: str,
                 type_of_parameter: str,
                 operation: NodeInterfaceOperation,
                 value_storage: "ValueStorage"):
        super().__init__(name)
        self.operation: NodeInterfaceOperation = operation
        self.type_of_parameter: str = type_of_parameter
        self.value_storage: ValueStorage = value_storage


class Requirement(ToscaTemplateObject):
    def __init__(self, name: str, node: NodeTemplate, node_name: str, capability: str, order: int):
        super().__init__(name)
        self.capability: str | None = capability
        self.father_node: NodeTemplate = node
        self.node: str | None = node_name
        self.node_link: NodeTemplate | None = None
        self.relationship: Relationship | None = None
        self.order: int = order


class Relationship(ToscaTemplateObject):
    def __init__(self, requirement: Requirement, type_name: str, name=None):
        super().__init__(name)
        self.database_id: str = requirement.database_id
        self.requirement: Requirement = requirement
        self.attributes: dict[str, AttributeAndPropertyFromRelationship] = {}
        self.properties: dict[str, AttributeAndPropertyFromRelationship] = {}
        self.interfaces: dict[str, RelationshipInterface] = {}
        self.type_name: str = type_name


class AttributeAndPropertyFromRelationship(ToscaTemplateObject):
    def __init__(self, name: str, relationship: Relationship, type_of_parameter: str, value_storage: "ValueStorage"):
        super().__init__(name)
        self.relationship: Relationship = relationship
        self.value_storage: ValueStorage = value_storage
        self.type_of_parameter = type_of_parameter


class RelationshipInterface(ToscaTemplateObject):
    def __init__(self, name: str, relationship: Relationship, type_name: str):
        super().__init__(name)
        self.relationship: Relationship = relationship
        self.operations: dict[str, RelationshipInterfaceOperation] = {}
        self.type_name: str = type_name


class RelationshipInterfaceOperation(ToscaTemplateObject):
    def __init__(self, name: str, interface: RelationshipInterface, implementation: str | None):
        super().__init__(name)
        self.interface: RelationshipInterface = interface
        self.implementation: str | None = implementation
        self.inputs: dict[str, RelationshipInterfaceOperationInputOutputs] = {}
        self.outputs: dict[str, RelationshipInterfaceOperationInputOutputs] = {}


class RelationshipInterfaceOperationInputOutputs(ToscaTemplateObject):
    def __init__(self, name: str, type_of_parameter: str, operation: RelationshipInterfaceOperation,
                 value_storage: "ValueStorage"):
        super().__init__(name)
        self.operation: RelationshipInterfaceOperation = operation
        self.type_of_parameter: str = type_of_parameter
        self.value_storage: ValueStorage = value_storage


class ValueStorage:

    def __init__(self, data: Union[str, dict]):
        self.database_id: str = str(uuid.uuid4())

        self.data: Union[str, dict] = data

    def get_data_in_json(self):
        return json.dumps(self.data)


class InstanceModelInternal:

    def __init__(self, data: dict):
        self.database_id: str = str(uuid.uuid4())
        self.description: str = data.get('description')
        self.inputs: dict[str, ParameterDefinition] = {}
        self.value_storage: list[ValueStorage] = []
        self.node_templates: dict[str, NodeTemplate] = {}
        self.metadata = {}

        if data.get('inputs'):
            for name, value in data.get('inputs').items():
                value_object = ValueStorage(value)
                input_definition = ParameterDefinition(name, 'input', self, value_object)
                input_definition.instance_model = self
                input_definition.value_storage = value_object
                self.value_storage.append(value_object)
                self.inputs[name] = input_definition
        self.metadata = data.get("metadata")
        if data.get('nodes'):
            for name, node_value in data.get('nodes').items():
                node_template = NodeTemplate(name, self, node_value.get('type'), node_value.get('directives'))
                self.node_templates[name] = node_template
                if node_value.get('attributes'):
                    for attribute_name, attribute_value in node_value.get('attributes').items():
                        value_object = ValueStorage(attribute_value)
                        attribute = AttributeAndPropertyFromNode(attribute_name,
                                                                 "attribute",
                                                                 node_template,
                                                                 value_object)
                        node_template.attributes[attribute_name] = attribute
                        self.value_storage.append(value_object)
                if node_value.get('properties'):
                    for property_name, property_value in node_value.get('properties').items():
                        value_object = ValueStorage(property_value)
                        property_object = AttributeAndPropertyFromNode(property_name,
                                                                       "property",
                                                                       node_template,
                                                                       value_object)
                        node_template.properties[property_name] = property_object
                        self.value_storage.append(value_object)
                if node_value.get('capabilities'):
                    for capability_name, capability_value in node_value.get('capabilities').items():
                        capability_object = Capability(capability_name, node_template, capability_value.get('type'))
                        node_template.capabilities[capability_name] = capability_object
                        if capability_value.get('attributes'):
                            for attribute_name, attribute_value in capability_value.get('attributes').items():
                                value_object = ValueStorage(attribute_value)
                                attribute = AttributeAndPropertyFromCapability(attribute_name,
                                                                               "attribute",
                                                                               capability_object,
                                                                               value_object)
                                capability_object.attributes[attribute_name] = attribute
                                self.value_storage.append(value_object)
                        if capability_value.get('properties'):
                            for property_name, property_value in capability_value.get('properties').items():
                                value_object = ValueStorage(property_value)
                                property_object = AttributeAndPropertyFromCapability(property_name,
                                                                                     "property",
                                                                                     capability_object,
                                                                                     value_object)
                                capability_object.properties[property_name] = property_object
                                self.value_storage.append(value_object)
                if node_value.get('interfaces'):
                    for interface_name, interface_value in node_value.get('interfaces').items():
                        interface = NodeInterface(interface_name, node_template, interface_value.get('type'))
                        node_template.interfaces[interface_name] = interface
                        if interface_value.get('operations'):
                            for operation_name, operation_value in interface_value.get('operations').items():
                                operation = NodeInterfaceOperation(operation_name,
                                                                   interface,
                                                                   operation_value.get('implementation'))
                                interface.operations[operation_name] = operation
                                if operation_value.get('inputs'):
                                    for input_name, input_value in operation_value.get('inputs').items():
                                        value_object = ValueStorage(input_value)
                                        input_assignments = NodeInterfaceOperationInputOutput(input_name,
                                                                                              'input',
                                                                                              operation,
                                                                                              value_object)
                                        self.value_storage.append(value_object)
                                        operation.inputs[input_name] = input_assignments
                                if operation_value.get('outputs'):
                                    for output_name, output_value in operation_value.get('outputs').items():
                                        value_object = ValueStorage(output_value)
                                        output_assignments = NodeInterfaceOperationInputOutput(output_name,
                                                                                               'output',
                                                                                               operation,
                                                                                               value_object)
                                        self.value_storage.append(value_object)
                                        operation.outputs[output_name] = output_assignments
                if node_value.get('metadata'):
                    node_template.metadata_value = node_value.get('metadata')
                if node_value.get('requirements'):
                    for requirement_element in node_value.get('requirements'):
                        for requirement_name, requirement_value in requirement_element.items():
                            requirement = Requirement(requirement_name,
                                                      node_template,
                                                      requirement_value.get('node'),
                                                      requirement_value.get('capability'),
                                                      len(node_template.requirements))
                            node_template.requirements.append(requirement)
                            if requirement_value.get('relationship'):
                                relationship_value = requirement_value.get('relationship')
                                relationship = Relationship(requirement, relationship_value.get('type'))
                                requirement.relationship = relationship

                                if relationship_value.get('attributes'):
                                    for attribute_name, attribute_value in relationship_value.get('attributes').items():
                                        value_object = ValueStorage(attribute_value)
                                        attribute = AttributeAndPropertyFromRelationship(attribute_name,
                                                                                         relationship,
                                                                                         "attribute",
                                                                                         value_object)
                                        relationship.attributes[attribute_name] = attribute
                                        self.value_storage.append(value_object)
                                if relationship_value.get('properties'):
                                    for property_name, property_value in relationship_value.get('properties').items():
                                        value_object = ValueStorage(property_value)
                                        property_object = AttributeAndPropertyFromRelationship(property_name,
                                                                                               relationship,
                                                                                               "property",
                                                                                               value_object)
                                        relationship.properties[property_name] = property_object
                                        self.value_storage.append(value_object)
                                if relationship_value.get('interfaces'):
                                    for interface_name, interface_value in relationship_value.get('interfaces').items():
                                        interface = RelationshipInterface(interface_name, relationship,
                                                                          interface_value.get('type'))
                                        interface.node = node_template
                                        relationship.interfaces[interface_name] = interface

                                        if interface_value.get('operations'):
                                            for operation_name, operation_value in interface_value.get(
                                                    'operations').items():
                                                operation = RelationshipInterfaceOperation(operation_name,
                                                                                           interface,
                                                                                           operation_value.get(
                                                                                               'implementation')
                                                                                           )
                                                interface.operations[operation_name] = operation
                                                if operation_value.get('inputs'):
                                                    for input_name, input_value in operation_value.get(
                                                            'inputs').items():
                                                        value_object = ValueStorage(input_value)
                                                        input_assignments = RelationshipInterfaceOperationInputOutputs(
                                                            input_name, 'input', operation, value_object)
                                                        self.value_storage.append(value_object)
                                                        operation.inputs[input_name] = input_assignments
                                                if operation_value.get('outputs'):
                                                    for output_name, output_value in operation_value.get(
                                                            'outputs').items():
                                                        value_object = ValueStorage(output_value)
                                                        output_assignments = RelationshipInterfaceOperationInputOutputs(
                                                            output_name, 'output', operation, value_object)
                                                        self.value_storage.append(value_object)
                                                        operation.outputs[output_name] = output_assignments
        for node_template in self.node_templates.values():
            for requirement in node_template.requirements:
                requirement.node_link = self.node_templates.get(requirement.node)


#
# with open("tosca-service-templates/templates/ray/ray-master.yaml", 'r') as stream:
#     data = yaml.safe_load(stream)
#     topology = puccini_parse(str(data).encode("utf-8"))
#     # topology = InstanceModelInternal("None", topology)
#     topology = TopologyTemplateInstance("None", topology)
#     with open("input.yaml", 'w') as f:
#         f.write(yaml.dump(topology.render()))
#     data
#     # data_loaded = test_data
#     # test = TypeStorage(data_loaded)
#     # loader = DataUploader('1.3', 'ust/test')
#     # loader.insert_type_storage(test)
