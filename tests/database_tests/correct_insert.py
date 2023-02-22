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
        self.loader.insert_type_storage(self.parsed_template, 'python_test')

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

    def _check_requirement_dependency_value(self, tosca_object: TOSCAType, expected_types: set[str]):
        requirement_dependency = self.session.query(DependencyTypes, Type).filter(
            DependencyTypes.dependency_type == DependencyTypeEnum.requirement_dependency,
            DependencyTypes.source_id == tosca_object.identifier
        ).filter(
            Type.id == DependencyTypes.dependency_id
        ).all()
        for _, tosca_type in requirement_dependency:
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
        self._check_dependency_size(tosca_capabilities_endpoint, 3)
        self._check_dependency_value(tosca_capabilities_endpoint,
                                     {'tosca.datatypes.network.PortSpec',
                                      'tosca.datatypes.network.PortDef',
                                      'tosca.datatypes.Root'})
        self._check_requirement_dependency_size(tosca_capabilities_endpoint, 0)
        self._check_derived_from_size(tosca_capabilities_endpoint, 1)
        self._check_derived_from_value(tosca_capabilities_endpoint,
                                       {'tosca.capabilities.Root'})

    def test_tosca_capabilities_endpoint_admin(self):
        tosca_capabilities_endpoint_admin = self.parsed_template.capability_types['tosca.capabilities.Endpoint.Admin']
        self._check_value_of_tosca_object(tosca_capabilities_endpoint_admin, TypeOfTypeEnum.capability_type)
        self._check_dependency_size(tosca_capabilities_endpoint_admin, 3)
        self._check_dependency_value(tosca_capabilities_endpoint_admin,
                                     {'tosca.datatypes.network.PortSpec',
                                      'tosca.datatypes.network.PortDef',
                                      'tosca.datatypes.Root'})
        self._check_requirement_dependency_size(tosca_capabilities_endpoint_admin, 0)
        self._check_derived_from_size(tosca_capabilities_endpoint_admin, 2)
        self._check_derived_from_value(tosca_capabilities_endpoint_admin,
                                       {'tosca.capabilities.Root', 'tosca.capabilities.Endpoint'})

    def test_tosca_capabilities_endpoint_public(self):
        tosca_capabilities_endpoint_public = self.parsed_template.capability_types['tosca.capabilities.Endpoint.Public']
        self._check_value_of_tosca_object(tosca_capabilities_endpoint_public, TypeOfTypeEnum.capability_type)
        self._check_dependency_size(tosca_capabilities_endpoint_public, 3)
        self._check_dependency_value(tosca_capabilities_endpoint_public,
                                     {'tosca.datatypes.network.PortSpec',
                                      'tosca.datatypes.network.PortDef',
                                      'tosca.datatypes.Root'})
        self._check_requirement_dependency_size(tosca_capabilities_endpoint_public, 0)
        self._check_derived_from_size(tosca_capabilities_endpoint_public, 2)
        self._check_derived_from_value(tosca_capabilities_endpoint_public,
                                       {'tosca.capabilities.Root', 'tosca.capabilities.Endpoint'})

    def test_tosca_capabilities_endpoint_database(self):
        tosca_capabilities_endpoint_database = self.parsed_template.capability_types[
            'tosca.capabilities.Endpoint.Database'
        ]
        self._check_value_of_tosca_object(tosca_capabilities_endpoint_database, TypeOfTypeEnum.capability_type)
        self._check_dependency_size(tosca_capabilities_endpoint_database, 3)
        self._check_dependency_value(tosca_capabilities_endpoint_database,
                                     {'tosca.datatypes.network.PortSpec',
                                      'tosca.datatypes.network.PortDef',
                                      'tosca.datatypes.Root'})
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
    def test_tosca_relationships_root(self):
        tosca_relationships_root = self.parsed_template.relationship_types['tosca.relationships.Root']
        self._check_value_of_tosca_object(tosca_relationships_root, TypeOfTypeEnum.relationship_type)
        self._check_dependency_size(tosca_relationships_root, 2)
        self._check_dependency_value(tosca_relationships_root,
                                     {'tosca.interfaces.relationship.Configure', 'tosca.interfaces.Root'})
        self._check_requirement_dependency_size(tosca_relationships_root, 0)
        self._check_derived_from_size(tosca_relationships_root, 0)

    def test_tosca_relationships_depends_on(self):
        tosca_relationships_depends_on = self.parsed_template.relationship_types['tosca.relationships.DependsOn']
        self._check_value_of_tosca_object(tosca_relationships_depends_on, TypeOfTypeEnum.relationship_type)
        self._check_dependency_size(tosca_relationships_depends_on, 4)
        self._check_dependency_value(tosca_relationships_depends_on,
                                     {'tosca.interfaces.relationship.Configure', 'tosca.interfaces.Root',
                                      'tosca.capabilities.Node', 'tosca.capabilities.Root'})
        self._check_requirement_dependency_size(tosca_relationships_depends_on, 0)
        self._check_derived_from_size(tosca_relationships_depends_on, 1)
        self._check_derived_from_value(tosca_relationships_depends_on, {'tosca.relationships.Root'})

    def test_tosca_relationships_connects_to(self):
        tosca_relationships_connects_to = self.parsed_template.relationship_types['tosca.relationships.ConnectsTo']
        self._check_value_of_tosca_object(tosca_relationships_connects_to, TypeOfTypeEnum.relationship_type)
        self._check_dependency_size(tosca_relationships_connects_to, 8)
        self._check_dependency_value(tosca_relationships_connects_to, {
            'tosca.interfaces.relationship.Configure', 'tosca.interfaces.Root', 'tosca.capabilities.Endpoint',
            'tosca.capabilities.Root', 'tosca.datatypes.Credential', 'tosca.datatypes.Root',
            'tosca.datatypes.network.PortSpec', 'tosca.datatypes.network.PortDef'})
        self._check_requirement_dependency_size(tosca_relationships_connects_to, 0)
        self._check_derived_from_size(tosca_relationships_connects_to, 1)
        self._check_derived_from_value(tosca_relationships_connects_to, {'tosca.relationships.Root'})

    def test_tosca_relationships_attaches_to(self):
        tosca_relationships_attaches_to = self.parsed_template.relationship_types['tosca.relationships.AttachesTo']
        self._check_value_of_tosca_object(tosca_relationships_attaches_to, TypeOfTypeEnum.relationship_type)
        self._check_dependency_size(tosca_relationships_attaches_to, 4)
        self._check_dependency_value(tosca_relationships_attaches_to, {
            'tosca.interfaces.relationship.Configure', 'tosca.interfaces.Root',
            'tosca.capabilities.Attachment', 'tosca.capabilities.Root'})
        self._check_requirement_dependency_size(tosca_relationships_attaches_to, 0)
        self._check_derived_from_size(tosca_relationships_attaches_to, 1)
        self._check_derived_from_value(tosca_relationships_attaches_to, {'tosca.relationships.Root'})

    def test_tosca_relationships_routes_to(self):
        tosca_relationships_routes_to = self.parsed_template.relationship_types['tosca.relationships.RoutesTo']
        self._check_value_of_tosca_object(tosca_relationships_routes_to, TypeOfTypeEnum.relationship_type)
        self._check_dependency_size(tosca_relationships_routes_to, 8)
        self._check_dependency_value(tosca_relationships_routes_to, {
            'tosca.interfaces.relationship.Configure', 'tosca.interfaces.Root', 'tosca.capabilities.Endpoint',
            'tosca.capabilities.Root', 'tosca.datatypes.Credential', 'tosca.datatypes.Root',
            'tosca.datatypes.network.PortSpec', 'tosca.datatypes.network.PortDef'})
        self._check_requirement_dependency_size(tosca_relationships_routes_to, 0)
        self._check_derived_from_size(tosca_relationships_routes_to, 2)
        self._check_derived_from_value(tosca_relationships_routes_to, {'tosca.relationships.Root',
                                                                       'tosca.relationships.ConnectsTo'})

    def test_tosca_relationships_network_links_to(self):
        tosca_relationships_network_links_to = self.parsed_template.relationship_types[
            'tosca.relationships.network.LinksTo']
        self._check_value_of_tosca_object(tosca_relationships_network_links_to, TypeOfTypeEnum.relationship_type)
        self._check_dependency_size(tosca_relationships_network_links_to, 5)
        self._check_dependency_value(tosca_relationships_network_links_to, {
            'tosca.interfaces.relationship.Configure', 'tosca.interfaces.Root', 'tosca.capabilities.Node',
            'tosca.capabilities.Root', 'tosca.capabilities.network.Linkable'})
        self._check_requirement_dependency_size(tosca_relationships_network_links_to, 0)
        self._check_derived_from_size(tosca_relationships_network_links_to, 2)
        self._check_derived_from_value(tosca_relationships_network_links_to, {
            'tosca.relationships.Root', 'tosca.relationships.DependsOn'})

    def test_tosca_relationships_network_binds_to(self):
        tosca_relationships_network_binds_to = self.parsed_template.relationship_types[
            'tosca.relationships.network.BindsTo']
        self._check_value_of_tosca_object(tosca_relationships_network_binds_to, TypeOfTypeEnum.relationship_type)
        self._check_dependency_size(tosca_relationships_network_binds_to, 5)
        self._check_dependency_value(tosca_relationships_network_binds_to, {
            'tosca.interfaces.relationship.Configure', 'tosca.interfaces.Root', 'tosca.capabilities.Node',
            'tosca.capabilities.Root', 'tosca.capabilities.network.Bindable'})
        self._check_requirement_dependency_size(tosca_relationships_network_binds_to, 0)
        self._check_derived_from_size(tosca_relationships_network_binds_to, 2)
        self._check_derived_from_value(tosca_relationships_network_binds_to, {
            'tosca.relationships.Root', 'tosca.relationships.DependsOn'})

    # Node Type

    def test_tosca_nodes_root(self):
        tosca_nodes_root = self.parsed_template.node_types['tosca.nodes.Root']
        self._check_value_of_tosca_object(tosca_nodes_root, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_root, 8)
        self._check_dependency_value(tosca_nodes_root, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn'})
        self._check_requirement_dependency_size(tosca_nodes_root, 3)
        self._check_requirement_dependency_value(tosca_nodes_root, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node'})
        self._check_derived_from_size(tosca_nodes_root, 0)

    def test_tosca_nodes_compute(self):
        tosca_nodes_compute = self.parsed_template.node_types['tosca.nodes.Compute']
        self._check_value_of_tosca_object(tosca_nodes_compute, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_compute, 24)
        self._check_dependency_value(tosca_nodes_compute, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.datatypes.network.NetworkInfo',
            'tosca.datatypes.Root', 'tosca.datatypes.network.PortInfo', 'tosca.capabilities.Container',
            'tosca.nodes.SoftwareComponent', 'tosca.capabilities.Endpoint.Admin', 'tosca.datatypes.network.PortDef',
            'tosca.datatypes.network.PortSpec', 'tosca.capabilities.Endpoint', 'tosca.capabilities.OperatingSystem',
            'tosca.capabilities.Scalable', 'tosca.capabilities.network.Bindable', 'tosca.capabilities.Attachment',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.datatypes.Credential', 'tosca.relationships.HostedOn', 'tosca.nodes.Compute',

        })
        self._check_requirement_dependency_size(tosca_nodes_compute, 6)
        self._check_requirement_dependency_value(tosca_nodes_compute, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node',
            'tosca.capabilities.Attachment', 'tosca.nodes.BlockStorage', 'tosca.relationships.AttachesTo'})
        self._check_derived_from_size(tosca_nodes_compute, 1)
        self._check_derived_from_value(tosca_nodes_compute, {'tosca.nodes.Root'})

    def test_tosca_nodes_software_component(self):
        tosca_nodes_software_component = self.parsed_template.node_types['tosca.nodes.SoftwareComponent']
        self._check_value_of_tosca_object(tosca_nodes_software_component, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_software_component, 26)
        self._check_dependency_value(tosca_nodes_software_component, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.datatypes.network.NetworkInfo',
            'tosca.datatypes.Root', 'tosca.datatypes.network.PortInfo', 'tosca.capabilities.Container',
            'tosca.nodes.SoftwareComponent', 'tosca.capabilities.Endpoint.Admin', 'tosca.datatypes.network.PortDef',
            'tosca.datatypes.network.PortSpec', 'tosca.capabilities.Endpoint', 'tosca.capabilities.OperatingSystem',
            'tosca.capabilities.Scalable', 'tosca.capabilities.network.Bindable', 'tosca.capabilities.Attachment',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.datatypes.Credential', 'tosca.relationships.HostedOn', 'tosca.nodes.Compute',
            'tosca.relationships.AttachesTo', 'tosca.nodes.BlockStorage'})
        self._check_requirement_dependency_size(tosca_nodes_software_component, 6)
        self._check_requirement_dependency_value(tosca_nodes_software_component, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node',
            'tosca.capabilities.Container', 'tosca.nodes.Compute', 'tosca.relationships.HostedOn'})
        self._check_derived_from_size(tosca_nodes_software_component, 1)
        self._check_derived_from_value(tosca_nodes_software_component, {'tosca.nodes.Root'})

    def test_tosca_nodes_webserver(self):
        tosca_nodes_webserver = self.parsed_template.node_types['tosca.nodes.WebServer']
        self._check_value_of_tosca_object(tosca_nodes_webserver, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_webserver, 28)
        self._check_dependency_value(tosca_nodes_webserver, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.datatypes.network.NetworkInfo',
            'tosca.datatypes.Root', 'tosca.datatypes.network.PortInfo', 'tosca.capabilities.Container',
            'tosca.nodes.SoftwareComponent', 'tosca.capabilities.Endpoint.Admin', 'tosca.datatypes.network.PortDef',
            'tosca.datatypes.network.PortSpec', 'tosca.capabilities.Endpoint', 'tosca.capabilities.OperatingSystem',
            'tosca.capabilities.Scalable', 'tosca.capabilities.network.Bindable', 'tosca.capabilities.Attachment',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.datatypes.Credential', 'tosca.relationships.HostedOn', 'tosca.nodes.Compute',
            'tosca.relationships.AttachesTo', 'tosca.nodes.BlockStorage', 'tosca.nodes.WebServer',
            'tosca.nodes.WebApplication'})
        self._check_requirement_dependency_size(tosca_nodes_webserver, 6)
        self._check_requirement_dependency_value(tosca_nodes_webserver, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node',
            'tosca.capabilities.Container', 'tosca.nodes.Compute', 'tosca.relationships.HostedOn'})
        self._check_derived_from_size(tosca_nodes_webserver, 2)
        self._check_derived_from_value(tosca_nodes_webserver, {'tosca.nodes.Root', 'tosca.nodes.SoftwareComponent'})

    def test_tosca_nodes_web_application(self):
        tosca_nodes_web_application = self.parsed_template.node_types['tosca.nodes.WebApplication']
        self._check_value_of_tosca_object(tosca_nodes_web_application, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_web_application, 28)
        self._check_dependency_value(tosca_nodes_web_application, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.datatypes.network.NetworkInfo',
            'tosca.datatypes.Root', 'tosca.datatypes.network.PortInfo', 'tosca.capabilities.Container',
            'tosca.nodes.SoftwareComponent', 'tosca.capabilities.Endpoint.Admin', 'tosca.datatypes.network.PortDef',
            'tosca.datatypes.network.PortSpec', 'tosca.capabilities.Endpoint', 'tosca.capabilities.OperatingSystem',
            'tosca.capabilities.Scalable', 'tosca.capabilities.network.Bindable', 'tosca.capabilities.Attachment',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.datatypes.Credential', 'tosca.relationships.HostedOn', 'tosca.nodes.Compute',
            'tosca.relationships.AttachesTo', 'tosca.nodes.BlockStorage', 'tosca.nodes.WebServer',
            'tosca.nodes.WebApplication'})
        self._check_requirement_dependency_size(tosca_nodes_web_application, 7)
        self._check_requirement_dependency_value(tosca_nodes_web_application, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node',
            'tosca.capabilities.Container', 'tosca.nodes.Compute', 'tosca.relationships.HostedOn',
            'tosca.nodes.WebServer'})
        self._check_derived_from_size(tosca_nodes_web_application, 2)
        self._check_derived_from_value(tosca_nodes_web_application, {'tosca.nodes.Root',
                                                                     'tosca.nodes.SoftwareComponent'})

    def test_tosca_nodes_dbms(self):
        tosca_nodes_dbms = self.parsed_template.node_types['tosca.nodes.DBMS']
        self._check_value_of_tosca_object(tosca_nodes_dbms, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_dbms, 29)
        self._check_dependency_value(tosca_nodes_dbms, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.datatypes.network.NetworkInfo',
            'tosca.datatypes.Root', 'tosca.datatypes.network.PortInfo', 'tosca.capabilities.Container',
            'tosca.nodes.SoftwareComponent', 'tosca.capabilities.Endpoint.Admin', 'tosca.datatypes.network.PortDef',
            'tosca.datatypes.network.PortSpec', 'tosca.capabilities.Endpoint', 'tosca.capabilities.OperatingSystem',
            'tosca.capabilities.Scalable', 'tosca.capabilities.network.Bindable', 'tosca.capabilities.Attachment',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.datatypes.Credential', 'tosca.relationships.HostedOn', 'tosca.nodes.Compute',
            'tosca.relationships.AttachesTo', 'tosca.nodes.BlockStorage', 'tosca.capabilities.Endpoint.Database',
            'tosca.nodes.DBMS', 'tosca.nodes.BlockStorage', 'tosca.nodes.Database'})
        self._check_requirement_dependency_size(tosca_nodes_dbms, 6)
        self._check_requirement_dependency_value(tosca_nodes_dbms, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node',
            'tosca.capabilities.Container', 'tosca.nodes.Compute', 'tosca.relationships.HostedOn'})
        self._check_derived_from_size(tosca_nodes_dbms, 2)
        self._check_derived_from_value(tosca_nodes_dbms, {'tosca.nodes.Root', 'tosca.nodes.SoftwareComponent'})

    def test_tosca_nodes_database(self):
        tosca_nodes_database = self.parsed_template.node_types['tosca.nodes.Database']
        self._check_value_of_tosca_object(tosca_nodes_database, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_database, 29)
        self._check_dependency_value(tosca_nodes_database, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.datatypes.network.NetworkInfo',
            'tosca.datatypes.Root', 'tosca.datatypes.network.PortInfo', 'tosca.capabilities.Container',
            'tosca.nodes.SoftwareComponent', 'tosca.capabilities.Endpoint.Admin', 'tosca.datatypes.network.PortDef',
            'tosca.datatypes.network.PortSpec', 'tosca.capabilities.Endpoint', 'tosca.capabilities.OperatingSystem',
            'tosca.capabilities.Scalable', 'tosca.capabilities.network.Bindable', 'tosca.capabilities.Attachment',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.datatypes.Credential', 'tosca.relationships.HostedOn', 'tosca.nodes.Compute',
            'tosca.relationships.AttachesTo', 'tosca.nodes.BlockStorage', 'tosca.capabilities.Endpoint.Database',
            'tosca.nodes.DBMS', 'tosca.nodes.BlockStorage', 'tosca.nodes.Database'})
        self._check_requirement_dependency_size(tosca_nodes_database, 6)
        self._check_requirement_dependency_value(tosca_nodes_database, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node',
            'tosca.capabilities.Container', 'tosca.nodes.DBMS', 'tosca.relationships.HostedOn'})
        self._check_derived_from_size(tosca_nodes_database, 1)
        self._check_derived_from_value(tosca_nodes_database, {'tosca.nodes.Root'})

    def test_tosca_nodes_object_storage(self):
        tosca_nodes_object_storage = self.parsed_template.node_types['tosca.nodes.ObjectStorage']
        self._check_value_of_tosca_object(tosca_nodes_object_storage, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_object_storage, 12)
        self._check_dependency_value(tosca_nodes_object_storage, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.datatypes.Root',
            'tosca.datatypes.network.PortDef', 'tosca.datatypes.network.PortSpec', 'tosca.capabilities.Endpoint'})
        self._check_requirement_dependency_size(tosca_nodes_object_storage, 3)
        self._check_requirement_dependency_value(tosca_nodes_object_storage, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node'})
        self._check_derived_from_size(tosca_nodes_object_storage, 1)
        self._check_derived_from_value(tosca_nodes_object_storage, {'tosca.nodes.Root'})

    def test_tosca_nodes_block_storage(self):
        tosca_nodes_block_storage = self.parsed_template.node_types['tosca.nodes.BlockStorage']
        self._check_value_of_tosca_object(tosca_nodes_block_storage, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_block_storage, 9)
        self._check_dependency_value(tosca_nodes_block_storage, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Attachment'})
        self._check_requirement_dependency_size(tosca_nodes_block_storage, 3)
        self._check_requirement_dependency_value(tosca_nodes_block_storage, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node'})
        self._check_derived_from_size(tosca_nodes_block_storage, 1)
        self._check_derived_from_value(tosca_nodes_block_storage, {'tosca.nodes.Root'})

    def test_tosca_nodes_container_runtime(self):
        tosca_nodes_software_component = self.parsed_template.node_types['tosca.nodes.Container.Runtime']
        self._check_value_of_tosca_object(tosca_nodes_software_component, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_software_component, 26)
        self._check_dependency_value(tosca_nodes_software_component, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.datatypes.network.NetworkInfo',
            'tosca.datatypes.Root', 'tosca.datatypes.network.PortInfo', 'tosca.capabilities.Container',
            'tosca.nodes.SoftwareComponent', 'tosca.capabilities.Endpoint.Admin', 'tosca.datatypes.network.PortDef',
            'tosca.datatypes.network.PortSpec', 'tosca.capabilities.Endpoint', 'tosca.capabilities.OperatingSystem',
            'tosca.capabilities.Scalable', 'tosca.capabilities.network.Bindable', 'tosca.capabilities.Attachment',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.datatypes.Credential', 'tosca.relationships.HostedOn', 'tosca.nodes.Compute',
            'tosca.relationships.AttachesTo', 'tosca.nodes.BlockStorage'})
        self._check_requirement_dependency_size(tosca_nodes_software_component, 6)
        self._check_requirement_dependency_value(tosca_nodes_software_component, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node',
            'tosca.capabilities.Container', 'tosca.nodes.Compute', 'tosca.relationships.HostedOn'})
        self._check_derived_from_size(tosca_nodes_software_component, 2)
        self._check_derived_from_value(tosca_nodes_software_component, {'tosca.nodes.Root',
                                                                        'tosca.nodes.SoftwareComponent'})

    def test_tosca_nodes_container_application(self):
        tosca_nodes_container_application = self.parsed_template.node_types['tosca.nodes.Container.Application']
        self._check_value_of_tosca_object(tosca_nodes_container_application, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_container_application, 26)
        self._check_dependency_value(tosca_nodes_container_application, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.datatypes.network.NetworkInfo',
            'tosca.datatypes.Root', 'tosca.datatypes.network.PortInfo', 'tosca.capabilities.Container',
            'tosca.nodes.SoftwareComponent', 'tosca.capabilities.Endpoint.Admin', 'tosca.datatypes.network.PortDef',
            'tosca.datatypes.network.PortSpec', 'tosca.capabilities.Endpoint', 'tosca.capabilities.OperatingSystem',
            'tosca.capabilities.Scalable', 'tosca.capabilities.network.Bindable', 'tosca.capabilities.Attachment',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.datatypes.Credential', 'tosca.relationships.HostedOn', 'tosca.nodes.Compute',
            'tosca.relationships.AttachesTo', 'tosca.nodes.BlockStorage'})
        self._check_requirement_dependency_size(tosca_nodes_container_application, 6)
        self._check_requirement_dependency_value(tosca_nodes_container_application, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node',
            'tosca.capabilities.Container', 'tosca.nodes.Container.Runtime', 'tosca.relationships.HostedOn'})
        self._check_derived_from_size(tosca_nodes_container_application, 1)
        self._check_derived_from_value(tosca_nodes_container_application, {'tosca.nodes.Root'})

    def test_tosca_nodes_load_balancer(self):
        tosca_nodes_load_balancer = self.parsed_template.node_types['tosca.nodes.LoadBalancer']
        self._check_value_of_tosca_object(tosca_nodes_load_balancer, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_load_balancer, 15)
        self._check_dependency_value(tosca_nodes_load_balancer, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.datatypes.Root', 'tosca.datatypes.Credential',
            'tosca.datatypes.network.PortDef', 'tosca.datatypes.network.PortSpec', 'tosca.capabilities.Endpoint',
            'tosca.capabilities.Endpoint.Public', 'tosca.relationships.ConnectsTo'})
        self._check_requirement_dependency_size(tosca_nodes_load_balancer, 5)
        self._check_requirement_dependency_value(tosca_nodes_load_balancer, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node',
            'tosca.capabilities.Endpoint', 'tosca.relationships.RoutesTo'})
        self._check_derived_from_size(tosca_nodes_load_balancer, 1)
        self._check_derived_from_value(tosca_nodes_load_balancer, {'tosca.nodes.Root'})

    def test_tosca_nodes_network_network(self):
        tosca_nodes_network_network = self.parsed_template.node_types['tosca.nodes.network.Network']
        self._check_value_of_tosca_object(tosca_nodes_network_network, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_network_network, 9)
        self._check_dependency_value(tosca_nodes_network_network, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.network.Linkable'})
        self._check_requirement_dependency_size(tosca_nodes_network_network, 3)
        self._check_requirement_dependency_value(tosca_nodes_network_network, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node'})
        self._check_derived_from_size(tosca_nodes_network_network, 1)
        self._check_derived_from_value(tosca_nodes_network_network, {'tosca.nodes.Root'})

    def test_tosca_nodes_network_port(self):
        tosca_nodes_network_port = self.parsed_template.node_types['tosca.nodes.network.Port']
        self._check_value_of_tosca_object(tosca_nodes_network_port, TypeOfTypeEnum.node_type)
        self._check_dependency_size(tosca_nodes_network_port, 10)
        self._check_dependency_value(tosca_nodes_network_port, {
            'tosca.capabilities.Node', 'tosca.capabilities.Root', 'tosca.interfaces.node.lifecycle.Standard',
            'tosca.interfaces.Root', 'tosca.interfaces.relationship.Configure', 'tosca.relationships.Root',
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.network.Linkable',
            'tosca.capabilities.network.Bindable'})
        self._check_requirement_dependency_size(tosca_nodes_network_port, 7)
        self._check_requirement_dependency_value(tosca_nodes_network_port, {
            'tosca.nodes.Root', 'tosca.relationships.DependsOn', 'tosca.capabilities.Node',
            'tosca.capabilities.network.Bindable', 'tosca.relationships.network.BindsTo',
            'tosca.capabilities.network.Linkable', 'tosca.relationships.network.LinksTo'})
        self._check_derived_from_size(tosca_nodes_network_port, 1)
        self._check_derived_from_value(tosca_nodes_network_port, {'tosca.nodes.Root'})


