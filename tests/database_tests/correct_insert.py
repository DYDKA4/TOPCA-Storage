from mariadb_parser.ORM_model.DataBase import Type, TypeOfTypeEnum, DependencyTypeEnum, DependencyTypes
from sqlalchemy.orm import Session

import mariadb_parser.ORM_model.InsertData as InsertData
from mariadb_parser.ORM_model.EngineInit import init_engine
from mariadb_parser.type_table.TypeStorage import TypeStorage, TOSCAType
from tests.database_tests.yaml_data import test_data


# Data Types

class TestInsertData:
    def setup_class(self):
        self.session = Session(init_engine())
        self.parsed_template = TypeStorage(test_data)
        self.loader = InsertData.DataUploader()
        self.type_list = ['data_types',
                          'group_types',
                          'interface_types',
                          'capability_types',
                          'policy_types',
                          'artifact_types',
                          'relationship_types',
                          'node_types']
        self.loader.insert_type_storage(self.parsed_template)

    def teardown_class(self):
        for tosca_type in self.type_list:
            tosca_type_dict = self.parsed_template.__getattribute__(tosca_type)
            for tosca_object in tosca_type_dict.values():
                self.session.query(
                    Type
                ).filter(
                    Type.id == int(tosca_object.identifier)
                ).delete()
        self.session.commit()
        self.session.close()

    def _check_dependency_size(self, tosca_object: TOSCAType, expected_size: int):
        derived_from = self.session.query(DependencyTypes).filter_by(
            source_id=tosca_object.identifier,
            dependency_type=DependencyTypeEnum.dependency
        ).all()
        assert len(derived_from) == expected_size

    def _check_derived_from_size(self, tosca_object: TOSCAType, expected_size: int):
        derived_from = self.session.query(DependencyTypes).filter_by(
            source_id=tosca_object.identifier,
            dependency_type=DependencyTypeEnum.derived_from
        ).all()
        assert len(derived_from) == expected_size

    def _check_requirement_dependency_size(self, tosca_object: TOSCAType, expected_size: int):
        derived_from = self.session.query(DependencyTypes).filter_by(
            source_id=tosca_object.identifier,
            dependency_type=DependencyTypeEnum.requirement_dependency
        ).all()
        assert len(derived_from) == expected_size

    def _check_value_of_tosca_object(self, tosca_object: TOSCAType, expected_type: TypeOfTypeEnum):
        orm_tosca_object = self.session.query(Type).filter_by(id=tosca_object.identifier).first()
        assert orm_tosca_object.version == tosca_object.version
        assert orm_tosca_object.type_of_type == expected_type
        assert orm_tosca_object.data == tosca_object.get_data_in_json()

    def _check_derived_from_value(self, tosca_object: TOSCAType, expected_types: set[str]):
        derived_from = self.session.query(DependencyTypes, Type).filter(
            DependencyTypes.dependency_type == DependencyTypeEnum.derived_from,
            DependencyTypes.source_id == tosca_object.identifier
        ).filter(
            Type.id == DependencyTypes.dependency_id
        ).all()
        for _, tosca_type in derived_from:
            assert tosca_type.type_name in expected_types
            expected_types.remove(tosca_type.type_name)
        assert len(expected_types) == 0

    def _check_dependency_value(self, tosca_object: TOSCAType, expected_types: set[str]):
        dependency = self.session.query(DependencyTypes, Type).filter(
            DependencyTypes.dependency_type == DependencyTypeEnum.dependency,
            DependencyTypes.source_id == tosca_object.identifier
        ).filter(
            Type.id == DependencyTypes.dependency_id
        ).all()
        for _, tosca_type in dependency:
            assert tosca_type.type_name in expected_types
            expected_types.remove(tosca_type.type_name)
        assert len(expected_types) == 0

    def test_tosca_datatypes_root(self):
        tosca_datatypes_root = self.parsed_template.data_types['tosca.datatypes.Root']
        self._check_value_of_tosca_object(tosca_datatypes_root, TypeOfTypeEnum.data_type)

        self._check_dependency_size(tosca_datatypes_root, 0)
        self._check_requirement_dependency_size(tosca_datatypes_root, 0)
        self._check_derived_from_size(tosca_datatypes_root, 0)

    def test_tosca_datatypes_credential(self):
        tosca_datatype_credential = self.parsed_template.data_types['tosca.datatypes.Credential']
        self._check_value_of_tosca_object(tosca_datatype_credential, TypeOfTypeEnum.data_type)

        self._check_dependency_size(tosca_datatype_credential, 0)
        self._check_requirement_dependency_size(tosca_datatype_credential, 0)
        self._check_derived_from_size(tosca_datatype_credential, 1)
        self._check_derived_from_value(tosca_datatype_credential, {'tosca.datatypes.Root'})

    def test_tosca_datatypes_network_info(self):
        tosca_datatypes_network_info = self.parsed_template.data_types['tosca.datatypes.network.NetworkInfo']
        self._check_value_of_tosca_object(tosca_datatypes_network_info, TypeOfTypeEnum.data_type)

        self._check_dependency_size(tosca_datatypes_network_info, 0)
        self._check_requirement_dependency_size(tosca_datatypes_network_info, 0)
        self._check_derived_from_size(tosca_datatypes_network_info, 1)
        self._check_derived_from_value(tosca_datatypes_network_info, {'tosca.datatypes.Root'})

    def test_tosca_datatypes_port_info(self):
        tosca_datatypes_port_info = self.parsed_template.data_types['tosca.datatypes.network.PortInfo']
        self._check_value_of_tosca_object(tosca_datatypes_port_info, TypeOfTypeEnum.data_type)

        self._check_dependency_size(tosca_datatypes_port_info, 0)
        self._check_requirement_dependency_size(tosca_datatypes_port_info, 0)
        self._check_derived_from_size(tosca_datatypes_port_info, 1)
        self._check_derived_from_value(tosca_datatypes_port_info, {'tosca.datatypes.Root'})

    def test_tosca_datatypes_port_def(self):
        tosca_datatypes_port_def = self.parsed_template.data_types['tosca.datatypes.network.PortDef']
        self._check_value_of_tosca_object(tosca_datatypes_port_def, TypeOfTypeEnum.data_type)

        self._check_dependency_size(tosca_datatypes_port_def, 0)
        self._check_requirement_dependency_size(tosca_datatypes_port_def, 0)
        self._check_derived_from_size(tosca_datatypes_port_def, 1)
        self._check_derived_from_value(tosca_datatypes_port_def, {'tosca.datatypes.Root'})

    def test_tosca_datatypes_port_spec(self):
        tosca_datatypes_port_def = self.parsed_template.data_types['tosca.datatypes.network.PortSpec']
        self._check_value_of_tosca_object(tosca_datatypes_port_def, TypeOfTypeEnum.data_type)

        self._check_dependency_size(tosca_datatypes_port_def, 1)
        self._check_dependency_value(tosca_datatypes_port_def, {'tosca.datatypes.network.PortDef'})
        self._check_requirement_dependency_size(tosca_datatypes_port_def, 0)
        self._check_derived_from_size(tosca_datatypes_port_def, 2)
        self._check_derived_from_value(tosca_datatypes_port_def,
                                       {'tosca.datatypes.Root', 'tosca.datatypes.network.PortDef'})

    # Group Types
    def test_tosca_groups_root(self):
        tosca_groups_root = self.parsed_template.group_types['tosca.groups.Root']
        self._check_value_of_tosca_object(tosca_groups_root, TypeOfTypeEnum.group_type)

        self._check_dependency_size(tosca_groups_root, 0)
        # todo actually 1
        # self._check_dependency_value(tosca_groups_root, {'tosca.interfaces.node.lifecycle.Standard'})
        self._check_requirement_dependency_size(tosca_groups_root, 0)
        self._check_derived_from_size(tosca_groups_root, 0)

    # Interface Types

    def test_tosca_interfaces_root(self):
        tosca_interfaces_root = self.parsed_template.interface_types['tosca.interfaces.Root']
        self._check_value_of_tosca_object(tosca_interfaces_root, TypeOfTypeEnum.interface_type)

        self._check_dependency_size(tosca_interfaces_root, 0)
        self._check_requirement_dependency_size(tosca_interfaces_root, 0)
        self._check_derived_from_size(tosca_interfaces_root, 0)

    def test_tosca_interfaces_node_lifecycle_standard(self):
        tosca_interfaces_node_lifecycle_standard = self.parsed_template.interface_types[
            'tosca.interfaces.node.lifecycle.Standard'
        ]
        self._check_value_of_tosca_object(tosca_interfaces_node_lifecycle_standard, TypeOfTypeEnum.interface_type)

        self._check_dependency_size(tosca_interfaces_node_lifecycle_standard, 0)
        self._check_requirement_dependency_size(tosca_interfaces_node_lifecycle_standard, 0)
        self._check_derived_from_size(tosca_interfaces_node_lifecycle_standard, 1)
        self._check_derived_from_value(tosca_interfaces_node_lifecycle_standard,
                                       {'tosca.interfaces.Root'})

    def test_tosca_interfaces_relationship_configure(self):
        tosca_interfaces_node_lifecycle_standard = self.parsed_template.interface_types[
            'tosca.interfaces.relationship.Configure'
        ]
        self._check_value_of_tosca_object(tosca_interfaces_node_lifecycle_standard, TypeOfTypeEnum.interface_type)

        self._check_dependency_size(tosca_interfaces_node_lifecycle_standard, 0)
        self._check_requirement_dependency_size(tosca_interfaces_node_lifecycle_standard, 0)
        self._check_derived_from_size(tosca_interfaces_node_lifecycle_standard, 1)
        self._check_derived_from_value(tosca_interfaces_node_lifecycle_standard,
                                       {'tosca.interfaces.Root'})

    # Capability Type
    def test_tosca_capabilities_root(self):
        tosca_capabilities_root = self.parsed_template.capability_types['tosca.capabilities.Root']
        self._check_value_of_tosca_object(tosca_capabilities_root, TypeOfTypeEnum.capability_type)

        self._check_dependency_size(tosca_capabilities_root, 0)
        self._check_requirement_dependency_size(tosca_capabilities_root, 0)
        self._check_derived_from_size(tosca_capabilities_root, 0)

    def test_tosca_capabilities_node(self):
        tosca_capabilities_node = self.parsed_template.capability_types['tosca.capabilities.Node']
        self._check_value_of_tosca_object(tosca_capabilities_node, TypeOfTypeEnum.capability_type)

        self._check_dependency_size(tosca_capabilities_node, 0)
        self._check_requirement_dependency_size(tosca_capabilities_node, 0)
        self._check_derived_from_size(tosca_capabilities_node, 1)
        self._check_derived_from_value(tosca_capabilities_node,
                                       {'tosca.capabilities.Root'})

    def test_tosca_capabilities_container(self):
        tosca_capabilities_container = self.parsed_template.capability_types['tosca.capabilities.Container']
        self._check_value_of_tosca_object(tosca_capabilities_container, TypeOfTypeEnum.capability_type)

        self._check_dependency_size(tosca_capabilities_container, 0)
        self._check_requirement_dependency_size(tosca_capabilities_container, 0)
        self._check_derived_from_size(tosca_capabilities_container, 1)
        self._check_derived_from_value(tosca_capabilities_container,
                                       {'tosca.capabilities.Root'})

    def test_tosca_capabilities_endpoint(self):
        tosca_capabilities_endpoint = self.parsed_template.capability_types['tosca.capabilities.Endpoint']
        self._check_value_of_tosca_object(tosca_capabilities_endpoint, TypeOfTypeEnum.capability_type)
        self._check_dependency_value(tosca_capabilities_endpoint,
                                     {'tosca.datatypes.network.PortSpec', 'tosca.datatypes.network.PortDef'})
        self._check_dependency_size(tosca_capabilities_endpoint, 2)
        self._check_requirement_dependency_size(tosca_capabilities_endpoint, 0)
        self._check_derived_from_size(tosca_capabilities_endpoint, 1)
        self._check_derived_from_value(tosca_capabilities_endpoint,
                                       {'tosca.capabilities.Root'})

    def test_tosca_capabilities_endpoint_admin(self):
        tosca_capabilities_endpoint_admin = self.parsed_template.capability_types['tosca.capabilities.Endpoint.Admin']
        self._check_value_of_tosca_object(tosca_capabilities_endpoint_admin, TypeOfTypeEnum.capability_type)
        self._check_dependency_value(tosca_capabilities_endpoint_admin,
                                     {'tosca.datatypes.network.PortSpec', 'tosca.datatypes.network.PortDef'})
        self._check_dependency_size(tosca_capabilities_endpoint_admin, 2)
        self._check_requirement_dependency_size(tosca_capabilities_endpoint_admin, 0)
        self._check_derived_from_size(tosca_capabilities_endpoint_admin, 2)
        self._check_derived_from_value(tosca_capabilities_endpoint_admin,
                                       {'tosca.capabilities.Root', 'tosca.capabilities.Endpoint'})

    def test_tosca_capabilities_endpoint_public(self):
        tosca_capabilities_endpoint_public = self.parsed_template.capability_types['tosca.capabilities.Endpoint.Public']
        self._check_value_of_tosca_object(tosca_capabilities_endpoint_public, TypeOfTypeEnum.capability_type)
        self._check_dependency_value(tosca_capabilities_endpoint_public,
                                     {'tosca.datatypes.network.PortSpec', 'tosca.datatypes.network.PortDef'})
        self._check_dependency_size(tosca_capabilities_endpoint_public, 2)
        self._check_requirement_dependency_size(tosca_capabilities_endpoint_public, 0)
        self._check_derived_from_size(tosca_capabilities_endpoint_public, 2)
        self._check_derived_from_value(tosca_capabilities_endpoint_public,
                                       {'tosca.capabilities.Root', 'tosca.capabilities.Endpoint'})

    def test_tosca_capabilities_endpoint_database(self):
        tosca_capabilities_endpoint_database = self.parsed_template.capability_types[
            'tosca.capabilities.Endpoint.Database'
        ]
        self._check_value_of_tosca_object(tosca_capabilities_endpoint_database, TypeOfTypeEnum.capability_type)
        self._check_dependency_value(tosca_capabilities_endpoint_database,
                                     {'tosca.datatypes.network.PortSpec', 'tosca.datatypes.network.PortDef'})
        self._check_dependency_size(tosca_capabilities_endpoint_database, 2)
        self._check_requirement_dependency_size(tosca_capabilities_endpoint_database, 0)
        self._check_derived_from_size(tosca_capabilities_endpoint_database, 2)
        self._check_derived_from_value(tosca_capabilities_endpoint_database,
                                       {'tosca.capabilities.Root', 'tosca.capabilities.Endpoint'})

    def test_tosca_capabilities_attachment(self):
        tosca_capabilities_attachment = self.parsed_template.capability_types['tosca.capabilities.Attachment']
        self._check_value_of_tosca_object(tosca_capabilities_attachment, TypeOfTypeEnum.capability_type)
        self._check_dependency_size(tosca_capabilities_attachment, 0)
        self._check_requirement_dependency_size(tosca_capabilities_attachment, 0)
        self._check_derived_from_size(tosca_capabilities_attachment, 1)
        self._check_derived_from_value(tosca_capabilities_attachment, {'tosca.capabilities.Root'})

    def test_tosca_capabilities_operating_system(self):
        tosca_capabilities_operating_system = self.parsed_template.capability_types[
            'tosca.capabilities.OperatingSystem'
        ]
        self._check_value_of_tosca_object(tosca_capabilities_operating_system, TypeOfTypeEnum.capability_type)
        self._check_dependency_size(tosca_capabilities_operating_system, 0)
        self._check_requirement_dependency_size(tosca_capabilities_operating_system, 0)
        self._check_derived_from_size(tosca_capabilities_operating_system, 1)
        self._check_derived_from_value(tosca_capabilities_operating_system, {'tosca.capabilities.Root'})

    def test_tosca_capabilities_scalable(self):
        tosca_capabilities_scalable = self.parsed_template.capability_types['tosca.capabilities.Scalable']
        self._check_value_of_tosca_object(tosca_capabilities_scalable, TypeOfTypeEnum.capability_type)
        self._check_dependency_size(tosca_capabilities_scalable, 0)
        self._check_requirement_dependency_size(tosca_capabilities_scalable, 0)
        self._check_derived_from_size(tosca_capabilities_scalable, 1)
        self._check_derived_from_value(tosca_capabilities_scalable, {'tosca.capabilities.Root'})

    def test_tosca_capabilities_network_linkable(self):
        tosca_capabilities_network_linkable = self.parsed_template.capability_types[
            'tosca.capabilities.network.Linkable'
        ]
        self._check_value_of_tosca_object(tosca_capabilities_network_linkable, TypeOfTypeEnum.capability_type)
        self._check_dependency_size(tosca_capabilities_network_linkable, 0)
        self._check_requirement_dependency_size(tosca_capabilities_network_linkable, 0)
        self._check_derived_from_size(tosca_capabilities_network_linkable, 2)
        self._check_derived_from_value(tosca_capabilities_network_linkable,
                                       {'tosca.capabilities.Root', 'tosca.capabilities.Node'})

    def test_tosca_capabilities_network_bindable(self):
        tosca_capabilities_network_bindable = self.parsed_template.capability_types[
            'tosca.capabilities.network.Bindable'
        ]
        self._check_value_of_tosca_object(tosca_capabilities_network_bindable, TypeOfTypeEnum.capability_type)
        self._check_dependency_size(tosca_capabilities_network_bindable, 0)
        self._check_requirement_dependency_size(tosca_capabilities_network_bindable, 0)
        self._check_derived_from_size(tosca_capabilities_network_bindable, 2)
        self._check_derived_from_value(tosca_capabilities_network_bindable,
                                       {'tosca.capabilities.Root', 'tosca.capabilities.Node'})

    # Policy Type

    def test_tosca_policies_root(self):
        tosca_policies_root = self.parsed_template.policy_types['tosca.policies.Root']
        self._check_value_of_tosca_object(tosca_policies_root, TypeOfTypeEnum.policy_type)
        self._check_dependency_size(tosca_policies_root, 0)
        self._check_requirement_dependency_size(tosca_policies_root, 0)
        self._check_derived_from_size(tosca_policies_root, 0)

    def test_tosca_policies_placement(self):
        tosca_policies_placement = self.parsed_template.policy_types['tosca.policies.Placement']
        self._check_value_of_tosca_object(tosca_policies_placement, TypeOfTypeEnum.policy_type)
        self._check_dependency_size(tosca_policies_placement, 0)
        self._check_requirement_dependency_size(tosca_policies_placement, 0)
        self._check_derived_from_size(tosca_policies_placement, 1)
        self._check_derived_from_value(tosca_policies_placement, {'tosca.policies.Root'})

    def test_tosca_policies_scaling(self):
        tosca_policies_placement = self.parsed_template.policy_types['tosca.policies.Scaling']
        self._check_value_of_tosca_object(tosca_policies_placement, TypeOfTypeEnum.policy_type)
        self._check_dependency_size(tosca_policies_placement, 0)
        self._check_requirement_dependency_size(tosca_policies_placement, 0)
        self._check_derived_from_size(tosca_policies_placement, 1)
        self._check_derived_from_value(tosca_policies_placement, {'tosca.policies.Root'})

    def test_tosca_policies_update(self):
        tosca_policies_update = self.parsed_template.policy_types['tosca.policies.Update']
        self._check_value_of_tosca_object(tosca_policies_update, TypeOfTypeEnum.policy_type)
        self._check_dependency_size(tosca_policies_update, 0)
        self._check_requirement_dependency_size(tosca_policies_update, 0)
        self._check_derived_from_size(tosca_policies_update, 1)
        self._check_derived_from_value(tosca_policies_update, {'tosca.policies.Root'})

    def test_tosca_policies_performance(self):
        tosca_policies_performance = self.parsed_template.policy_types['tosca.policies.Performance']
        self._check_value_of_tosca_object(tosca_policies_performance, TypeOfTypeEnum.policy_type)
        self._check_dependency_size(tosca_policies_performance, 0)
        self._check_requirement_dependency_size(tosca_policies_performance, 0)
        self._check_derived_from_size(tosca_policies_performance, 1)
        self._check_derived_from_value(tosca_policies_performance, {'tosca.policies.Root'})

    # Artifact Type
    def test_tosca_artifacts_root(self):
        tosca_artifacts_root = self.parsed_template.artifact_types['tosca.artifacts.Root']
        self._check_value_of_tosca_object(tosca_artifacts_root, TypeOfTypeEnum.artifact_type)
        self._check_dependency_size(tosca_artifacts_root, 0)
        self._check_requirement_dependency_size(tosca_artifacts_root, 0)
        self._check_derived_from_size(tosca_artifacts_root, 0)

    def test_tosca_artifacts_file(self):
        tosca_artifacts_file = self.parsed_template.artifact_types['tosca.artifacts.File']
        self._check_value_of_tosca_object(tosca_artifacts_file, TypeOfTypeEnum.artifact_type)
        self._check_dependency_size(tosca_artifacts_file, 0)
        self._check_requirement_dependency_size(tosca_artifacts_file, 0)
        self._check_derived_from_size(tosca_artifacts_file, 1)
        self._check_derived_from_value(tosca_artifacts_file, {'tosca.artifacts.Root'})

    def test_tosca_artifacts_deployment(self):
        tosca_artifacts_deployment = self.parsed_template.artifact_types['tosca.artifacts.Deployment']
        self._check_value_of_tosca_object(tosca_artifacts_deployment, TypeOfTypeEnum.artifact_type)
        self._check_dependency_size(tosca_artifacts_deployment, 0)
        self._check_requirement_dependency_size(tosca_artifacts_deployment, 0)
        self._check_derived_from_size(tosca_artifacts_deployment, 1)
        self._check_derived_from_value(tosca_artifacts_deployment, {'tosca.artifacts.Root'})

    def test_tosca_artifacts_deployment_image(self):
        tosca_artifacts_deployment_image = self.parsed_template.artifact_types['tosca.artifacts.Deployment.Image']
        self._check_value_of_tosca_object(tosca_artifacts_deployment_image, TypeOfTypeEnum.artifact_type)
        self._check_dependency_size(tosca_artifacts_deployment_image, 0)
        self._check_requirement_dependency_size(tosca_artifacts_deployment_image, 0)
        self._check_derived_from_size(tosca_artifacts_deployment_image, 2)
        self._check_derived_from_value(tosca_artifacts_deployment_image,
                                       {'tosca.artifacts.Root', 'tosca.artifacts.Deployment'})

    def test_tosca_artifacts_deployment_image_vm(self):
        tosca_artifacts_deployment_image_vm = self.parsed_template.artifact_types['tosca.artifacts.Deployment.Image.VM']
        self._check_value_of_tosca_object(tosca_artifacts_deployment_image_vm, TypeOfTypeEnum.artifact_type)
        self._check_dependency_size(tosca_artifacts_deployment_image_vm, 0)
        self._check_requirement_dependency_size(tosca_artifacts_deployment_image_vm, 0)
        self._check_derived_from_size(tosca_artifacts_deployment_image_vm, 3)
        self._check_derived_from_value(tosca_artifacts_deployment_image_vm,
                                       {'tosca.artifacts.Root',
                                        'tosca.artifacts.Deployment',
                                        'tosca.artifacts.Deployment.Image'
                                        })

    def test_tosca_artifacts_implementation(self):
        tosca_artifacts_implementation = self.parsed_template.artifact_types['tosca.artifacts.Implementation']
        self._check_value_of_tosca_object(tosca_artifacts_implementation, TypeOfTypeEnum.artifact_type)
        self._check_dependency_size(tosca_artifacts_implementation, 0)
        self._check_requirement_dependency_size(tosca_artifacts_implementation, 0)
        self._check_derived_from_size(tosca_artifacts_implementation, 1)
        self._check_derived_from_value(tosca_artifacts_implementation, {'tosca.artifacts.Root'})

    def test_tosca_artifacts_implementation_bash(self):
        tosca_artifacts_implementation_bash = self.parsed_template.artifact_types[
            'tosca.artifacts.Implementation.Bash']
        self._check_value_of_tosca_object(tosca_artifacts_implementation_bash, TypeOfTypeEnum.artifact_type)
        self._check_dependency_size(tosca_artifacts_implementation_bash, 0)
        self._check_requirement_dependency_size(tosca_artifacts_implementation_bash, 0)
        self._check_derived_from_size(tosca_artifacts_implementation_bash, 2)
        self._check_derived_from_value(tosca_artifacts_implementation_bash,
                                       {'tosca.artifacts.Root', 'tosca.artifacts.Implementation'})

    # Relationship Types
    def test_tosca_artifacts_implementation_bash(self):
        tosca_artifacts_implementation_bash = self.parsed_template.artifact_types[
            'tosca.artifacts.Implementation.Bash']
        self._check_value_of_tosca_object(tosca_artifacts_implementation_bash, TypeOfTypeEnum.artifact_type)
        self._check_dependency_size(tosca_artifacts_implementation_bash, 0)
        self._check_requirement_dependency_size(tosca_artifacts_implementation_bash, 0)
        self._check_derived_from_size(tosca_artifacts_implementation_bash, 2)
        self._check_derived_from_value(tosca_artifacts_implementation_bash,
                                       {'tosca.artifacts.Root', 'tosca.artifacts.Implementation'})
# Type(id=30,
#      version='1.0',
#      type_of_type='relationship_type',
#      type_name='tosca.relationships.Root',
#      data="{\"description\": \"The TOSCA root Relationship Type all other TOSCA base Relationship Types derive "
#           "from.\\n\", \"attributes\": {\"tosca_id\": {\"type\": \"string\"}, \"state\": {\"type\": \"string\"}}, "
#           "\"properties\": {\"tosca_name\": {\"type\": \"string\", \"required\": true}}, \"interfaces\": {"
#           "\"Configure\": {\"type\": \"tosca.interfaces.relationship.Configure\"}}}")
#
# DependencyTypes(source_id=30,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# Type(id=31,
#      version='1.0',
#      type_of_type='relationship_type',
#      type_name='tosca.relationships.DependsOn',
#      data="{\"description\": \"This type represents a general dependency relationship between two nodes.\", "
#           "\"derived_from\": \"tosca.relationships.Root\", \"valid_target_types\": [\"tosca.capabilities.Node\"]}")
#
# DependencyTypes(source_id=31,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=31,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=31,
#                 dependency_id=30,
#                 dependency_type='derived_from')
#
# Type(id=32,
#      version='1.0',
#      type_of_type='relationship_type',
#      type_name='tosca.relationships.HostedOn',
#      data="{\"description\": \"This type represents a hosting relationship between two nodes.\", \"derived_from\": "
#           "\"tosca.relationships.Root\", \"valid_target_types\": [\"tosca.capabilities.Container\"]}")
#
# DependencyTypes(source_id=32,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=32,
#                 dependency_id=9,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=32,
#                 dependency_id=30,
#                 dependency_type='derived_from')
#
# Type(id=33,
#      version='1.0',
#      type_of_type='relationship_type',
#      type_name='tosca.relationships.ConnectsTo',
#      data="{\"description\": \"This type represents a network connection relationship between two nodes.\", "
#           "\"derived_from\": \"tosca.relationships.Root\", \"valid_target_types\": [\"tosca.capabilities.Endpoint\"], "
#           "\"properties\": {\"credential\": {\"type\": \"tosca.datatypes.Credential\", \"required\": false}}}")
#
# DependencyTypes(source_id=33,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=33,
#                 dependency_id=30,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=33,
#                 dependency_id=2,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=33,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=33,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=33,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# Type(id=34,
#      version='1.0',
#      type_of_type='relationship_type',
#      type_name='tosca.relationships.AttachesTo',
#      data="{\"description\": \"This type represents an attachment relationship between two nodes. For example, "
#           "an AttachesTo relationship type would be used for attaching a storage node to a Compute node.\\n\", "
#           "\"derived_from\": \"tosca.relationships.Root\", \"valid_target_types\": ["
#           "\"tosca.capabilities.Attachment\"], \"properties\": {\"location\": {\"required\": true, \"type\": "
#           "\"string\", \"constraints\": [{\"min_length\": 1}]}, \"device\": {\"required\": false, \"type\": "
#           "\"string\"}}}")
#
# DependencyTypes(source_id=34,
#                 dependency_id=30,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=34,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=34,
#                 dependency_id=14,
#                 dependency_type='dependency')
#
# Type(id=35,
#      version='1.0',
#      type_of_type='relationship_type',
#      type_name='tosca.relationships.RoutesTo',
#      data="{\"description\": \"This type represents an intentional network routing between two Endpoints in different "
#           "networks.\", \"derived_from\": \"tosca.relationships.ConnectsTo\", \"valid_target_types\": ["
#           "\"tosca.capabilities.Endpoint\"]}")
#
# DependencyTypes(source_id=35,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=35,
#                 dependency_id=33,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=35,
#                 dependency_id=30,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=35,
#                 dependency_id=2,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=35,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=35,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=33,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# Type(id=36,
#      version='1.0',
#      type_of_type='relationship_type',
#      type_name='tosca.relationships.network.LinksTo',
#      data="{\"description\": \"This relationship type represents an association relationship between Port and Network "
#           "node types.\", \"derived_from\": \"tosca.relationships.DependsOn\", \"valid_target_types\": ["
#           "\"tosca.capabilities.network.Linkable\"]}")
#
# DependencyTypes(source_id=36,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=36,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=36,
#                 dependency_id=30,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=36,
#                 dependency_id=31,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=36,
#                 dependency_id=17,
#                 dependency_type='dependency')
#
# Type(id=37,
#      version='1.0',
#      type_of_type='relationship_type',
#      type_name='tosca.relationships.network.BindsTo',
#      data="{\"description\": \"This type represents a network association relationship between Port and Compute node "
#           "types.\", \"derived_from\": \"tosca.relationships.DependsOn\", \"valid_target_types\": ["
#           "\"tosca.capabilities.network.Bindable\"]}")
#
# DependencyTypes(source_id=37,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=37,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=37,
#                 dependency_id=30,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=37,
#                 dependency_id=31,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=37,
#                 dependency_id=18,
#                 dependency_type='dependency')
#
# # Node Type
#
# Type(id=38,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.Root',
#      data="{\"description\": \"The TOSCA root node all other TOSCA base node types derive from.\\n\", \"properties\": "
#           "{\"tosca_id\": {\"description\": \"A unique identifier of the realized instance of a Node Template that "
#           "derives from any TOSCA normative type.\\n\", \"type\": \"string\", \"required\": false}, \"tosca_name\": {"
#           "\"description\": \"This attribute reflects the name of the Node Template as defined in the TOSCA service "
#           "template.\\n\", \"type\": \"string\", \"required\": false}, \"state\": {\"description\": \"The state of "
#           "the node instance. See section \\u201cNode States\\u201d for allowed values.\\n\", \"type\": \"string\", "
#           "\"required\": false}}, \"capabilities\": {\"feature\": {\"type\": \"tosca.capabilities.Node\"}}, "
#           "\"requirements\": [{\"dependency\": {\"capability\": \"tosca.capabilities.Node\", \"node\": "
#           "\"tosca.nodes.Root\", \"relationship\": \"tosca.relationships.DependsOn\", \"occurrences\": [0, "
#           "\"UNBOUNDED\"]}}], \"interfaces\": {\"Standard\": {\"type\": "
#           "\"tosca.interfaces.node.lifecycle.Standard\"}}}")
#
# DependencyTypes(source_id=38,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=38,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
#
# DependencyTypes(source_id=38,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=38,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=38,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=38,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=38,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=38,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=38,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
#
# Type(id=39,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.Compute',
#      data="{\"description\": \"The TOSCA Compute node represents one or more real or virtual processors of software "
#           "applications or services along with other essential local resources.\\n\", \"derived_from\": "
#           "\"tosca.nodes.Root\", \"properties\": {\"meta\": {\"type\": \"string\", \"required\": false}, "
#           "\"private_address\": {\"type\": \"string\", \"required\": false}, \"public_address\": {\"type\": "
#           "\"string\", \"required\": false}, \"networks\": {\"type\": \"map\", \"entry_schema\": {\"type\": "
#           "\"tosca.datatypes.network.NetworkInfo\"}, \"required\": false}, \"ports\": {\"type\": \"map\", "
#           "\"entry_schema\": {\"type\": \"tosca.datatypes.network.PortInfo\"}, \"required\": false}}, "
#           "\"capabilities\": {\"host\": {\"type\": \"tosca.capabilities.Container\", \"valid_source_types\": ["
#           "\"tosca.nodes.SoftwareComponent\"]}, \"endpoint\": {\"type\": \"tosca.capabilities.Endpoint.Admin\"}, "
#           "\"os\": {\"type\": \"tosca.capabilities.OperatingSystem\"}, \"scalable\": {\"type\": "
#           "\"tosca.capabilities.Scalable\"}, \"binding\": {\"type\": \"tosca.capabilities.network.Bindable\"}}, "
#           "\"requirements\": [{\"local_storage\": {\"capability\": \"tosca.capabilities.Attachment\", "
#           "\"node\": \"tosca.nodes.BlockStorage\", \"relationship\": \"tosca.relationships.AttachesTo\", "
#           "\"occurrences\": [0, \"UNBOUNDED\"]}}]}")
#
# DependencyTypes(source_id=39,
#                 dependency_id=1,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=2,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=3,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=4,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=9,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=11,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=14,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=15,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=16,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=18,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=31,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=32,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=34,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=38,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=39,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=40,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=46,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=14,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=34,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=46,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=39,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
#
# Type(id=40,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.SoftwareComponent',
#      data="{\"description\": \"The TOSCA SoftwareComponent node represents a generic software component that can be "
#           "managed and run by a TOSCA Compute Node Type.\\n\", \"derived_from\": \"tosca.nodes.Root\", "
#           "\"properties\": {\"component_version\": {\"type\": \"version\", \"required\": false, \"description\": "
#           "\"Software component version.\\n\"}, \"admin_credential\": {\"type\": \"tosca.datatypes.Credential\", "
#           "\"required\": false}}, \"requirements\": [{\"host\": {\"capability\": \"tosca.capabilities.Container\", "
#           "\"node\": \"tosca.nodes.Compute\", \"relationship\": \"tosca.relationships.HostedOn\"}}]}")
#
# DependencyTypes(source_id=40,
#                 dependency_id=1,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=2,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=3,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=4,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=9,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=11,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=14,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=15,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=16,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=18,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=31,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=32,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=34,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=38,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=39,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=40,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=46,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=9,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=32,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=40,
#                 dependency_id=39,
#                 dependency_type='requirement_dependency')
#
#
# DependencyTypes(source_id=40,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
# Type(id=41,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.WebServer',
#      data="{\"description\": \"This TOSCA WebServer Node Type represents an abstract software component or service "
#           "that is capable of hosting and providing management operations for one or more WebApplication nodes\\n\", "
#           "\"derived_from\": \"tosca.nodes.SoftwareComponent\", \"capabilities\": {\"data_endpoint\": {\"type\": "
#           "\"tosca.capabilities.Endpoint\"}, \"admin_endpoint\": {\"type\": \"tosca.capabilities.Endpoint.Admin\"}, "
#           "\"host\": {\"type\": \"tosca.capabilities.Container\", \"valid_source_types\": ["
#           "\"tosca.nodes.WebApplication\"]}}}")
#
# DependencyTypes(source_id=41,
#                 dependency_id=1,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=2,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=3,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=4,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=9,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=11,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=14,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=15,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=16,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=18,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=31,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=32,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=34,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=38,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=39,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=40,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=46,
#                 dependency_type='dependency')
#
#
# DependencyTypes(source_id=41,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=9,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=32,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=41,
#                 dependency_id=39,
#                 dependency_type='requirement_dependency')
#
#
# DependencyTypes(source_id=41,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=41,
#                 dependency_id=40,
#                 dependency_type='derived_from')
#
# Type(id=42,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.WebApplication',
#      data="{\"description\": \"The TOSCA WebApplication node represents a software application that can be managed "
#           "and run by a TOSCA WebServer node.\\n\", \"derived_from\": \"tosca.nodes.SoftwareComponent\", "
#           "\"properties\": {\"context_root\": {\"type\": \"string\", \"required\": false}}, \"requirements\": [{"
#           "\"host\": {\"capability\": \"tosca.capabilities.Container\", \"node\": \"tosca.nodes.WebServer\", "
#           "\"relationship\": \"tosca.relationships.HostedOn\"}}], \"capabilities\": {\"app_endpoint\": {\"type\": "
#           "\"tosca.capabilities.Endpoint\"}}}")
#
# DependencyTypes(source_id=42,
#                 dependency_id=1,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=2,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=3,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=4,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=9,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=11,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=14,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=15,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=16,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=18,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=31,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=32,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=34,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=38,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=39,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=40,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=46,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=9,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=32,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=39,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=41,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=42,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=42,
#                 dependency_id=40,
#                 dependency_type='derived_from')
#
# Type(id=43,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.DBMS',
#      data="{\"description\": \"The TOSCA DBMS node represents a typical relational, SQL Database Management System "
#           "software component or service.\\n\", \"derived_from\": \"tosca.nodes.SoftwareComponent\", \"properties\": "
#           "{\"port\": {\"required\": false, \"type\": \"integer\", \"description\": \"The port the DBMS service will "
#           "listen to for data and requests.\\n\"}, \"root_password\": {\"required\": false, \"type\": \"string\", "
#           "\"description\": \"The root password for the DBMS service.\\n\"}}, \"capabilities\": {\"host\": {\"type\": "
#           "\"tosca.capabilities.Container\", \"valid_source_types\": [\"tosca.nodes.Database\"]}}}")
#
# DependencyTypes(source_id=43,
#                 dependency_id=1,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=2,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=3,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=4,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=9,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=11,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=13,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=14,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=15,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=16,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=18,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=31,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=32,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=34,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=38,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=39,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=40,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=43,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=44,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=46,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=9,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=32,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=39,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=43,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=43,
#                 dependency_id=40,
#                 dependency_type='derived_from')
#
# Type(id=44,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.Root',
#      data="{\"description\": \"The TOSCA root node all other TOSCA base node types derive from.\\n\", \"properties\": "
#           "{\"tosca_id\": {\"description\": \"A unique identifier of the realized instance of a Node Template that "
#           "derives from any TOSCA normative type.\\n\", \"type\": \"string\", \"required\": false}, \"tosca_name\": {"
#           "\"description\": \"This attribute reflects the name of the Node Template as defined in the TOSCA service "
#           "template.\\n\", \"type\": \"string\", \"required\": false}, \"state\": {\"description\": \"The state of "
#           "the node instance. See section \\u201cNode States\\u201d for allowed values.\\n\", \"type\": \"string\", "
#           "\"required\": false}}, \"capabilities\": {\"feature\": {\"type\": \"tosca.capabilities.Node\"}}, "
#           "\"requirements\": [{\"dependency\": {\"capability\": \"tosca.capabilities.Node\", \"node\": "
#           "\"tosca.nodes.Root\", \"relationship\": \"tosca.relationships.DependsOn\", \"occurrences\": [0, "
#           "\"UNBOUNDED\"]}}], \"interfaces\": {\"Standard\": {\"type\": "
#           "\"tosca.interfaces.node.lifecycle.Standard\"}}}")
#
# DependencyTypes(source_id=44,
#                 dependency_id=1,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=2,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=3,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=4,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=9,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=11,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=14,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=15,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=16,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=18,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=31,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=32,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=34,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=38,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=39,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=40,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=44,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=46,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=9,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=13,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=32,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=43,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=44,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
# Type(id=45,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.ObjectStorage',
#      data="{\"description\": \"The TOSCA ObjectStorage node represents storage that provides the ability to store "
#           "data as objects (or BLOBs of data) without consideration for the underlying filesystem or devices\\n\", "
#           "\"derived_from\": \"tosca.nodes.Root\", \"properties\": {\"name\": {\"type\": \"string\", \"required\": "
#           "true, \"description\": \"The logical name of the object store (or container).\\n\"}, \"size\": {\"type\": "
#           "\"scalar-unit.size\", \"required\": false, \"constraints\": [{\"greater_or_equal\": \"0 GB\"}], "
#           "\"description\": \"The requested initial storage size.\\n\"}, \"maxsize\": {\"type\": "
#           "\"scalar-unit.size\", \"required\": false, \"constraints\": [{\"greater_or_equal\": \"0 GB\"}], "
#           "\"description\": \"The requested maximum storage size.\\n\"}}, \"capabilities\": {\"storage_endpoint\": {"
#           "\"type\": \"tosca.capabilities.Endpoint\"}}}")
#
#
# DependencyTypes(source_id=45,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=45,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
# Type(id=46,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.BlockStorage',
#      data="{\"description\": \"The TOSCA BlockStorage node currently represents a server-local block storage device ("
#           "i.e., not shared) offering evenly sized blocks of data from which raw storage volumes can be "
#           "created.\\n\", \"derived_from\": \"tosca.nodes.Root\", \"properties\": {\"size\": {\"type\": "
#           "\"scalar-unit.size\", \"constraints\": [{\"greater_or_equal\": \"1 MB\"}]}, \"volume_id\": {\"type\": "
#           "\"string\", \"required\": false}, \"snapshot_id\": {\"type\": \"string\", \"required\": false}}, "
#           "\"capabilities\": {\"attachment\": {\"type\": \"tosca.capabilities.Attachment\"}}}")
#
# DependencyTypes(source_id=46,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=46,
#                 dependency_id=14,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=46,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
#
# DependencyTypes(source_id=46,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=46,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=46,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=46,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=46,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=46,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=46,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=46,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
# Type(id=47,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.Container.Runtime',
#      data="{\"description\": \"The TOSCA Container Runtime node represents operating system-level virtualization "
#           "technology used to run multiple application services on a single Compute host.\\n\", \"derived_from\": "
#           "\"tosca.nodes.SoftwareComponent\", \"capabilities\": {\"host\": {\"type\": "
#           "\"tosca.capabilities.Container\"}, \"scalable\": {\"type\": \"tosca.capabilities.Scalable\"}}}")
#
# DependencyTypes(source_id=47,
#                 dependency_id=1,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=2,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=3,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=4,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=9,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=11,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=14,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=15,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=16,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=18,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=31,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=32,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=34,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=38,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=39,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=47,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=46,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=9,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=32,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=39,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=47,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=47,
#                 dependency_id=40,
#                 dependency_type='derived_from')
#
#
# Type(id=48,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.Container.Application',
#      data="{\"description\": \"The TOSCA Container Application node represents an application that requires "
#           "Container-level virtualization technology.\\n\", \"derived_from\": \"tosca.nodes.Root\", \"requirements\": "
#           "[{\"host\": {\"capability\": \"tosca.capabilities.Container\", \"node\": "
#           "\"tosca.nodes.Container.Runtime\", \"relationship\": \"tosca.relationships.HostedOn\"}}]}")
#
# DependencyTypes(source_id=48,
#                 dependency_id=1,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=2,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=3,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=4,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=9,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=11,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=14,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=15,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=16,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=18,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=31,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=32,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=34,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=38,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=39,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=40,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=47,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=46,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=9,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=32,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=47,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=48,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
# Type(id=49,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.LoadBalancer',
#      data="{\"description\": \"The TOSCA root node all other TOSCA base node types derive from.\\n\", \"properties\": "
#           "{\"tosca_id\": {\"description\": \"A unique identifier of the realized instance of a Node Template that "
#           "derives from any TOSCA normative type.\\n\", \"type\": \"string\", \"required\": false}, \"tosca_name\": {"
#           "\"description\": \"This attribute reflects the name of the Node Template as defined in the TOSCA service "
#           "template.\\n\", \"type\": \"string\", \"required\": false}, \"state\": {\"description\": \"The state of "
#           "the node instance. See section \\u201cNode States\\u201d for allowed values.\\n\", \"type\": \"string\", "
#           "\"required\": false}}, \"capabilities\": {\"feature\": {\"type\": \"tosca.capabilities.Node\"}}, "
#           "\"requirements\": [{\"dependency\": {\"capability\": \"tosca.capabilities.Node\", \"node\": "
#           "\"tosca.nodes.Root\", \"relationship\": \"tosca.relationships.DependsOn\", \"occurrences\": [0, "
#           "\"UNBOUNDED\"]}}], \"interfaces\": {\"Standard\": {\"type\": "
#           "\"tosca.interfaces.node.lifecycle.Standard\"}}}")
#
# DependencyTypes(source_id=49,
#                 dependency_id=2,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=10,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=12,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=33,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=10,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=35,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=49,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
# Type(id=50,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.network.Network',
#      data="{\"derived_from\": \"tosca.nodes.Root\", \"description\": \"The TOSCA Network node represents a simple, "
#           "logical network service.\\n\", \"properties\": {\"ip_version\": {\"type\": \"integer\", \"required\": "
#           "false, \"default\": 4, \"constraints\": [{\"valid_values\": [4, 6]}], \"description\": \"The IP version of "
#           "the requested network. Valid values are 4 for ipv4 or 6 for ipv6.\\n\"}, \"cidr\": {\"type\": \"string\", "
#           "\"required\": false, \"description\": \"The cidr block of the requested network.\\n\"}, \"start_ip\": {"
#           "\"type\": \"string\", \"required\": false, \"description\": \"The IP address to be used as the start of a "
#           "pool of addresses within the full IP range derived from the cidr block.\\n\"}, \"end_ip\": {\"type\": "
#           "\"string\", \"required\": false, \"description\": \"The IP address to be used as the end of a pool of "
#           "addresses within the full IP range derived from the cidr block.\\n\"}, \"gateway_ip\": {\"type\": "
#           "\"string\", \"required\": false, \"description\": \"The gateway IP address.\\n\"}, \"network_name\": {"
#           "\"type\": \"string\", \"required\": false, \"description\": \"An identifier that represents an existing "
#           "Network instance in the underlying cloud infrastructure or can be used as the name of the newly created "
#           "network. If network_name is provided and no other properties are provided (with exception of network_id), "
#           "then an existing network instance will be used. If network_name is provided alongside with more properties "
#           "then a new network with this name will be created.\\n\"}, \"network_id\": {\"type\": \"string\", "
#           "\"required\": false, \"description\": \"An identifier that represents an existing Network instance in the "
#           "underlying cloud infrastructure. This property is mutually exclusive with all other properties except "
#           "network_name. This can be used alone or together with network_name to identify an existing network.\\n\"}, "
#           "\"segmentation_id\": {\"type\": \"string\", \"required\": false, \"description\": \"A segmentation "
#           "identifier in the underlying cloud infrastructure. E.g. VLAN ID, GRE tunnel ID, etc..\\n\"}, "
#           "\"network_type\": {\"type\": \"string\", \"required\": false, \"description\": \"It specifies the nature "
#           "of the physical network in the underlying cloud infrastructure. Examples are flat, vlan, gre or vxlan. For "
#           "flat and vlan types, physical_network should be provided too.\\n\"}, \"physical_network\": {\"type\": "
#           "\"string\", \"required\": false, \"description\": \"It identifies the physical network on top of which the "
#           "network is implemented, e.g. physnet1. This property is required if network_type is flat or vlan.\\n\"}, "
#           "\"dhcp_enabled\": {\"type\": \"boolean\", \"required\": false, \"default\": true, \"description\": "
#           "\"Indicates should DHCP service be enabled on the network or not.\\n\"}}, \"capabilities\": {\"link\": {"
#           "\"type\": \"tosca.capabilities.network.Linkable\"}}}")
#
# DependencyTypes(source_id=50,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=50,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=50,
#                 dependency_id=17,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=50,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=50,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=50,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=50,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=50,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=50,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=50,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=50,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
# Type(id=51,
#      version='1.0',
#      type_of_type='node_type',
#      type_name='tosca.nodes.network.Port',
#      data="{\"derived_from\": \"tosca.nodes.Root\", \"description\": \"The TOSCA Port node represents a logical "
#           "entity that associates between Compute and Network normative types. The Port node type effectively "
#           "represents a single virtual NIC on the Compute node instance.\\n\", \"properties\": {\"ip_address\": {"
#           "\"type\": \"string\", \"required\": false, \"description\": \"Allow the user to set a static IP.\\n\"}, "
#           "\"order\": {\"type\": \"integer\", \"required\": false, \"default\": 0, \"constraints\": [{"
#           "\"greater_or_equal\": 0}], \"description\": \"The order of the NIC on the compute instance (e.g. "
#           "eth2).\\n\"}, \"is_default\": {\"type\": \"boolean\", \"required\": false, \"default\": false, "
#           "\"description\": \"If is_default=true this port will be used for the default gateway route. Only one port "
#           "that is associated to single compute node can set as is_default=true.\\n\"}, \"ip_range_start\": {"
#           "\"type\": \"string\", \"required\": false, \"description\": \"Defines the starting IP of a range to be "
#           "allocated for the compute instances that are associated with this Port.\\n\"}, \"ip_range_end\": {"
#           "\"type\": \"string\", \"required\": false, \"description\": \"Defines the ending IP of a range to be "
#           "allocated for the compute instances that are associated with this Port.\\n\"}}, \"requirements\": [{"
#           "\"binding\": {\"capability\": \"tosca.capabilities.network.Bindable\", \"relationship\": "
#           "\"tosca.relationships.network.BindsTo\"}}, {\"link\": {\"capability\": "
#           "\"tosca.capabilities.network.Linkable\", \"relationship\": \"tosca.relationships.network.LinksTo\"}}]}")
#
# DependencyTypes(source_id=51,
#                 dependency_id=7,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=8,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=17,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=18,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=27,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=28,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=29,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=30,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=31,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=8,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=17,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=18,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=31,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=36,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=37,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=38,
#                 dependency_type='requirement_dependency')
#
# DependencyTypes(source_id=51,
#                 dependency_id=38,
#                 dependency_type='derived_from')
#
#
#
#
#
#
