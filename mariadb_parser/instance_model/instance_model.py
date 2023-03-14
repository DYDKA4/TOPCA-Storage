import json
import uuid
from typing import Union


# import yaml
#
# from mariadb_parser.instance_model.parse_puccini import TopologyTemplateInstance
# from mariadb_parser.instance_model.puccini_try import puccini_parse


class ToscaTemplateObject:

    def __init__(self, name: str):
        self.name = name
        self.database_id: str = str(uuid.uuid4())


class ParameterDefinition(ToscaTemplateObject):

    def __init__(self, name: str, type_of_parameter):
        super().__init__(name)
        self.instance_model: InstanceModel
        self.type_name: str
        self.type_link: object
        # todo realisation of data_type_linking
        self.description: str
        self.required: bool
        self.default: dict
        self.key_schema: dict
        self.entry_schema: dict
        self.type_of_parameter: str = type_of_parameter
        self.value_storage: ValueStorage
        self.mapping: dict


class NodeTemplate(ToscaTemplateObject):

    def __init__(self, name: str):
        super().__init__(name)
        self.instance_model: InstanceModel
        self.type_name: str
        self.type_link: object
        self.description: str
        self.metadata_value: dict
        self.copy_name: str
        self.copy_link: object
        self.properties: dict[str, AttributeAndPropertyFromNode] = {}
        self.attributes: dict[str, AttributeAndPropertyFromNode] = {}
        self.capabilities: dict[str, Capability] = {}
        self.interfaces: dict[str, NodeInterface] = {}
        self.requirements: list[Requirement] = []


class AttributeAndPropertyFromNode(ToscaTemplateObject):

    def __init__(self, name: str, type_of_parameter: str):
        super().__init__(name)
        self.node: NodeTemplate
        self.value_storage: ValueStorage
        self.type_of_parameter = type_of_parameter


class Capability(ToscaTemplateObject):

    def __init__(self, name: str):
        super().__init__(name)
        self.node: NodeTemplate
        self.value: dict
        self.attributes: dict[str, AttributeAndPropertyFromCapability] = {}
        self.properties: dict[str, AttributeAndPropertyFromCapability] = {}


class AttributeAndPropertyFromCapability(ToscaTemplateObject):
    def __init__(self, name: str, type_of_parameter: str):
        super().__init__(name)
        self.capability_object: Capability
        self.value_storage: ValueStorage
        self.type_of_parameter = type_of_parameter


class NodeInterface(ToscaTemplateObject):
    def __init__(self, name: str):
        super().__init__(name)
        self.node: NodeTemplate
        self.operations: dict[str, NodeInterfaceOperation] = {}


class NodeInterfaceOperation(ToscaTemplateObject):
    def __init__(self, name: str):
        super().__init__(name)
        self.interface: NodeInterface
        self.implementation: str
        self.inputs: dict[str, NodeInterfaceOperationInputOutput] = {}
        self.outputs: dict[str, NodeInterfaceOperationInputOutput] = {}


class NodeInterfaceOperationInputOutput(ToscaTemplateObject):
    def __init__(self, name: str, type_of_parameter: str, operation: NodeInterfaceOperation):
        super().__init__(name)
        self.operation: NodeInterfaceOperation = operation
        self.type_of_parameter: str = type_of_parameter
        self.value_storage: ValueStorage


class Requirement(ToscaTemplateObject):
    def __init__(self, name: str, node: NodeTemplate):
        super().__init__(name)
        self.capability: str
        self.father_node: NodeTemplate = node
        self.node: str
        self.node_link: NodeTemplate
        self.relationship: Relationship


class Relationship(ToscaTemplateObject):
    def __init__(self, requirement: Requirement, name=None):
        super().__init__(name)
        self.requirement: Requirement = requirement
        self.attributes: dict[str, AttributeAndPropertyFromRelationship] = {}
        self.properties: dict[str, AttributeAndPropertyFromRelationship] = {}
        self.interfaces: dict[str, RelationshipInterface] = {}


class AttributeAndPropertyFromRelationship(ToscaTemplateObject):
    def __init__(self, name: str, relationship: Relationship, type_of_parameter: str):
        super().__init__(name)
        self.relationship: Relationship = relationship
        self.value_storage: ValueStorage
        self.type_of_parameter = type_of_parameter


class RelationshipInterface(ToscaTemplateObject):
    def __init__(self, name: str, relationship: Relationship):
        super().__init__(name)
        self.relationship: Relationship = relationship
        self.operations: dict[str, RelationshipInterfaceOperation] = {}


class RelationshipInterfaceOperation(ToscaTemplateObject):
    def __init__(self, name: str, interface: RelationshipInterface):
        super().__init__(name)
        self.interface: RelationshipInterface = interface
        self.implementation: str
        self.inputs: dict[str, RelationshipInterfaceOperationInputOutputs] = {}
        self.outputs: dict[str, RelationshipInterfaceOperationInputOutputs] = {}


class RelationshipInterfaceOperationInputOutputs(ToscaTemplateObject):
    def __init__(self, name: str, type_of_parameter: str, operation: RelationshipInterfaceOperation):
        super().__init__(name)
        self.operation: RelationshipInterfaceOperation = operation
        self.type_of_parameter: str = type_of_parameter
        self.value_storage: ValueStorage


class ValueStorage:

    def __init__(self, data: Union[str, dict]):
        self.database_id: str = str(uuid.uuid4())

        self.data: Union[str, dict] = data

    def get_data_in_json(self):
        return json.dumps(self.data)


class InstanceModel:

    def __init__(self, data: dict):
        self.database_id: str = str(uuid.uuid4())
        self.description: str = data.get('description')
        self.inputs: dict[str, ParameterDefinition] = {}
        self.value_storage: list[ValueStorage] = []
        self.node_templates: dict[str, NodeTemplate] = {}

        if data.get('inputs'):
            for name, value in data.get('inputs').items():
                input_definition = ParameterDefinition(name, 'input')
                input_definition.instance_model = self
                value_object = ValueStorage(value)
                input_definition.value_storage = value_object
                self.value_storage.append(value_object)
                self.inputs[name] = input_definition
        if data.get('nodes'):
            for name, node_value in data.get('nodes').items():
                node_template = NodeTemplate(name)
                self.node_templates[name] = node_template
                if node_value.get('attributes'):
                    for attribute_name, attribute_value in node_value.get('attributes').items():
                        attribute = AttributeAndPropertyFromNode(attribute_name, "attribute")
                        value_object = ValueStorage(attribute_value)
                        attribute.value_storage = value_object
                        attribute.node = node_template
                        node_template.attributes[attribute_name] = attribute
                        self.value_storage.append(value_object)
                if node_value.get('properties'):
                    for property_name, property_value in node_value.get('properties').items():
                        property_object = AttributeAndPropertyFromNode(property_name, "property")
                        value_object = ValueStorage(property_value)
                        property_object.value_storage = value_object
                        property_object.node = node_template
                        node_template.properties[property_name] = property_object
                        self.value_storage.append(value_object)
                if node_value.get('capabilities'):
                    for capability_name, capability_value in node_value.get('capabilities').items():
                        capability_object = Capability(capability_name)
                        capability_object.node = node_template
                        node_template.capabilities[capability_name] = capability_object
                        if capability_value.get('attributes'):
                            for attribute_name, attribute_value in node_value.get('attributes').items():
                                attribute = AttributeAndPropertyFromCapability(attribute_name, "attribute")
                                value_object = ValueStorage(attribute_value)
                                attribute.value_storage = value_object
                                attribute.capability_object = capability_object
                                capability_object.attributes[attribute_name] = attribute
                                self.value_storage.append(value_object)
                        if capability_value.get('properties'):
                            for property_name, property_value in node_value.get('properties').items():
                                property_object = AttributeAndPropertyFromCapability(property_name, "property")
                                value_object = ValueStorage(property_value)
                                property_object.value_storage = value_object
                                property_object.capability_object = capability_object
                                capability_object.properties[property_name] = property_object
                                self.value_storage.append(value_object)
                if node_value.get('interfaces'):
                    for interface_name, interface_value in node_value.get('interfaces').items():
                        interface = NodeInterface(interface_name)
                        interface.node = node_template
                        node_template.interfaces[interface_name] = interface
                        if interface_value.get('operations'):
                            for operation_name, operation_value in interface_value.get('operations').items():
                                operation = NodeInterfaceOperation(operation_name)
                                operation.interface = interface
                                interface.operations[operation_name] = operation
                                if operation_value.get('implementation'):
                                    operation.implementation = operation_value.get('implementation')
                                if operation_value.get('inputs'):
                                    for input_name, input_value in data.get('inputs').items():
                                        input_assignments = NodeInterfaceOperationInputOutput(input_name,
                                                                                              'input',
                                                                                              operation)
                                        value_object = ValueStorage(input_value)
                                        input_assignments.value_storage = value_object
                                        self.value_storage.append(value_object)
                                        operation.inputs[input_name] = input_assignments
                                if operation_value.get('outputs'):
                                    for output_name, output_value in data.get('outputs').items():
                                        output_assignments = NodeInterfaceOperationInputOutput(output_name,
                                                                                               'output',
                                                                                               operation)
                                        value_object = ValueStorage(output_value)
                                        output_assignments.value_storage = value_object
                                        self.value_storage.append(value_object)
                                        operation.outputs[output_name] = output_assignments
                if node_value.get('metadata'):
                    node_template.metadata_value = node_value.get('metadata')
                if node_value.get('requirements'):
                    for requirement_element in node_value.get('requirements'):
                        for requirement_name, requirement_value in requirement_element.items():
                            requirement = Requirement(requirement_name, node_template)
                            if requirement_value.get('capability'):
                                requirement.capability = requirement_value.get('capability')
                            if requirement_value.get('node'):
                                requirement.node = requirement_value.get('node')
                            node_template.requirements.append(requirement)
                            if requirement_value.get('relationship'):
                                relationship = Relationship(requirement)
                                relationship_value = requirement_value.get('relationship')
                                requirement.relationship = relationship

                                if relationship_value.get('attributes'):
                                    for attribute_name, attribute_value in relationship_value.get('attributes').items():
                                        attribute = AttributeAndPropertyFromRelationship(attribute_name,
                                                                                         relationship,
                                                                                         "attribute")
                                        value_object = ValueStorage(attribute_value)
                                        attribute.value_storage = value_object
                                        relationship.attributes[attribute_name] = attribute
                                        self.value_storage.append(value_object)
                                if relationship_value.get('properties'):
                                    for property_name, property_value in relationship_value.get('properties').items():
                                        property_object = AttributeAndPropertyFromRelationship(property_name,
                                                                                               relationship,
                                                                                               "property")
                                        value_object = ValueStorage(property_value)
                                        property_object.value_storage = value_object
                                        relationship.properties[property_name] = property_object
                                        self.value_storage.append(value_object)
                                if requirement_value.get('interfaces'):

                                    for interface_name, interface_value in requirement_value.get('interfaces').items():
                                        interface = RelationshipInterface(interface_name, relationship)
                                        interface.node = node_template
                                        relationship.interfaces[interface_name] = interface

                                        if interface_value.get('operations'):
                                            for operation_name, operation_value in interface_value.get('operations'):
                                                operation = RelationshipInterfaceOperation(operation_name, interface)
                                                interface.operations[operation_name] = operation
                                                if operation_value.get('implementation'):
                                                    operation.implementation = operation_value.get('implementation')
                                                if operation_value.get('inputs'):
                                                    for input_name, input_value in data.get('inputs').items():
                                                        input_assignments = RelationshipInterfaceOperationInputOutputs(
                                                            input_name, 'input', operation)
                                                        value_object = ValueStorage(input_value)
                                                        input_assignments.value_storage = value_object
                                                        self.value_storage.append(value_object)
                                                        operation.inputs[input_name] = input_assignments
                                                if operation_value.get('outputs'):
                                                    for output_name, output_value in data.get('outputs').items():
                                                        output_assignments = RelationshipInterfaceOperationInputOutputs(
                                                            output_name, 'output', operation)
                                                        value_object = ValueStorage(output_value)
                                                        output_assignments.value_storage = value_object
                                                        self.value_storage.append(value_object)
                                                        operation.outputs[output_name] = output_assignments

# with open("template.yaml", 'r') as stream:
#     data = yaml.safe_load(stream)
#     topology = puccini_parse(str(data).encode("utf-8"))
#     # topology = InstanceModel("None", topology)
#     topology = TopologyTemplateInstance("None", topology)
#     data = InstanceModel(topology.render())
#     data
#     # data_loaded = test_data
#     # test = TypeStorage(data_loaded)
#     # loader = DataUploader('1.3', 'ust/test')
#     # loader.insert_type_storage(test)
