import subprocess as sp
import yaml
# from parse_puccini import *


def puccini_parse(file, phases=5):
    PUCCINI_CMD = '/home/tulin/go/bin/puccini-tosca compile --resolve=False'
    pipe = sp.Popen(
        f'{PUCCINI_CMD} -x namespace.normative.shortcuts.disable',
        shell=True,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        stdin=sp.PIPE
    )
    res = pipe.communicate(file)

    if pipe.returncode != 0:
        raise RuntimeError(res[1].decode())

    return yaml.safe_load(res[0])

# test = puccini_parse("""tosca_definitions_version: tosca_simple_yaml_1_3
#
#
#
# description: >
#
#   TOSCA simple profile with WordPress, a web server, a MySQL DBMS hosting the application’s database content on the same server. Does not have input defaults or constraints.
#
#
# node_types:
#     tosca.nodes.WebApplication.WordPress:
#
#       derived_from: tosca.nodes.WebApplication
#
#       properties:
#
#         admin_user:
#
#           type: string
#
#           required: False
#
#         admin_password:
#
#           type: string
#
#           required: False
#
#         db_host:
#
#           type: string
#           required: False
#
#       requirements:
#
#         - database_endpoint:
#
#             capability: tosca.capabilities.Endpoint.Database
#
#             node: tosca.nodes.Database
#
#             relationship: tosca.relationships.ConnectsTo
# metadata: {abra: KADABRA}
# topology_template:
#
#   inputs:
#
#     cpus:
#
#       type: integer
#
#       description: Number of CPUs for the server.
#
#       value: 10
#
#       default: 1
#
#     db_name:
#
#       type: string
#
#       description: The name of the database.
#
#       default: default name
#
#     db_user:
#
#       type: string
#
#       description: The username of the DB user.
#
#       default: user
#
#     db_pwd:
#
#       type: string
#
#       description: The WordPress database admin account password.
#
#       default: password
#
#     db_root_pwd:
#
#       type: string
#
#       description: Root password for MySQL.
#
#       default: password
#
#     db_port:
#
#       type: tosca.datatypes.network.PortDef
#
#       description: Port for the MySQL database
#
#       default: 4000
#
#
#
#   node_templates:
#
#     wordpress:
#
#       type: tosca.nodes.WebApplication.WordPress
#
#       properties:
#
#         context_root: hello
#
#       requirements:
#
#         - host: webserver
#
#         - database_endpoint: mysql_database
#
#       interfaces:
#
#         Standard:
#
#           operations:
#
#               create: wordpress_install.sh
#
#               configure:
#
#                 implementation: wordpress_configure.sh
#
#                 inputs:
#
#                   wp_db_name: { get_property: [ mysql_database, name ] }
#
#                   wp_db_user: { get_property: [ mysql_database, user ] }
#
#                   wp_db_password: { get_property: [ mysql_database, password ] }
#
#                   # In my own template, find requirement/capability, find port property
#
#                   wp_db_port: { get_property: [ SELF, database_endpoint, port ] }
#
#
#
#     mysql_database:
#
#       type: tosca.nodes.Database
#
#       properties:
#
#         name: { get_input: db_name }
#
#         user: { get_input: db_user }
#
#         password: { get_input: db_pwd }
#
#         port: { get_input: db_port }
#
#       capabilities:
#
#         database_endpoint:
#
#           properties:
#
#             port: { get_input: db_port }
#
#       requirements:
#
#         - host: mysql_dbms
#
#       interfaces:
#
#         Standard:
#           inputs:
#             abra: {get_attribute: [SELF, name]}
#           operations:
#             configure: mysql_database_configure.sh
#
#
#
#
#     mysql_dbms:
#
#       type: tosca.nodes.DBMS
#
#       properties:
#
#         root_password: { get_input: db_root_pwd }
#
#         port: { get_input: db_port }
#
#       requirements:
#
#         - host: server
#
#       interfaces:
#
#         Standard:
#
#           inputs:
#
#               db_root_password: { get_property: [ mysql_dbms, root_password ] }
#
#           operations:
#               create: mysql_dbms_install.sh
#
#               start: mysql_dbms_start.sh
#
#               configure: mysql_dbms_configure.sh
#
#
#
#     webserver:
#
#       type: tosca.nodes.WebServer
#
#       requirements:
#
#         - host: server
#
#       interfaces:
#
#         Standard:
#
#             operations:
#
#               create: webserver_install.sh
#
#               start: webserver_start.sh
#
#
#
#     server:
#
#       type: tosca.nodes.Compute
#
#       capabilities:
#
#         host:
#
#           properties:
#
#             disk_size: 10 GB
#
#             num_cpus: { get_input: cpus }
#
#             mem_size: 4096 MB
#
#         os:
#
#           properties:
#
#             architecture: x86_64
#
#             type: linux
#
#             distribution: fedora
#
#             version: "17.0"
#
#
#
#   outputs:
#
#     website_url:
#
#       description: URL for Wordpress wiki.
#
#       value: { get_attribute: [server, public_address] }
# """.encode("utf-8"))
# topology = TopologyTemplateInstance("ABRA", test)
# print(yaml.dump(topology.render()))
