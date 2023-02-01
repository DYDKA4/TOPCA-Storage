test_data = {'tosca_definitions_version': 'tosca_simple_yaml_1_0',
             'data_types':
                 {'tosca.datatypes.Root':
                      {'description': 'The TOSCA root Data Type all other TOSCA base Data Types derive from\n'},
                  'tosca.datatypes.Credential': {'derived_from': 'tosca.datatypes.Root',
                                                 'properties': {'protocol': {'type': 'string', 'required': False},
                                                                'token_type': {'type': 'string', 'default': 'password',
                                                                               'required': True},
                                                                'token': {'type': 'string', 'required': True},
                                                                'keys': {'type': 'map',
                                                                         'entry_schema': {'type': 'string'},
                                                                         'required': False},
                                                                'user': {'type': 'string', 'required': False}}},
                  'tosca.datatypes.network.NetworkInfo': {'derived_from': 'tosca.datatypes.Root', 'properties': {
                      'network_name': {'type': 'string', 'required': False},
                      'network_id': {'type': 'string', 'required': False},
                      'addresses': {'type': 'list', 'required': False, 'entry_schema': {'type': 'string'}}}},
                  'tosca.datatypes.network.PortInfo': {'derived_from': 'tosca.datatypes.Root', 'properties': {
                      'port_name': {'type': 'string', 'required': False},
                      'port_id': {'type': 'string', 'required': False},
                      'network_id': {'type': 'string', 'required': False},
                      'mac_address': {'type': 'string', 'required': False},
                      'addresses': {'type': 'list', 'required': False, 'entry_schema': {'type': 'string'}}}},
                  'tosca.datatypes.network.PortDef': {'derived_from': 'tosca.datatypes.Root',
                                                      'constraints': [{'in_range': [1, 65535]}]},
                  'tosca.datatypes.network.PortSpec': {'derived_from': 'tosca.datatypes.network.PortDef',
                                                       'properties': {'protocol': {'type': 'string', 'required': True,
                                                                                   'default': 'tcp', 'constraints': [
                                                               {'valid_values': ['udp', 'tcp', 'igmp', 'icmp']}]},
                                                                      'target': {
                                                                          'type': 'tosca.datatypes.network.PortDef',
                                                                          'required': False},
                                                                      'target_range': {'type': 'range',
                                                                                       'required': False,
                                                                                       'constraints': [
                                                                                           {'in_range': [1, 65535]}]},
                                                                      'source': {
                                                                          'type': 'tosca.datatypes.network.PortDef',
                                                                          'required': False},
                                                                      'source_range': {'type': 'range',
                                                                                       'required': False,
                                                                                       'constraints': [{'in_range': [1,
                                                                                                                     65535]}]}}}},
             'node_types': {'tosca.nodes.Root': {
                 'description': 'The TOSCA root node all other TOSCA base node types derive from.\n', 'properties': {
                     'tosca_id': {
                         'description': 'A unique identifier of the realized instance of a Node Template that derives from any TOSCA normative type.\n',
                         'type': 'string', 'required': False}, 'tosca_name': {
                         'description': 'This attribute reflects the name of the Node Template as defined in the TOSCA service template.\n',
                         'type': 'string', 'required': False}, 'state': {
                         'description': 'The state of the node instance. See section “Node States” for allowed values.\n',
                         'type': 'string', 'required': False}},
                 'capabilities': {'feature': {'type': 'tosca.capabilities.Node'}}, 'requirements': [{'dependency': {
                     'capability': 'tosca.capabilities.Node', 'node': 'tosca.nodes.Root',
                     'relationship': 'tosca.relationships.DependsOn', 'occurrences': [0, 'UNBOUNDED']}}],
                 'interfaces': {'Standard': {'type': 'tosca.interfaces.node.lifecycle.Standard'}}},
                            'tosca.nodes.Compute': {
                                'description': 'The TOSCA Compute node represents one or more real or virtual processors of software applications or services along with other essential local resources.\n',
                                'derived_from': 'tosca.nodes.Root',
                                'properties': {'meta': {'type': 'string', 'required': False},
                                               'private_address': {'type': 'string', 'required': False},
                                               'public_address': {'type': 'string', 'required': False},
                                               'networks': {'type': 'map', 'entry_schema': {
                                                   'type': 'tosca.datatypes.network.NetworkInfo'}, 'required': False},
                                               'ports': {'type': 'map',
                                                         'entry_schema': {'type': 'tosca.datatypes.network.PortInfo'},
                                                         'required': False}}, 'capabilities': {
                                    'host': {'type': 'tosca.capabilities.Container',
                                             'valid_source_types': ['tosca.nodes.SoftwareComponent']},
                                    'endpoint': {'type': 'tosca.capabilities.Endpoint.Admin'},
                                    'os': {'type': 'tosca.capabilities.OperatingSystem'},
                                    'scalable': {'type': 'tosca.capabilities.Scalable'},
                                    'binding': {'type': 'tosca.capabilities.network.Bindable'}}, 'requirements': [{
                                                                                                                      'local_storage': {
                                                                                                                          'capability': 'tosca.capabilities.Attachment',
                                                                                                                          'node': 'tosca.nodes.BlockStorage',
                                                                                                                          'relationship': 'tosca.relationships.AttachesTo',
                                                                                                                          'occurrences': [
                                                                                                                              0,
                                                                                                                              'UNBOUNDED']}}]},
                            'tosca.nodes.SoftwareComponent': {
                                'description': 'The TOSCA SoftwareComponent node represents a generic software component that can be managed and run by a TOSCA Compute Node Type.\n',
                                'derived_from': 'tosca.nodes.Root', 'properties': {
                                    'component_version': {'type': 'version', 'required': False,
                                                          'description': 'Software component version.\n'},
                                    'admin_credential': {'type': 'tosca.datatypes.Credential', 'required': False}},
                                'requirements': [{'host': {'capability': 'tosca.capabilities.Container',
                                                           'node': 'tosca.nodes.Compute',
                                                           'relationship': 'tosca.relationships.HostedOn'}}]},
                            'tosca.nodes.WebServer': {
                                'description': 'This TOSCA WebServer Node Type represents an abstract software component or service that is capable of hosting and providing management operations for one or more WebApplication nodes\n',
                                'derived_from': 'tosca.nodes.SoftwareComponent',
                                'capabilities': {'data_endpoint': {'type': 'tosca.capabilities.Endpoint'},
                                                 'admin_endpoint': {'type': 'tosca.capabilities.Endpoint.Admin'},
                                                 'host': {'type': 'tosca.capabilities.Container',
                                                          'valid_source_types': ['tosca.nodes.WebApplication']}}},
                            'tosca.nodes.WebApplication': {
                                'description': 'The TOSCA WebApplication node represents a software application that can be managed and run by a TOSCA WebServer node.\n',
                                'derived_from': 'tosca.nodes.SoftwareComponent',
                                'properties': {'context_root': {'type': 'string', 'required': False}}, 'requirements': [
                                    {'host': {'capability': 'tosca.capabilities.Container',
                                              'node': 'tosca.nodes.WebServer',
                                              'relationship': 'tosca.relationships.HostedOn'}}],
                                'capabilities': {'app_endpoint': {'type': 'tosca.capabilities.Endpoint'}}},
                            'tosca.nodes.DBMS': {
                                'description': 'The TOSCA DBMS node represents a typical relational, SQL Database Management System software component or service.\n',
                                'derived_from': 'tosca.nodes.SoftwareComponent', 'properties': {
                                    'port': {'required': False, 'type': 'integer',
                                             'description': 'The port the DBMS service will listen to for data and requests.\n'},
                                    'root_password': {'required': False, 'type': 'string',
                                                      'description': 'The root password for the DBMS service.\n'}},
                                'capabilities': {'host': {'type': 'tosca.capabilities.Container',
                                                          'valid_source_types': ['tosca.nodes.Database']}}},
                            'tosca.nodes.Database': {
                                'description': 'The TOSCA Database node represents a logical database that can be managed and hosted by a TOSCA DBMS node.\n',
                                'derived_from': 'tosca.nodes.Root', 'properties': {
                                    'user': {'required': False, 'type': 'string',
                                             'description': 'User account name for DB administration\n'},
                                    'port': {'required': False, 'type': 'integer',
                                             'description': 'The port the database service will use to listen for incoming data and requests.\n'},
                                    'name': {'required': True, 'type': 'string',
                                             'description': 'The logical name of the database.\n'},
                                    'password': {'required': False, 'type': 'string',
                                                 'description': 'The password for the DB user account\n'}},
                                'requirements': [{'host': {'capability': 'tosca.capabilities.Container',
                                                           'node': 'tosca.nodes.DBMS',
                                                           'relationship': 'tosca.relationships.HostedOn'}}],
                                'capabilities': {
                                    'database_endpoint': {'type': 'tosca.capabilities.Endpoint.Database'}}},
                            'tosca.nodes.ObjectStorage': {
                                'description': 'The TOSCA ObjectStorage node represents storage that provides the ability to store data as objects (or BLOBs of data) without consideration for the underlying filesystem or devices\n',
                                'derived_from': 'tosca.nodes.Root', 'properties': {
                                    'name': {'type': 'string', 'required': True,
                                             'description': 'The logical name of the object store (or container).\n'},
                                    'size': {'type': 'scalar-unit.size', 'required': False,
                                             'constraints': [{'greater_or_equal': '0 GB'}],
                                             'description': 'The requested initial storage size.\n'},
                                    'maxsize': {'type': 'scalar-unit.size', 'required': False,
                                                'constraints': [{'greater_or_equal': '0 GB'}],
                                                'description': 'The requested maximum storage size.\n'}},
                                'capabilities': {'storage_endpoint': {'type': 'tosca.capabilities.Endpoint'}}},
                            'tosca.nodes.BlockStorage': {
                                'description': 'The TOSCA BlockStorage node currently represents a server-local block storage device (i.e., not shared) offering evenly sized blocks of data from which raw storage volumes can be created.\n',
                                'derived_from': 'tosca.nodes.Root', 'properties': {
                                    'size': {'type': 'scalar-unit.size', 'constraints': [{'greater_or_equal': '1 MB'}]},
                                    'volume_id': {'type': 'string', 'required': False},
                                    'snapshot_id': {'type': 'string', 'required': False}},
                                'capabilities': {'attachment': {'type': 'tosca.capabilities.Attachment'}}},
                            'tosca.nodes.Container.Runtime': {
                                'description': 'The TOSCA Container Runtime node represents operating system-level virtualization technology used to run multiple application services on a single Compute host.\n',
                                'derived_from': 'tosca.nodes.SoftwareComponent',
                                'capabilities': {'host': {'type': 'tosca.capabilities.Container'},
                                                 'scalable': {'type': 'tosca.capabilities.Scalable'}}},
                            'tosca.nodes.Container.Application': {
                                'description': 'The TOSCA Container Application node represents an application that requires Container-level virtualization technology.\n',
                                'derived_from': 'tosca.nodes.Root', 'requirements': [{'host': {
                                    'capability': 'tosca.capabilities.Container',
                                    'node': 'tosca.nodes.Container.Runtime',
                                    'relationship': 'tosca.relationships.HostedOn'}}]}, 'tosca.nodes.LoadBalancer': {
                     'description': 'The TOSCA Load Balancer node represents logical function that be used in conjunction with a Floating Address to distribute an application’s traffic (load) across a number of instances of the application (e.g., for a clustered or scaled application).\n',
                     'derived_from': 'tosca.nodes.Root',
                     'properties': {'algorithm': {'type': 'string', 'required': False, 'status': 'experimental'}},
                     'capabilities': {
                         'client': {'type': 'tosca.capabilities.Endpoint.Public', 'occurrences': [0, 'UNBOUNDED'],
                                    'description': 'the Floating (IP) client’s on the public network can connect to'}},
                     'requirements': [{'application': {'capability': 'tosca.capabilities.Endpoint',
                                                       'relationship': 'tosca.relationships.RoutesTo',
                                                       'occurrences': [0, 'UNBOUNDED']}}]},
                            'tosca.nodes.network.Network': {'derived_from': 'tosca.nodes.Root',
                                                            'description': 'The TOSCA Network node represents a simple, logical network service.\n',
                                                            'properties': {
                                                                'ip_version': {'type': 'integer', 'required': False,
                                                                               'default': 4, 'constraints': [
                                                                        {'valid_values': [4, 6]}],
                                                                               'description': 'The IP version of the requested network. Valid values are 4 for ipv4 or 6 for ipv6.\n'},
                                                                'cidr': {'type': 'string', 'required': False,
                                                                         'description': 'The cidr block of the requested network.\n'},
                                                                'start_ip': {'type': 'string', 'required': False,
                                                                             'description': 'The IP address to be used as the start of a pool of addresses within the full IP range derived from the cidr block.\n'},
                                                                'end_ip': {'type': 'string', 'required': False,
                                                                           'description': 'The IP address to be used as the end of a pool of addresses within the full IP range derived from the cidr block.\n'},
                                                                'gateway_ip': {'type': 'string', 'required': False,
                                                                               'description': 'The gateway IP address.\n'},
                                                                'network_name': {'type': 'string', 'required': False,
                                                                                 'description': 'An identifier that represents an existing Network instance in the underlying cloud infrastructure or can be used as the name of the newly created network. If network_name is provided and no other properties are provided (with exception of network_id), then an existing network instance will be used. If network_name is provided alongside with more properties then a new network with this name will be created.\n'},
                                                                'network_id': {'type': 'string', 'required': False,
                                                                               'description': 'An identifier that represents an existing Network instance in the underlying cloud infrastructure. This property is mutually exclusive with all other properties except network_name. This can be used alone or together with network_name to identify an existing network.\n'},
                                                                'segmentation_id': {'type': 'string', 'required': False,
                                                                                    'description': 'A segmentation identifier in the underlying cloud infrastructure. E.g. VLAN ID, GRE tunnel ID, etc..\n'},
                                                                'network_type': {'type': 'string', 'required': False,
                                                                                 'description': 'It specifies the nature of the physical network in the underlying cloud infrastructure. Examples are flat, vlan, gre or vxlan. For flat and vlan types, physical_network should be provided too.\n'},
                                                                'physical_network': {'type': 'string',
                                                                                     'required': False,
                                                                                     'description': 'It identifies the physical network on top of which the network is implemented, e.g. physnet1. This property is required if network_type is flat or vlan.\n'},
                                                                'dhcp_enabled': {'type': 'boolean', 'required': False,
                                                                                 'default': True,
                                                                                 'description': 'Indicates should DHCP service be enabled on the network or not.\n'}},
                                                            'capabilities': {'link': {
                                                                'type': 'tosca.capabilities.network.Linkable'}}},
                            'tosca.nodes.network.Port': {'derived_from': 'tosca.nodes.Root',
                                                         'description': 'The TOSCA Port node represents a logical entity that associates between Compute and Network normative types. The Port node type effectively represents a single virtual NIC on the Compute node instance.\n',
                                                         'properties': {
                                                             'ip_address': {'type': 'string', 'required': False,
                                                                            'description': 'Allow the user to set a static IP.\n'},
                                                             'order': {'type': 'integer', 'required': False,
                                                                       'default': 0,
                                                                       'constraints': [{'greater_or_equal': 0}],
                                                                       'description': 'The order of the NIC on the compute instance (e.g. eth2).\n'},
                                                             'is_default': {'type': 'boolean', 'required': False,
                                                                            'default': False,
                                                                            'description': 'If is_default=true this port will be used for the default gateway route. Only one port that is associated to single compute node can set as is_default=true.\n'},
                                                             'ip_range_start': {'type': 'string', 'required': False,
                                                                                'description': 'Defines the starting IP of a range to be allocated for the compute instances that are associated with this Port.\n'},
                                                             'ip_range_end': {'type': 'string', 'required': False,
                                                                              'description': 'Defines the ending IP of a range to be allocated for the compute instances that are associated with this Port.\n'}},
                                                         'requirements': [{'binding': {
                                                             'capability': 'tosca.capabilities.network.Bindable',
                                                             'relationship': 'tosca.relationships.network.BindsTo'}}, {
                                                                              'link': {
                                                                                  'capability': 'tosca.capabilities.network.Linkable',
                                                                                  'relationship': 'tosca.relationships.network.LinksTo'}}]}},
             'relationship_types': {'tosca.relationships.Root': {
                 'description': 'The TOSCA root Relationship Type all other TOSCA base Relationship Types derive from.\n',
                 'attributes': {'tosca_id': {'type': 'string'}, 'state': {'type': 'string'}},
                 'properties': {'tosca_name': {'type': 'string', 'required': True}},
                 'interfaces': {'Configure': {'type': 'tosca.interfaces.relationship.Configure'}}},
                                    'tosca.relationships.DependsOn': {
                                        'description': 'This type represents a general dependency relationship between two nodes.',
                                        'derived_from': 'tosca.relationships.Root',
                                        'valid_target_types': ['tosca.capabilities.Node']},
                                    'tosca.relationships.HostedOn': {
                                        'description': 'This type represents a hosting relationship between two nodes.',
                                        'derived_from': 'tosca.relationships.Root',
                                        'valid_target_types': ['tosca.capabilities.Container']},
                                    'tosca.relationships.ConnectsTo': {
                                        'description': 'This type represents a network connection relationship between two nodes.',
                                        'derived_from': 'tosca.relationships.Root',
                                        'valid_target_types': ['tosca.capabilities.Endpoint'], 'properties': {
                                            'credential': {'type': 'tosca.datatypes.Credential', 'required': False}}},
                                    'tosca.relationships.AttachesTo': {
                                        'description': 'This type represents an attachment relationship between two nodes. For example, an AttachesTo relationship type would be used for attaching a storage node to a Compute node.\n',
                                        'derived_from': 'tosca.relationships.Root',
                                        'valid_target_types': ['tosca.capabilities.Attachment'], 'properties': {
                                            'location': {'required': True, 'type': 'string',
                                                         'constraints': [{'min_length': 1}]},
                                            'device': {'required': False, 'type': 'string'}}},
                                    'tosca.relationships.RoutesTo': {
                                        'description': 'This type represents an intentional network routing between two Endpoints in different networks.',
                                        'derived_from': 'tosca.relationships.ConnectsTo',
                                        'valid_target_types': ['tosca.capabilities.Endpoint']},
                                    'tosca.relationships.network.LinksTo': {
                                        'description': 'This relationship type represents an association relationship between Port and Network node types.',
                                        'derived_from': 'tosca.relationships.DependsOn',
                                        'valid_target_types': ['tosca.capabilities.network.Linkable']},
                                    'tosca.relationships.network.BindsTo': {
                                        'description': 'This type represents a network association relationship between Port and Compute node types.',
                                        'derived_from': 'tosca.relationships.DependsOn',
                                        'valid_target_types': ['tosca.capabilities.network.Bindable']}},
             'capability_types': {'tosca.capabilities.Root': {
                 'description': 'The TOSCA root Capability Type all other TOSCA base Capability Types derive from.\n'},
                                  'tosca.capabilities.Node': {
                                      'description': 'The Node capability indicates the base capabilities of a TOSCA Node Type.',
                                      'derived_from': 'tosca.capabilities.Root'}, 'tosca.capabilities.Container': {
                     'description': 'The Container capability, when included on a Node Type or Template definition, indicates that the node can act as a container for (or a host for) one or more other declared Node Types.\n',
                     'derived_from': 'tosca.capabilities.Root', 'properties': {
                         'num_cpus': {'required': False, 'type': 'integer', 'constraints': [{'greater_or_equal': 1}]},
                         'cpu_frequency': {'required': False, 'type': 'scalar-unit.frequency',
                                           'constraints': [{'greater_or_equal': '0.1 GHz'}]},
                         'disk_size': {'required': False, 'type': 'scalar-unit.size',
                                       'constraints': [{'greater_or_equal': '0 MB'}]},
                         'mem_size': {'required': False, 'type': 'scalar-unit.size',
                                      'constraints': [{'greater_or_equal': '0 MB'}]}}}, 'tosca.capabilities.Endpoint': {
                     'description': 'This is the default TOSCA type that should be used or extended to define a network endpoint capability. This includes the information to express a basic endpoint with a single port or a complex endpoint with multiple ports. By default the Endpoint is assumed to represent an address on a private network unless otherwise specified.\n',
                     'derived_from': 'tosca.capabilities.Root',
                     'properties': {'protocol': {'type': 'string', 'required': True, 'default': 'tcp'},
                                    'port': {'type': 'tosca.datatypes.network.PortDef', 'required': False},
                                    'secure': {'type': 'boolean', 'required': False, 'default': False},
                                    'url_path': {'type': 'string', 'required': False},
                                    'port_name': {'type': 'string', 'required': False},
                                    'network_name': {'type': 'string', 'required': False, 'default': 'PRIVATE'},
                                    'initiator': {'type': 'string', 'required': False, 'default': 'source',
                                                  'constraints': [{'valid_values': ['source', 'target', 'peer']}]},
                                    'ports': {'type': 'map', 'required': False, 'constraints': [{'min_length': 1}],
                                              'entry_schema': {'type': 'tosca.datatypes.network.PortSpec'}},
                                    'ip_address': {'type': 'string', 'default': '0.0.0.0/0'}}},
                                  'tosca.capabilities.Endpoint.Admin': {
                                      'description': 'This is the default TOSCA type that should be used or extended to define a specialized administrator endpoint capability.\n',
                                      'derived_from': 'tosca.capabilities.Endpoint', 'properties': {
                                          'secure': {'type': 'boolean', 'default': True, 'required': False,
                                                     'constraints': [{'equal': True}]}}},
                                  'tosca.capabilities.Endpoint.Public': {
                                      'description': 'This capability represents a public endpoint which is accessible to the general internet (and its public IP address ranges).\n',
                                      'derived_from': 'tosca.capabilities.Endpoint', 'properties': {
                                          'network_name': {'type': 'string', 'default': 'PUBLIC', 'required': False,
                                                           'constraints': [{'equal': 'PUBLIC'}]}, 'floating': {
                                              'description': 'Indicates that the public address should be allocated from a pool of floating IPs that are associated with the network.\n',
                                              'type': 'boolean', 'default': False, 'status': 'experimental',
                                              'required': False},
                                          'dns_name': {'description': 'The optional name to register with DNS',
                                                       'type': 'string', 'required': False, 'status': 'experimental'}}},
                                  'tosca.capabilities.Endpoint.Database': {
                                      'derived_from': 'tosca.capabilities.Endpoint'}, 'tosca.capabilities.Attachment': {
                     'description': 'This is the default TOSCA type that should be used or extended to define an attachment capability of a (logical) infrastructure device node (e.g., BlockStorage node)\n',
                     'derived_from': 'tosca.capabilities.Root'},
                                  'tosca.capabilities.OperatingSystem': {'derived_from': 'tosca.capabilities.Root',
                                                                         'properties': {
                                                                             'architecture': {'required': False,
                                                                                              'type': 'string',
                                                                                              'description': 'The host Operating System (OS) architecture.\n'},
                                                                             'type': {'required': False,
                                                                                      'type': 'string',
                                                                                      'description': 'The host Operating System (OS) type.\n'},
                                                                             'distribution': {'required': False,
                                                                                              'type': 'string',
                                                                                              'description': 'The host Operating System (OS) distribution. Examples of valid values for an “type” of “Linux” would include: debian, fedora, rhel and ubuntu.\n'},
                                                                             'version': {'required': False,
                                                                                         'type': 'version',
                                                                                         'description': 'The host Operating System version.\n'}}},
                                  'tosca.capabilities.Scalable': {'derived_from': 'tosca.capabilities.Root',
                                                                  'properties': {'min_instances': {'type': 'integer',
                                                                                                   'required': True,
                                                                                                   'default': 1,
                                                                                                   'description': 'This property is used to indicate the minimum number of instances that should be created for the associated TOSCA Node Template by a TOSCA orchestrator.\n'},
                                                                                 'max_instances': {'type': 'integer',
                                                                                                   'required': True,
                                                                                                   'default': 1,
                                                                                                   'description': 'This property is used to indicate the maximum number of instances that should be created for the associated TOSCA Node Template by a TOSCA orchestrator.\n'},
                                                                                 'default_instances': {
                                                                                     'type': 'integer',
                                                                                     'required': False,
                                                                                     'description': 'An optional property that indicates the requested default number of instances that should be the starting number of instances a TOSCA orchestrator should attempt to allocate. The value for this property MUST be in the range between the values set for min_instances and max_instances properties.\n'}}},
                                  'tosca.capabilities.network.Linkable': {'derived_from': 'tosca.capabilities.Node',
                                                                          'description': 'A node type that includes the Linkable capability indicates that it can be pointed by tosca.relationships.network.LinksTo relationship type, which represents an association relationship between Port and Network node types.\n'},
                                  'tosca.capabilities.network.Bindable': {'derived_from': 'tosca.capabilities.Node',
                                                                          'description': 'A node type that includes the Bindable capability indicates that it can be pointed by tosca.relationships.network.BindsTo relationship type, which represents a network association relationship between Port and Compute node types.\n'}},
             'interface_types': {'tosca.interfaces.Root': {
                 'description': 'The TOSCA root Interface Type all other TOSCA base Interface Types derive from\n'},
                                 'tosca.interfaces.node.lifecycle.Standard': {
                                     'description': 'This lifecycle interface defines the essential, normative operations that TOSCA nodes may support.',
                                     'derived_from': 'tosca.interfaces.Root',
                                     'create': {'description': 'Standard lifecycle create operation.'},
                                     'configure': {'description': 'Standard lifecycle configure operation.'},
                                     'start': {'description': 'Standard lifecycle start operation.'},
                                     'stop': {'description': 'Standard lifecycle stop operation.'},
                                     'delete': {'description': 'Standard lifecycle delete operation.'}},
                                 'tosca.interfaces.relationship.Configure': {
                                     'description': 'The lifecycle interfaces define the essential, normative operations that each TOSCA Relationship Types may support.\n',
                                     'derived_from': 'tosca.interfaces.Root', 'pre_configure_source': {
                                         'description': 'Operation to pre-configure the source endpoint.'},
                                     'pre_configure_target': {
                                         'description': 'Operation to pre-configure the target endpoint.'},
                                     'post_configure_source': {
                                         'description': 'Operation to post-configure the source endpoint.'},
                                     'post_configure_target': {
                                         'description': 'Operation to post-configure the target endpoint.'},
                                     'add_target': {'description': 'Operation to add a target node.'},
                                     'remove_target': {'description': 'Operation to remove a target node.'},
                                     'add_source': {
                                         'description': 'Operation to notify the target node of a source node which is now available via a relationship.\n'},
                                     'target_changed': {
                                         'description': 'Operation to notify source some property or attribute of the target changed\n'}}},
             'artifact_types': {'tosca.artifacts.Root': {
                 'description': 'The TOSCA Artifact Type all other TOSCA Artifact Types derive from\n',
                 'properties': {'version': {'type': 'version', 'required': False}}},
                                'tosca.artifacts.File': {'derived_from': 'tosca.artifacts.Root'},
                                'tosca.artifacts.Deployment': {'derived_from': 'tosca.artifacts.Root',
                                                               'description': 'TOSCA base type for deployment artifacts'},
                                'tosca.artifacts.Deployment.Image': {'derived_from': 'tosca.artifacts.Deployment'},
                                'tosca.artifacts.Deployment.Image.VM': {
                                    'derived_from': 'tosca.artifacts.Deployment.Image'},
                                'tosca.artifacts.Implementation': {'derived_from': 'tosca.artifacts.Root',
                                                                   'description': 'TOSCA base type for implementation artifacts'},
                                'tosca.artifacts.Implementation.Bash': {
                                    'derived_from': 'tosca.artifacts.Implementation',
                                    'description': 'Script artifact for the Unix Bash shell',
                                    'mime_type': 'application/x-sh', 'file_ext': ['sh']},
                                'tosca.artifacts.Implementation.Python': {
                                    'derived_from': 'tosca.artifacts.Implementation',
                                    'description': 'Artifact for the interpreted Python language',
                                    'mime_type': 'application/x-python', 'file_ext': ['py']}}, 'policy_types': {
        'tosca.policies.Root': {'description': 'The TOSCA Policy Type all other TOSCA Policy Types derive from.'},
        'tosca.policies.Placement': {'derived_from': 'tosca.policies.Root',
                                     'description': 'The TOSCA Policy Type definition that is used to govern placement of TOSCA nodes or groups of nodes.'},
        'tosca.policies.Scaling': {'derived_from': 'tosca.policies.Root',
                                   'description': 'The TOSCA Policy Type definition that is used to govern scaling of TOSCA nodes or groups of nodes.'},
        'tosca.policies.Update': {'derived_from': 'tosca.policies.Root',
                                  'description': 'The TOSCA Policy Type definition that is used to govern update of TOSCA nodes or groups of nodes.'},
        'tosca.policies.Performance': {'derived_from': 'tosca.policies.Root',
                                       'description': 'The TOSCA Policy Type definition that is used to declare performance requirements for TOSCA nodes or groups of nodes.'}},
             'group_types': {
                 'tosca.groups.Root': {'description': 'The TOSCA Group Type all other TOSCA Group Types derive from',
                                       'interfaces': {
                                           'Standard': {'type': 'tosca.interfaces.node.lifecycle.Standard'}}}}}
