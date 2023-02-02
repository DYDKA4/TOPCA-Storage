from mariadb_parser.ORM_model.DataBase import Type, TypeOfTypeEnum, DependencyTypes, DependencyTypeEnum
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
        self.loader.insert_type_storage(self.parsed_template)
        # todo get indexes of types

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_tosca_datatypes_root(self):
        tosca_datatype_root = self.session.query(Type).filter_by(type_name='tosca.datatypes.Root').first()
        assert tosca_datatype_root.version == '1.0'
        assert tosca_datatype_root.type_of_type == TypeOfTypeEnum.data_type
        assert tosca_datatype_root.data == \
               self.parsed_template.data_types['tosca.datatypes.Root'].convert_data_to_json()

    def test_tosca_datatypes_credential(self):
        tosca_datatype_credential = self.session.query(Type).filter_by(type_name='tosca.datatypes.Credential').first()
        assert tosca_datatype_credential.version == '1.0'
        assert tosca_datatype_credential.type_of_type == TypeOfTypeEnum.data_type
        assert tosca_datatype_credential.data == \
               self.parsed_template.data_types['tosca.datatypes.Credential'].convert_data_to_json()
        tosca_datatype_credential_dependency = self.session.query(DependencyTypes).filter_by(
            source_id=tosca_datatype_credential.id)
        # todo tosca_datatype_credential_dependency to list
        assert len(tosca_datatype_credential_dependency) == 1
        type_to_check = self.session.query(Type).filter_by(
            id=tosca_datatype_credential_dependency[0].dependency_id).first()
        assert type_to_check.type_name in self.parsed_template.data_types['tosca.datatypes.Credential'].derived_from

    def test_tosca_datatypes_network_info(self):
        tosca_datatype_network_info = self.session.query(Type).filter_by(
            type_name='tosca.datatypes.network.NetworkInfo').first()
        assert tosca_datatype_network_info.version == '1.0'
        assert tosca_datatype_network_info.type_of_type == TypeOfTypeEnum.data_type
        assert tosca_datatype_network_info.data == \
               self.parsed_template.data_types['tosca.datatypes.network.NetworkInfo'].convert_data_to_json()
        tosca_datatype_credential_dependency = self.session.query(DependencyTypes).filter_by(
            source_id=tosca_datatype_network_info.id)
        # todo tosca_datatype_credential_dependency to list sorted by dependency_id
        assert len(tosca_datatype_credential_dependency) == 1
        type_to_check = self.session.query(Type).filter_by(
            id=tosca_datatype_credential_dependency[0].dependency_id).first()
        assert type_to_check.type_name in self.parsed_template.data_types[
            'tosca.datatypes.network.NetworkInfo'].derived_from

    def test_tosca_datatypes_port_info(self):
        tosca_datatype_port_info = self.session.query(Type).filter_by(
            type_name='tosca.datatypes.network.PortInfo').first()
        assert tosca_datatype_port_info.version == '1.0'
        assert tosca_datatype_port_info.type_of_type == TypeOfTypeEnum.data_type
        assert tosca_datatype_port_info.data == \
               self.parsed_template.data_types['tosca.datatypes.network.PortInfo'].convert_data_to_json()
        tosca_datatype_credential_dependency = self.session.query(DependencyTypes).filter_by(
            source_id=tosca_datatype_port_info.id)
        # todo tosca_datatype_credential_dependency to list sorted by dependency_id
        assert len(tosca_datatype_credential_dependency) == 1
        type_to_check = self.session.query(Type).filter_by(
            id=tosca_datatype_credential_dependency[0].dependency_id).first()
        assert type_to_check.type_name in self.parsed_template.data_types[
            'tosca.datatypes.network.PortInfo'].derived_from

    def test_tosca_datatypes_port_def(self):
        tosca_datatype_port_def = self.session.query(Type).filter_by(
            type_name='tosca.datatypes.network.PortDef').first()
        assert tosca_datatype_port_def.version == '1.0'
        assert tosca_datatype_port_def.type_of_type == TypeOfTypeEnum.data_type
        assert tosca_datatype_port_def.data == \
               self.parsed_template.data_types['tosca.datatypes.network.PortDef'].convert_data_to_json()
        tosca_datatype_credential_dependency = self.session.query(DependencyTypes).filter_by(
            source_id=tosca_datatype_port_def.id)
        # todo tosca_datatype_credential_dependency to list sorted by dependency_id
        assert len(tosca_datatype_credential_dependency) == 1
        type_to_check = self.session.query(Type).filter_by(
            id=tosca_datatype_credential_dependency[0].dependency_id).first()
        assert type_to_check.type_name in self.parsed_template.data_types[
            'tosca.datatypes.network.PortDef'].derived_from

    def test_tosca_datatypes_port_spec(self):
        tosca_datatype_port_spec = self.session.query(Type).filter_by(
            type_name='tosca.datatypes.network.PortSpec').first()
        assert tosca_datatype_port_spec.version == '1.0'
        assert tosca_datatype_port_spec.type_of_type == TypeOfTypeEnum.data_type
        assert tosca_datatype_port_spec.data == \
               self.parsed_template.data_types['tosca.datatypes.network.PortSpec'].convert_data_to_json()
        tosca_datatype_credential_derived_from = self.session.query(DependencyTypes).filter_by(
            source_id=tosca_datatype_port_spec.id, dependency_type=DependencyTypeEnum.derived_from)
        # todo tosca_datatype_credential_derived_from to list sorted by dependency_id
        assert len(tosca_datatype_credential_derived_from) == 2
        for elem in tosca_datatype_credential_derived_from:
            type_to_check = self.session.query(Type).filter_by(id=elem.dependency_id).first()
            assert type_to_check.type_name in self.parsed_template.data_types[
                'tosca.datatypes.network.PortSpec'].derived_from
            self.parsed_template.data_types['tosca.datatypes.network.PortSpec'].derived_from.remove(
                type_to_check.type_name)
        tosca_datatype_credential_dependency = self.session.query(DependencyTypes).filter_by(
            source_id=tosca_datatype_port_spec.id, dependency_type=DependencyTypeEnum.dependency)
        assert len(tosca_datatype_credential_derived_from) == 1
        type_to_check = self.session.query(Type).filter_by(
            id=tosca_datatype_credential_dependency[0].dependency_id).first()
        assert self.parsed_template.data_types[]

#

# Type(id=6,
#      version='1.0',
#      type_of_type='data_type',
#      type_name='tosca.datatypes.network.PortSpec',
#      data="{\"derived_from\": \"tosca.datatypes.network.PortDef\", \"properties\": {\"protocol\": {\"type\": "
#           "\"string\", \"required\": true, \"default\": \"tcp\", \"constraints\": [{\"valid_values\": [\"udp\", "
#           "\"tcp\", \"igmp\", \"icmp\"]}]}, \"target\": {\"type\": \"tosca.datatypes.network.PortDef\", \"required\": "
#           "false}, \"target_range\": {\"type\": \"range\", \"required\": false, \"constraints\": [{\"in_range\": [1, "
#           "65535]}]}, \"source\": {\"type\": \"tosca.datatypes.network.PortDef\", \"required\": false}, "
#           "\"source_range\": {\"type\": \"range\", \"required\": false, \"constraints\": [{\"in_range\": [1, "
#           "65535]}]}}}")
#
# DependencyTypes(source_id=6,
#                 dependency_id=5,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=6,
#                 dependency_id=1,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=6,
#                 dependency_id=5,
#                 dependency_type='dependency')
# }
# # Group Types
# Type(id=52,
#      version='1.0',
#      type_of_type='group_type',
#      type_name='tosca.groups.Root',
#      data="{\"description\": \"The TOSCA Group Type all other TOSCA Group Types derive from\", \"interfaces\": {"
#           "\"Standard\": {\"type\": \"tosca.interfaces.node.lifecycle.Standard\"}}}")
#
# DependencyTypes(source_id=52,
#                 dependency_id=28,
#                 dependency_type='dependency')
# # Interface Types
#
# Type(id=27,
#      version='1.0',
#      type_of_type='interface_type',
#      type_name='tosca.interfaces.Root',
#      data="{\"description\": \"The TOSCA root Interface Type all other TOSCA base Interface Types derive from\\n\"}")
#
# Type(id=28,
#      version='1.0',
#      type_of_type='interface_type',
#      type_name='tosca.interfaces.node.lifecycle.Standard',
#      data="{\"description\": \"This lifecycle interface defines the essential, normative operations that TOSCA nodes "
#           "may support.\", \"derived_from\": \"tosca.interfaces.Root\", \"create\": {\"description\": \"Standard "
#           "lifecycle create operation.\"}, \"configure\": {\"description\": \"Standard lifecycle configure "
#           "operation.\"}, \"start\": {\"description\": \"Standard lifecycle start operation.\"}, \"stop\": {"
#           "\"description\": \"Standard lifecycle stop operation.\"}, \"delete\": {\"description\": \"Standard "
#           "lifecycle delete operation.\"}}")
#
# DependencyTypes(source_id=28,
#                 dependency_id=27,
#                 dependency_type='derived_from')
#
# Type(id=29,
#      version='1.0',
#      type_of_type='interface_type',
#      type_name='tosca.interfaces.relationship.Configure',
#      data="{\"description\": \"The lifecycle interfaces define the essential, normative operations that each TOSCA "
#           "Relationship Types may support.\\n\", \"derived_from\": \"tosca.interfaces.Root\", "
#           "\"pre_configure_source\": {\"description\": \"Operation to pre-configure the source endpoint.\"}, "
#           "\"pre_configure_target\": {\"description\": \"Operation to pre-configure the target endpoint.\"}, "
#           "\"post_configure_source\": {\"description\": \"Operation to post-configure the source endpoint.\"}, "
#           "\"post_configure_target\": {\"description\": \"Operation to post-configure the target endpoint.\"}, "
#           "\"add_target\": {\"description\": \"Operation to add a target node.\"}, \"remove_target\": {"
#           "\"description\": \"Operation to remove a target node.\"}, \"add_source\": {\"description\": \"Operation to "
#           "notify the target node of a source node which is now available via a relationship.\\n\"}, "
#           "\"target_changed\": {\"description\": \"Operation to notify source some property or attribute of the "
#           "target changed\\n\"}}")
#
# DependencyTypes(source_id=29,
#                 dependency_id=27,
#                 dependency_type='derived_from')
#
# # Capability Type
#
# Type(id=7,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.Root',
#      data="{\"description\": \"The TOSCA root Capability Type all other TOSCA base Capability Types derive from.\\n\"}")
#
# Type(id=8,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.Node',
#      data="{\"description\": \"The Node capability indicates the base capabilities of a TOSCA Node Type.\", "
#           "\"derived_from\": \"tosca.capabilities.Root\"}")
#
# DependencyTypes(source_id=8,
#                 dependency_id=7,
#                 dependency_type='derived_from')
#
# Type(id=9,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.Container',
#      data="{\"description\": \"The Container capability, when included on a Node Type or Template definition, "
#           "indicates that the node can act as a container for (or a host for) one or more other declared Node "
#           "Types.\\n\", \"derived_from\": \"tosca.capabilities.Root\", \"properties\": {\"num_cpus\": {\"required\": "
#           "false, \"type\": \"integer\", \"constraints\": [{\"greater_or_equal\": 1}]}, \"cpu_frequency\": {"
#           "\"required\": false, \"type\": \"scalar-unit.frequency\", \"constraints\": [{\"greater_or_equal\": \"0.1 "
#           "GHz\"}]}, \"disk_size\": {\"required\": false, \"type\": \"scalar-unit.size\", \"constraints\": [{"
#           "\"greater_or_equal\": \"0 MB\"}]}, \"mem_size\": {\"required\": false, \"type\": \"scalar-unit.size\", "
#           "\"constraints\": [{\"greater_or_equal\": \"0 MB\"}]}}}")
#
# DependencyTypes(source_id=9,
#                 dependency_id=7,
#                 dependency_type='derived_from')
#
# Type(id=10,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.Endpoint',
#      data="{\"description\": \"This is the default TOSCA type that should be used or extended to define a network "
#           "endpoint capability. This includes the information to express a basic endpoint with a single port or a "
#           "complex endpoint with multiple ports. By default the Endpoint is assumed to represent an address on a "
#           "private network unless otherwise specified.\\n\", \"derived_from\": \"tosca.capabilities.Root\", "
#           "\"properties\": {\"protocol\": {\"type\": \"string\", \"required\": true, \"default\": \"tcp\"}, "
#           "\"port\": {\"type\": \"tosca.datatypes.network.PortDef\", \"required\": false}, \"secure\": {\"type\": "
#           "\"boolean\", \"required\": false, \"default\": false}, \"url_path\": {\"type\": \"string\", \"required\": "
#           "false}, \"port_name\": {\"type\": \"string\", \"required\": false}, \"network_name\": {\"type\": "
#           "\"string\", \"required\": false, \"default\": \"PRIVATE\"}, \"initiator\": {\"type\": \"string\", "
#           "\"required\": false, \"default\": \"source\", \"constraints\": [{\"valid_values\": [\"source\", "
#           "\"target\", \"peer\"]}]}, \"ports\": {\"type\": \"map\", \"required\": false, \"constraints\": [{"
#           "\"min_length\": 1}], \"entry_schema\": {\"type\": \"tosca.datatypes.network.PortSpec\"}}, \"ip_address\": "
#           "{\"type\": \"string\", \"default\": \"0.0.0.0/0\"}}}")
#
# DependencyTypes(source_id=10,
#                 dependency_id=7,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=10,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=10,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# Type(id=11,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.Endpoint.Admin',
#      data="{\"description\": \"This is the default TOSCA type that should be used or extended to define a specialized "
#           "administrator endpoint capability.\\n\", \"derived_from\": \"tosca.capabilities.Endpoint\", "
#           "\"properties\": {\"secure\": {\"type\": \"boolean\", \"default\": true, \"required\": false, "
#           "\"constraints\": [{\"equal\": true}]}}}")
#
# DependencyTypes(source_id=11,
#                 dependency_id=10,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=11,
#                 dependency_id=7,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=11,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=11,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# Type(id=12,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.Endpoint.Public',
#      data="{\"description\": \"This capability represents a public endpoint which is accessible to the general "
#           "internet (and its public IP address ranges).\\n\", \"derived_from\": \"tosca.capabilities.Endpoint\", "
#           "\"properties\": {\"network_name\": {\"type\": \"string\", \"default\": \"PUBLIC\", \"required\": false, "
#           "\"constraints\": [{\"equal\": \"PUBLIC\"}]}, \"floating\": {\"description\": \"Indicates that the public "
#           "address should be allocated from a pool of floating IPs that are associated with the network.\\n\", "
#           "\"type\": \"boolean\", \"default\": false, \"status\": \"experimental\", \"required\": false}, "
#           "\"dns_name\": {\"description\": \"The optional name to register with DNS\", \"type\": \"string\", "
#           "\"required\": false, \"status\": \"experimental\"}}}")
#
# DependencyTypes(source_id=12,
#                 dependency_id=10,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=12,
#                 dependency_id=7,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=12,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=12,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# Type(id=13,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.Endpoint.Database',
#      data="{\"derived_from\": \"tosca.capabilities.Endpoint\"}")
#
# DependencyTypes(source_id=13,
#                 dependency_id=10,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=13,
#                 dependency_id=7,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=13,
#                 dependency_id=5,
#                 dependency_type='dependency')
#
# DependencyTypes(source_id=13,
#                 dependency_id=6,
#                 dependency_type='dependency')
#
# Type(id=14,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.Attachment',
#      data="{\"description\": \"This is the default TOSCA type that should be used or extended to define an attachment "
#           "capability of a (logical) infrastructure device node (e.g., BlockStorage node)\\n\", \"derived_from\": "
#           "\"tosca.capabilities.Root\"}")
#
# DependencyTypes(source_id=14,
#                 dependency_id=7,
#                 dependency_type='derived_from')
#
# Type(id=15,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.OperatingSystem',
#      data="{\"derived_from\": \"tosca.capabilities.Root\", \"properties\": {\"architecture\": {\"required\": false, "
#           "\"type\": \"string\", \"description\": \"The host Operating System (OS) architecture.\\n\"}, \"type\": {"
#           "\"required\": false, \"type\": \"string\", \"description\": \"The host Operating System (OS) type.\\n\"}, "
#           "\"distribution\": {\"required\": false, \"type\": \"string\", \"description\": \"The host Operating System "
#           "(OS) distribution. Examples of valid values for an \\u201ctype\\u201d of \\u201cLinux\\u201d would "
#           "include: debian, fedora, rhel and ubuntu.\\n\"}, \"version\": {\"required\": false, \"type\": \"version\", "
#           "\"description\": \"The host Operating System version.\\n\"}}}")
#
# DependencyTypes(source_id=15,
#                 dependency_id=7,
#                 dependency_type='derived_from')
#
# Type(id=16,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.Scalable',
#      data="{\"derived_from\": \"tosca.capabilities.Root\", \"properties\": {\"min_instances\": {\"type\": "
#           "\"integer\", \"required\": true, \"default\": 1, \"description\": \"This property is used to indicate the "
#           "minimum number of instances that should be created for the associated TOSCA Node Template by a TOSCA "
#           "orchestrator.\\n\"}, \"max_instances\": {\"type\": \"integer\", \"required\": true, \"default\": 1, "
#           "\"description\": \"This property is used to indicate the maximum number of instances that should be "
#           "created for the associated TOSCA Node Template by a TOSCA orchestrator.\\n\"}, \"default_instances\": {"
#           "\"type\": \"integer\", \"required\": false, \"description\": \"An optional property that indicates the "
#           "requested default number of instances that should be the starting number of instances a TOSCA orchestrator "
#           "should attempt to allocate. The value for this property MUST be in the range between the values set for "
#           "min_instances and max_instances properties.\\n\"}}}")
#
# DependencyTypes(source_id=16,
#                 dependency_id=7,
#                 dependency_type='derived_from')
#
# Type(id=17,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.network.Linkable',
#      data="{\"derived_from\": \"tosca.capabilities.Node\", \"description\": \"A node type that includes the Linkable "
#           "capability indicates that it can be pointed by tosca.relationships.network.LinksTo relationship type, "
#           "which represents an association relationship between Port and Network node types.\\n\"}")
#
# DependencyTypes(source_id=17,
#                 dependency_id=7,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=17,
#                 dependency_id=8,
#                 dependency_type='derived_from')
#
# Type(id=18,
#      version='1.0',
#      type_of_type='capability_type',
#      type_name='tosca.capabilities.network.Bindable',
#      data="{\"derived_from\": \"tosca.capabilities.Node\", \"description\": \"A node type that includes the Bindable "
#           "capability indicates that it can be pointed by tosca.relationships.network.BindsTo relationship type, "
#           "which represents a network association relationship between Port and Compute node types.\\n\"}")
#
# DependencyTypes(source_id=18,
#                 dependency_id=7,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=18,
#                 dependency_id=8,
#                 dependency_type='derived_from')
#
# # Policy Type
#
# Type(id=53,
#      version='1.0',
#      type_of_type='policy_type',
#      type_name='tosca.policies.Root',
#      data="{\"description\": \"The TOSCA Policy Type all other TOSCA Policy Types derive from.\"}")
#
# Type(id=54,
#      version='1.0',
#      type_of_type='policy_type',
#      type_name='tosca.policies.Placement',
#      data="{\"derived_from\": \"tosca.policies.Root\", \"description\": \"The TOSCA Policy Type definition that is "
#           "used to govern placement of TOSCA nodes or groups of nodes.\"}")
#
# DependencyTypes(source_id=54,
#                 dependency_id=53,
#                 dependency_type='derived_from')
#
# Type(id=55,
#      version='1.0',
#      type_of_type='policy_type',
#      type_name='tosca.policies.Scaling',
#      data="{\"derived_from\": \"tosca.policies.Root\", \"description\": \"The TOSCA Policy Type definition that is "
#           "used to govern scaling of TOSCA nodes or groups of nodes.\"}")
#
# DependencyTypes(source_id=55,
#                 dependency_id=53,
#                 dependency_type='derived_from')
#
# Type(id=56,
#      version='1.0',
#      type_of_type='policy_type',
#      type_name='tosca.policies.Update',
#      data="{\"derived_from\": \"tosca.policies.Root\", \"description\": \"The TOSCA Policy Type definition that is "
#           "used to govern update of TOSCA nodes or groups of nodes.\"}")
#
# DependencyTypes(source_id=56,
#                 dependency_id=53,
#                 dependency_type='derived_from')
#
# Type(id=57,
#      version='1.0',
#      type_of_type='policy_type',
#      type_name='tosca.policies.Performance',
#      data="{\"derived_from\": \"tosca.policies.Root\", \"description\": \"The TOSCA Policy Type definition that is "
#           "used to declare performance requirements for TOSCA nodes or groups of nodes.\"}")
#
# DependencyTypes(source_id=57,
#                 dependency_id=53,
#                 dependency_type='derived_from')
#
# # Artifact Type
#
# Type(id=19,
#      version='1.0',
#      type_of_type='artifact_type',
#      type_name='tosca.artifacts.Root',
#      data="{\"description\": \"The TOSCA Artifact Type all other TOSCA Artifact Types derive from\\n\", "
#           "\"properties\": {\"version\": {\"type\": \"version\", \"required\": false}}}")
#
# Type(id=20,
#      version='1.0',
#      type_of_type='artifact_type',
#      type_name='tosca.artifacts.File',
#      data="{\"derived_from\": \"tosca.artifacts.Root\"}")
#
# DependencyTypes(source_id=20,
#                 dependency_id=19,
#                 dependency_type='derived_from')
#
# Type(id=21,
#      version='1.0',
#      type_of_type='artifact_type',
#      type_name='tosca.artifacts.Deployment',
#      data="{\"derived_from\": \"tosca.artifacts.Root\", \"description\": \"TOSCA base type for deployment artifacts\"}")
#
# DependencyTypes(source_id=21,
#                 dependency_id=19,
#                 dependency_type='derived_from')
#
# Type(id=22,
#      version='1.0',
#      type_of_type='artifact_type',
#      type_name='tosca.artifacts.Deployment.Image',
#      data="{\"derived_from\": \"tosca.artifacts.Deployment\"}")
#
# DependencyTypes(source_id=22,
#                 dependency_id=21,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=22,
#                 dependency_id=19,
#                 dependency_type='derived_from')
#
# Type(id=23,
#      version='1.0',
#      type_of_type='artifact_type',
#      type_name='tosca.artifacts.Deployment.Image.VM',
#      data="{\"derived_from\": \"tosca.artifacts.Deployment.Image\"}")
#
# DependencyTypes(source_id=23,
#                 dependency_id=22,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=23,
#                 dependency_id=21,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=23,
#                 dependency_id=19,
#                 dependency_type='derived_from')
#
# Type(id=24,
#      version='1.0',
#      type_of_type='artifact_type',
#      type_name='tosca.artifacts.Implementation',
#      data="{\"derived_from\": \"tosca.artifacts.Root\", \"description\": \"TOSCA base type for implementation "
#           "artifacts\"}")
#
# DependencyTypes(source_id=24,
#                 dependency_id=19,
#                 dependency_type='derived_from')
#
# Type(id=25,
#      version='1.0',
#      type_of_type='artifact_type',
#      type_name='tosca.artifacts.Implementation.Bash',
#      data="{\"derived_from\": \"tosca.artifacts.Implementation\", \"description\": \"Script artifact for the Unix "
#           "Bash shell\", \"mime_type\": \"application/x-sh\", \"file_ext\": [\"sh\"]}")
#
# DependencyTypes(source_id=25,
#                 dependency_id=24,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=25,
#                 dependency_id=19,
#                 dependency_type='derived_from')
#
# Type(id=26,
#      version='1.0',
#      type_of_type='artifact_type',
#      type_name='tosca.artifacts.Implementation.Python',
#      data="{\"derived_from\": \"tosca.artifacts.Implementation\", \"description\": \"Artifact for the interpreted "
#           "Python language\", \"mime_type\": \"application/x-python\", \"file_ext\": [\"py\"]}")
#
# DependencyTypes(source_id=26,
#                 dependency_id=24,
#                 dependency_type='derived_from')
#
# DependencyTypes(source_id=26,
#                 dependency_id=19,
#                 dependency_type='derived_from')
#
# # Relationship Types
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
