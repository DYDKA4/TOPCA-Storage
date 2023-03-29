import yaml

from mariadb_parser.ORM_model.EngineInit import init_engine
from sqlalchemy.orm import Session
from mariadb_parser.ORM_model.DataBase import (
    Type,
    DBInstanceModel,
    InstanceModelInputAndOutput,
    ValueStorage,
    InputAndOutput,
    DBNodeTemplate,
    DBNodeAttributeAndProperty,
    AttributeAndProperty,
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
import json

from mariadb_parser.instance_model.NormalizedTOSCA import (
    InstanceModel,
    Node,
    Capability,
    Interface,
    Operation,
    Requirement,
    Relationship, ImplementationDefinition,
)
from mariadb_parser.instance_model.parse_puccini import TopologyTemplateInstance
from mariadb_parser.instance_model.puccini_try import puccini_parse


class DataGetter:
    def __init__(self, uuid:str):
        self.database_id = uuid
        self.engine = init_engine()
        self.engine.connect()
        self.result = {
            "artifact_types": {},
            "data_types": {},
            "capability_types": {},
            "interface_types": {},
            "relationship_types": {},
            "node_types": {},
            "group_types": {},
            "policy_types": {},
        }

    def get_types(self):
        with Session(self.engine) as session:
            session.begin()
            try:
                for tosca_type in session.query(Type).filter_by(header_id=self.database_id):
                    self.result[tosca_type.type_of_type._value_ + "s"][
                        tosca_type.type_name
                    ] = json.loads(tosca_type.data)
            except Exception:
                session.rollback()
                raise
            else:
                session.commit()


class InstanceModelGetter:
    def __init__(self, uuid: str):
        self.uuid: str = uuid
        self.engine = init_engine()
        self.engine.connect()
        self.instance_model: InstanceModel = InstanceModel()

    def construct_instance_model(self):
        with Session(self.engine) as session:
            session: Session
            try:
                instance_model: DBInstanceModel = session.query(DBInstanceModel).filter(DBInstanceModel.id == self.uuid).one()
                if instance_model.metadata_value:
                    self.instance_model.metadata = instance_model.metadata_value
                for input_object in (
                    session.query(InstanceModelInputAndOutput, ValueStorage)
                    .filter(
                        InstanceModelInputAndOutput.instance_model_id == self.uuid,
                        InstanceModelInputAndOutput.type == InputAndOutput.input,
                    )
                    .filter(
                        ValueStorage.id == InstanceModelInputAndOutput.value_storage_id
                    )
                    .all()
                ):
                    # print(input_object[0], input_object[1], type(input_object[0]), type(input_object[1]))
                    input_and_output: InstanceModelInputAndOutput = input_object[0]
                    value: ValueStorage = input_object[1]
                    self.instance_model.inputs[input_and_output.name] = value.value
                for node_object in (
                    session.query(DBNodeTemplate)
                    .filter(DBNodeTemplate.instance_model_id == self.uuid)
                    .all()
                ):
                    node = Node()
                    node_object: DBNodeTemplate
                    for attribute_property_object in (
                        session.query(DBNodeAttributeAndProperty, ValueStorage)
                        .filter(DBNodeAttributeAndProperty.node_id == node_object.id)
                        .filter(
                            ValueStorage.id
                            == DBNodeAttributeAndProperty.value_storage_id
                        )
                    ):
                        attribute_property: DBNodeAttributeAndProperty = (
                            attribute_property_object[0]
                        )
                        value: ValueStorage = attribute_property_object[1]
                        if attribute_property.type == AttributeAndProperty.attribute:
                            node.attributes[attribute_property.name] = value.value
                        elif attribute_property.type == AttributeAndProperty.property:
                            node.properties[attribute_property.name] = value.value
                    for capability_object in (
                        session.query(DBCapability)
                        .filter(DBCapability.node_id == node_object.id)
                        .all()
                    ):
                        capability_object: DBCapability
                        capability = Capability()
                        for attribute_property_object in (
                            session.query(
                                DBCapabilityAttributeAndProperty, ValueStorage
                            )
                            .filter(
                                DBCapabilityAttributeAndProperty.capability_id
                                == capability_object.id
                            )
                            .filter(
                                DBCapabilityAttributeAndProperty.value_storage_id
                                == ValueStorage.id
                            )
                            .all()
                        ):
                            attribute_property: DBCapabilityAttributeAndProperty = (
                                attribute_property_object[0]
                            )
                            value: ValueStorage = attribute_property_object[1]
                            if (
                                attribute_property.type
                                == AttributeAndProperty.attribute
                            ):
                                capability.attributes[
                                    attribute_property.name
                                ] = value.value
                            elif (
                                attribute_property.type == AttributeAndProperty.property
                            ):
                                capability.properties[
                                    attribute_property.name
                                ] = value.value
                        capability.type = capability_object.type
                        node.capabilities[capability_object.name] = capability
                    for interface_object in (
                        session.query(DBNodeInterface)
                        .filter(DBNodeInterface.node_id == node_object.id)
                        .all()
                    ):
                        interface_object: DBNodeInterface
                        interface = Interface()
                        for operation_object in (
                            session.query(DBNodeInterfaceOperation)
                            .filter(
                                DBNodeInterfaceOperation.node_interface_id
                                == interface_object.id
                            )
                            .all()
                        ):
                            operation_object: DBNodeInterfaceOperation
                            operation = Operation()
                            for input_output_object in (
                                session.query(
                                    DBNodeInterfaceOperationInputOutput, ValueStorage
                                )
                                .filter(
                                    DBNodeInterfaceOperationInputOutput.operation_id
                                    == operation_object.id
                                )
                                .filter(
                                    ValueStorage.id
                                    == DBNodeInterfaceOperationInputOutput.value_storage_id
                                )
                                .all()
                            ):
                                input_output_header: DBNodeInterfaceOperationInputOutput = input_output_object[
                                    0
                                ]
                                value: ValueStorage = input_output_object[1]
                                if input_output_header.type == InputAndOutput.input:
                                    operation.inputs[
                                        input_output_header.name
                                    ] = value.value
                                elif input_output_header.type == InputAndOutput.output:
                                    operation.outputs[
                                        input_output_header.name
                                    ] = value.value
                            if operation_object.implementation:
                                implementation = ImplementationDefinition(primary=operation_object.implementation.get('primary'))
                                implementation.operation_host = operation_object.implementation.get('operation_host')
                                implementation.dependencies = operation_object.implementation.get('dependencies')
                                operation.implementation = implementation
                            else:
                                operation.implementation = None
                            interface.operations[operation_object.name] = operation
                            interface.type = interface_object.type_name
                        node.interfaces[interface_object.name] = interface
                    for requirement_object in (
                        session.query(DBRequirement)
                        .filter(DBRequirement.node_id == node_object.id).order_by(DBRequirement.order)
                        .all()
                    ):
                        requirement_object: DBRequirement
                        requirement = Requirement()
                        relationship = Relationship()
                        requirement.node = requirement_object.node
                        requirement.capability = requirement_object.capability
                        for attribute_property_object in (
                            session.query(
                                DBRelationshipsAttributeAndProperty, ValueStorage
                            )
                            .filter(
                                DBRelationshipsAttributeAndProperty.requirement_id
                                == requirement_object.id
                            )
                            .filter(
                                ValueStorage.id
                                == DBRelationshipsAttributeAndProperty.value_storage_id
                            )
                            .all()
                        ):
                            attribute_property: DBRelationshipsAttributeAndProperty = (
                                attribute_property_object[0]
                            )
                            value: ValueStorage = attribute_property_object[1]
                            if (
                                attribute_property.type
                                == AttributeAndProperty.attribute
                            ):
                                relationship.attributes[
                                    attribute_property.name
                                ] = value.value
                            elif (
                                attribute_property.type == AttributeAndProperty.property
                            ):
                                relationship.properties[
                                    attribute_property.name
                                ] = value.value
                        for interface_object in session.query(
                            DBRelationshipInterface
                        ).filter(
                            DBRelationshipInterface.requirement_id
                            == requirement_object.id
                        ):
                            interface_object: DBRelationshipInterface
                            interface = Interface()
                            for operation_object in (
                                session.query(DBRelationshipInterfaceOperation)
                                .filter(
                                    DBRelationshipInterfaceOperation.relationship_interface_id
                                    == interface_object.id
                                )
                                .all()
                            ):
                                operation_object: DBRelationshipInterfaceOperation
                                operation = Operation()
                                for input_output_object in (
                                    session.query(
                                        DBRelationshipInterfaceOperationInputOutput,
                                        ValueStorage,
                                    )
                                    .filter(
                                        DBRelationshipInterfaceOperationInputOutput.operation_id
                                        == operation_object.id
                                    )
                                    .filter(
                                        ValueStorage.id
                                        == DBRelationshipInterfaceOperationInputOutput.value_storage_id
                                    )
                                    .all()
                                ):
                                    input_output_header: DBRelationshipInterfaceOperationInputOutput = input_output_object[
                                        0
                                    ]
                                    value: ValueStorage = input_output_object[1]
                                    if input_output_header.type == InputAndOutput.input:
                                        operation.inputs[
                                            input_output_header.name
                                        ] = value.value
                                    elif (
                                        input_output_header.type
                                        == InputAndOutput.output
                                    ):
                                        operation.outputs[
                                            input_output_header.name
                                        ] = value.value
                                operation.implementation = (
                                    operation_object.implementation
                                )
                                interface.type = interface_object.type_name
                                interface.operations[operation_object.name] = operation
                            relationship.interfaces[interface_object.name] = interface
                        relationship.type = requirement_object.relationship_type
                        requirement.relationship = relationship
                        node.requirements.append({requirement_object.name: requirement})
                    if node_object.metadata_value:
                        node.metadata = node_object.metadata_value
                    if node_object.directives:
                        node.directives = node_object.directives
                    node.type = node_object.type_name
                    self.instance_model.nodes[node_object.name] = node
            except Exception:
                session.rollback()
                raise
            else:
                session.commit()

#
# im = InstanceModelGetter("fc912b15-193a-4df3-a8c5-880928b53aa4")
# im.construct_instance_model()
# im
# with open("output.yaml", 'w') as stream:
#     stream.write(yaml.dump(im.instance_model.dict()))
# # with open("../instance_model/output.yaml", 'r') as stream:
# #     data = yaml.safe_load(stream)
# #     topology = puccini_parse(str(data).encode("utf-8"))
# #     topology = TopologyTemplateInstance("None", topology)
# #     with open("input.yaml", "w") as file:
# #         file.write(yaml.dump(topology.render()))
