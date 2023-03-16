# import json

import yaml
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from mariadb_parser.ORM_model.DataBase import (
    Type,
    ArtifactStorage,
    DependencyTypes,
    ValueStorage,
    DBInstanceModel,
    InstanceModelInputAndOutput,
    InputAndOutput,
    DBNodeTemplate,
    AttributeAndProperty,
    DBNodeAttributeAndProperty,
    DBCapability,
    DBCapabilityAttributeAndProperty,
    DBNodeInterface,
    DBNodeInterfaceOperation,
    DBNodeInterfaceOperationInputOutput,
    DBRequirement,
    DBRelationshipsAttributeAndProperty,
    DBRelationshipInterface,
    DBRelationshipInterfaceOperation,
    DBRelationshipInterfaceOperationInputOutput,
)
from mariadb_parser.ORM_model.EngineInit import init_engine
from mariadb_parser.instance_model.instance_model import (
    InstanceModel,
    ParameterDefinition,
    NodeTemplate,
    AttributeAndPropertyFromNode,
    Capability,
    AttributeAndPropertyFromCapability,
    NodeInterface,
    NodeInterfaceOperation,
    NodeInterfaceOperationInputOutput,
    Requirement,
    Relationship,
    AttributeAndPropertyFromRelationship,
    RelationshipInterface,
    RelationshipInterfaceOperation,
    RelationshipInterfaceOperationInputOutputs,
)
from mariadb_parser.instance_model.parse_puccini import TopologyTemplateInstance
from mariadb_parser.instance_model.puccini_try import puccini_parse
from mariadb_parser.type_table.TypeStorage import TOSCAType, TypeStorage


# from tests.database_tests.yaml_data import test_data


class DataUploader:
    def __init__(self, tosca_definitions_version: str, path_to_type: str):
        self.engine = init_engine()
        self.engine.connect()
        self.path_to_type = path_to_type
        self.tosca_definitions_version = tosca_definitions_version
        self.type_list = [
            "data_types",
            "group_types",
            "interface_types",
            "capability_types",
            "policy_types",
            "artifact_types",
            "relationship_types",
            "node_types",
        ]

    def __insert_type(self, tosca_types: dict, session: Session) -> None:
        tosca_objects = []
        for tosca_type in tosca_types.values():
            tosca_type: TOSCAType
            tosca_object = Type(
                id=tosca_type.identifier,
                version=tosca_type.version,
                type_of_type=tosca_type.type_of_type,
                type_name=tosca_type.name,
                data=tosca_type.get_data_in_json(),
                path_to_type=self.path_to_type,
                tosca_definitions_version=self.tosca_definitions_version,
            )
            tosca_objects.append(tosca_object)
        session.bulk_save_objects(tosca_objects)
        return

    @staticmethod
    def __insert_dependency_derived_from(tosca_types: dict, session: Session):
        for data_type in tosca_types.values():
            for derived_from in data_type.derived_from:
                dependency = DependencyTypes(
                    source_id=data_type.identifier,
                    dependency_id=tosca_types[derived_from].identifier,
                    dependency_type="derived_from",
                )
                session.add(dependency)

    def __insert_dependency(self, type_storage: TypeStorage, session: Session):
        for type_name in self.type_list:
            type_dict: dict = type_storage.__getattribute__(type_name)
            for node in type_dict.values():
                dependencies: dict = node.__getattribute__("dependencies")
                requirements: dict = node.__getattribute__("requirements")
                for dependency_type, dependency_set in dependencies.items():
                    for dependency_name in dependency_set:
                        destination_node = type_storage.__getattribute__(
                            dependency_type
                        )
                        destination_node = destination_node[dependency_name]
                        dependency = DependencyTypes(
                            source_id=node.identifier,
                            dependency_id=destination_node.identifier,
                            dependency_type="dependency",
                        )
                        session.add(dependency)
                for requirement_type, requirement_set in requirements.items():
                    for requirement_name in requirement_set:
                        destination_node = type_storage.__getattribute__(
                            requirement_type
                        )
                        destination_node = destination_node[requirement_name]
                        requirement = DependencyTypes(
                            source_id=node.identifier,
                            dependency_id=destination_node.identifier,
                            dependency_type="requirement_dependency",
                        )
                        session.add(requirement)

    def insert_type_storage(self, type_storage: TypeStorage):
        with Session(self.engine) as session:
            session.begin()
            try:

                for type_name in self.type_list:
                    type_dict: dict = type_storage.__getattribute__(type_name)
                    self.__insert_type(type_dict, session)
                    self.__insert_dependency_derived_from(type_dict, session)

                for artifact_definition in type_storage.artifacts.values():
                    session.add(
                        ArtifactStorage(
                            artifact_definition.identifier,
                            artifact_definition.name,
                            artifact_definition.get_data_in_json(),
                        )
                    )

                self.__insert_dependency(type_storage, session)
            except Exception:
                session.rollback()
                raise
            else:
                session.commit()


class InstanceModelUploader:
    def __init__(self, instance_model: InstanceModel):
        self.engine = init_engine()
        self.engine.connect()
        self.instance_model = instance_model

    def insert_instance_model(self):
        with Session(self.engine) as session:
            session: Session
            session.begin()
            try:
                objects = []
                for value_object in self.instance_model.value_storage:
                    value_model = ValueStorage(
                        id=value_object.database_id, value=value_object.data
                    )
                    objects.append(value_model)
                    # session.add(value_model)
                instance_model = DBInstanceModel(
                    id=self.instance_model.database_id,
                    description=self.instance_model.description,
                    metadata_value=self.instance_model.metadata,
                )
                objects.append(instance_model)
                # session.add(instance_model)
                for input_value in self.instance_model.inputs.values():
                    input_value: ParameterDefinition
                    input_object = InstanceModelInputAndOutput(
                        id=input_value.database_id,
                        instance_model_id=input_value.instance_model.database_id,
                        type=InputAndOutput.input,
                        value_storage_id=input_value.value_storage.database_id,
                        name=None if input_value.name == "" else input_value.name,
                        type_name=None
                        if input_value.type_name == ""
                        else input_value.type_name,
                        type_id=None
                        if input_value.type_link == ""
                        else input_value.type_link,
                        description=None
                        if input_value.description == ""
                        else input_value.description,
                        mapping=None
                        if input_value.mapping == {}
                        else input_value.mapping,
                        required=input_value.required,
                        default=None
                        if input_value.default == {}
                        else input_value.default,
                        key_schema=None
                        if input_value.key_schema == {}
                        else input_value.key_schema,
                        entry_schema=None
                        if input_value.entry_schema == {}
                        else input_value.entry_schema,
                    )
                    objects.append(input_object)
                    # session.add(input_object)
                node_templates: dict[
                    str, NodeTemplate
                ] = self.instance_model.node_templates
                for node_template in node_templates.values():
                    node_template: NodeTemplate
                    node_object = DBNodeTemplate(
                        id=node_template.database_id,
                        instance_model_id=node_template.instance_model.database_id,
                        name=node_template.name,
                        type_name=None
                        if node_template.type_name == ""
                        else node_template.type_name,
                        type_id=None
                        if node_template.type_link == ""
                        else node_template.type_link,
                        description=None
                        if node_template.type_name == ""
                        else node_template.type_name,
                        metadata_value=None
                        if node_template.metadata_value == {}
                        else node_template.metadata_value,
                        copy_name=None
                        if node_template.copy_name == ""
                        else node_template.copy_name,
                        # copy_id=None #todo NoteImplemented
                    )
                    objects.append(node_object)
                    for property_value in node_template.properties.values():
                        property_value: AttributeAndPropertyFromNode
                        property_object = DBNodeAttributeAndProperty(
                            id=property_value.database_id,
                            name=property_value.name,
                            type=AttributeAndProperty.property,
                            node_id=property_value.node.database_id,
                            value_storage_id=property_value.value_storage.database_id,
                        )
                        objects.append(property_object)
                    for attribute_value in node_template.attributes.values():
                        attribute_value: AttributeAndPropertyFromNode
                        attribute_object = DBNodeAttributeAndProperty(
                            id=attribute_value.database_id,
                            name=attribute_value.name,
                            type=AttributeAndProperty.attribute,
                            node_id=attribute_value.node.database_id,
                            value_storage_id=attribute_value.value_storage.database_id,
                        )
                        objects.append(attribute_object)
                    for capability_value in node_template.capabilities.values():
                        capability_value: Capability
                        capability_entity = DBCapability(
                            id=capability_value.database_id,
                            name=capability_value.name,
                            node_id=capability_value.node.database_id,
                            value=None
                            if capability_value.value == {}
                            else capability_value.value,
                            type=capability_value.type_name,
                        )
                        objects.append(capability_entity)
                        for property_value in capability_value.properties.values():
                            property_value: AttributeAndPropertyFromCapability
                            property_object = DBCapabilityAttributeAndProperty(
                                id=property_value.database_id,
                                name=property_value.name,
                                type=AttributeAndProperty.property,
                                capability_id=property_value.capability_object.database_id,
                                value_storage_id=property_value.value_storage.database_id,
                            )
                            objects.append(property_object)
                        for attribute_value in capability_value.attributes.values():
                            attribute_value: AttributeAndPropertyFromCapability
                            attribute_object = DBCapabilityAttributeAndProperty(
                                id=attribute_value.database_id,
                                name=attribute_value.name,
                                type=AttributeAndProperty.attribute,
                                capability_id=attribute_value.capability_object.database_id,
                                value_storage_id=attribute_value.value_storage.database_id,
                            )
                            objects.append(attribute_object)
                    for node_interface in node_template.interfaces.values():
                        node_interface: NodeInterface
                        interface_object = DBNodeInterface(
                            id=node_interface.database_id,
                            node_id=node_interface.node.database_id,
                            name=node_interface.name,
                        )
                        objects.append(interface_object)
                        for operation in node_interface.operations.values():
                            operation: NodeInterfaceOperation
                            operation_object = DBNodeInterfaceOperation(
                                id=operation.database_id,
                                node_interface_id=operation.interface.database_id,
                                name=operation.name,
                                implementation=operation.implementation,
                            )
                            objects.append(operation_object)
                            for input_value in operation.inputs.values():
                                input_value: NodeInterfaceOperationInputOutput
                                input_object = DBNodeInterfaceOperationInputOutput(
                                    id=input_value.database_id,
                                    name=input_value.name,
                                    operation_id=input_value.operation.database_id,
                                    type=InputAndOutput.input,
                                    value_storage_id=input_value.value_storage.database_id,
                                )
                                objects.append(input_object)
                            for output_value in operation.outputs.values():
                                output_value: NodeInterfaceOperationInputOutput
                                output_object = DBNodeInterfaceOperationInputOutput(
                                    id=output_value.database_id,
                                    name=output_value.name,
                                    operation_id=output_value.operation.database_id,
                                    type=InputAndOutput.output,
                                    value_storage_id=output_value.value_storage.database_id,
                                )
                                objects.append(output_object)
                for node_template in node_templates.values():
                    for requirement in node_template.requirements:
                        requirement: Requirement
                        requirement_object = DBRequirement(
                            id=requirement.database_id,
                            name=requirement.name,
                            node_link=requirement.node_link.database_id,
                            node=requirement.node,
                            node_id=requirement.father_node.database_id,
                            capability=requirement.capability,
                        )
                        objects.append(requirement_object)
                        relationship: Relationship = requirement.relationship
                        for property_value in relationship.properties.values():
                            property_value: AttributeAndPropertyFromRelationship
                            property_object = DBRelationshipsAttributeAndProperty(
                                id=property_value.database_id,
                                name=property_value.name,
                                type=AttributeAndProperty.property,
                                requirement_id=property_value.relationship.database_id,
                                value_storage_id=property_value.value_storage.database_id,
                            )
                            objects.append(property_object)
                        for attribute_value in relationship.attributes.values():
                            attribute_value: AttributeAndPropertyFromRelationship
                            attribute_object = DBRelationshipsAttributeAndProperty(
                                id=attribute_value.database_id,
                                name=attribute_value.name,
                                type=AttributeAndProperty.attribute,
                                requirement_id=attribute_value.relationship.database_id,
                                value_storage_id=attribute_value.value_storage.database_id,
                            )
                            objects.append(attribute_object)
                        for relationship_interface in relationship.interfaces.values():
                            relationship_interface: RelationshipInterface
                            interface_object = DBRelationshipInterface(
                                id=relationship_interface.database_id,
                                requirement_id=relationship_interface.relationship.database_id,
                                name=relationship_interface.name,
                            )
                            objects.append(interface_object)
                            for operation in relationship_interface.operations.values():
                                operation: RelationshipInterfaceOperation
                                operation_object = DBRelationshipInterfaceOperation(
                                    id=operation.database_id,
                                    relationship_interface_id=operation.interface.database_id,
                                    name=operation.name,
                                    implementation=operation.implementation,
                                )
                                objects.append(operation_object)
                                for input_value in operation.inputs.values():
                                    input_value: RelationshipInterfaceOperationInputOutputs
                                    input_object = DBRelationshipInterfaceOperationInputOutput(
                                        id=input_value.database_id,
                                        name=input_value.name,
                                        operation_id=input_value.operation.database_id,
                                        type=InputAndOutput.input,
                                        value_storage_id=input_value.value_storage.database_id,
                                    )
                                    objects.append(input_object)
                                for output_value in operation.outputs.values():
                                    output_value: RelationshipInterfaceOperationInputOutputs
                                    output_object = DBRelationshipInterfaceOperationInputOutput(
                                        id=output_value.database_id,
                                        name=output_value.name,
                                        operation_id=output_value.operation.database_id,
                                        type=InputAndOutput.output,
                                        value_storage_id=output_value.value_storage.database_id,
                                    )
                                    objects.append(output_object)
                session.bulk_save_objects(objects)
            except Exception:
                session.rollback()
                raise
            else:
                session.commit()


# with open("../instance_model/template.yaml", 'r') as stream:
#     data = yaml.safe_load(stream)
#     topology = puccini_parse(str(data).encode("utf-8"))
#     # topology = InstanceModel("None", topology)
#     topology = TopologyTemplateInstance("None", topology)
#     data = InstanceModel(topology.render())
#     uploader = InstanceModelUploader(data)
#     uploader.insert_instance_model()
