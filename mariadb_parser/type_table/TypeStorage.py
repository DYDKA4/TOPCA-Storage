import json

import yaml


class TOSCAType:
    def __init__(self, identifier: int, name: str, data: dict, type_of_type: str, version: str = None):
        self.identifier = identifier
        self.name = name
        self.type_of_type: str = type_of_type
        self.version: str = version
        self.data = data
        self.derived_from: set[str] = set()
        self.derived_from_id: set[int] = set()
        self.dependencies: dict[str, set] = {'data_types': set(),
                                             'artifact_types': set(),
                                             'capability_types': set(),
                                             'interface_types': set(),
                                             'relationship_types': set(),
                                             'node_types': set(),
                                             'group_types': set(),
                                             'policy_types': set(),
                                             'artifacts': set()}

    def convert_data_to_json(self):
        self.data = json.dumps(self.data)


class DataType(TOSCAType):
    """
    Data Type Class storage parsed data of Data Type from yaml file. And prepare data to upload to SQL database
    identifier storage id of Data Type in SQL database
    name storage name of Data Type from yaml file
    data storage unparsed json of Data Type
    version storage version of Data Type, by default it set to 1.0.0 if this version is not occupied by anyone
    DataType(0, 'test_name', {'data': 'value'}, '1.0.0')
    """

    # TODO поиграть с наследованием
    def __init__(self, identifier: int, name: str, data: dict, version: str = ''):
        super().__init__(identifier, name, data, 'data_type', version=version)


class ArtifactType(TOSCAType):

    def __init__(self, identifier: int, name: str, data: dict, version: str = ''):
        super().__init__(identifier, name, data, 'artifact_type', version=version)


class InterfaceType(TOSCAType):
    def __init__(self, identifier: int, name: str, data: dict, version: str = ''):
        super().__init__(identifier, name, data, 'interface_type', version=version)


class NodeType(TOSCAType):
    def __init__(self, identifier: int, name: str, data: dict, version: str = ''):
        super().__init__(identifier, name, data, 'node_type', version=version)


class GroupType(TOSCAType):
    def __init__(self, identifier: int, name: str, data: dict, version: str = ''):
        super().__init__(identifier, name, data, 'group_type', version=version)


class PolicyType(TOSCAType):
    def __init__(self, identifier: int, name: str, data: dict, version: str = ''):
        super().__init__(identifier, name, data, 'policy_type', version=version)


class CapabilityType(TOSCAType):
    def __init__(self, identifier: int, name: str, data: dict, version: str = ''):
        super().__init__(identifier, name, data, 'capability_type', version=version)


class RelationshipType(TOSCAType):
    def __init__(self, identifier: int, name: str, data: dict, version: str = ''):
        super().__init__(identifier, name, data, 'relationship_type', version=version)


class ArtifactDefinition:
    def __init__(self, name: str, value: dict, father_node):
        self.name = name
        self.value = value
        self.father_node = father_node


class TypeStorage:
    """
    TypeStorage class parse part of yaml file with type definition and prepare it to submit it into SQL database
    it consists of:
        data_types where stored dict where keys are name of DataType and value is DataType object
    """

    def __init__(self, data: dict):
        self.data = data
        self.data_types: dict[str, DataType] = {}
        self.artifact_types: dict[str, ArtifactType] = {}
        self.capability_types: dict[str, CapabilityType] = {}
        self.interface_types: dict[str, InterfaceType] = {}
        self.relationship_types: dict[str, RelationshipType] = {}
        self.node_types: dict[str, NodeType] = {}
        self.group_types: dict[str, GroupType] = {}
        self.policy_types: dict[str, PolicyType] = {}
        self.artifact_definition: dict[str, ArtifactDefinition] = {}
        if data.get('data_types'):
            self.data_types = self.prepare_data_types(data.get('data_types'))
            # TODO ADD DERIVED FROM FINDER
        if data.get('capability_types'):
            self.capability_types = self.prepare_capability_types(data.get('capability_types'))
            # TODO ADD DERIVED FROM FINDER
        if data.get('artifact_types'):
            self.artifact_types = self.prepare_artifact_types(data.get('artifact_types'))
            # TODO ADD DERIVED FROM FINDER
        if data.get('interface_types'):
            self.interface_types = self.prepare_interface_types(data.get('interface_types'))
            # TODO ADD DERIVED FROM FINDER
        if data.get('relationship_types'):
            self.relationship_types = self.prepare_relationship_types(data.get('relationship_types'))
            # TODO ADD DERIVED FROM FINDER
        if data.get('node_types'):
            self.node_types = self.prepare_node_types(data.get('node_types'))
            # TODO ADD DERIVED FROM FINDER
        if data.get('group_types'):
            self.group_types = self.prepare_group_types(data.get('group_types'))
            # TODO ADD DERIVED FROM FINDER
        if data.get('policy_types'):
            self.policy_types = self.prepare_policy_types(data.get('policy_types'))

    def identifier_generator(self) -> int:
        return len(self.data_types) + \
               len(self.artifact_types) + \
               len(self.capability_types) + \
               len(self.interface_types) + \
               len(self.relationship_types) + \
               len(self.node_types) + \
               len(self.group_types) + \
               len(self.policy_types)

    def prepare_data_types(self, data) -> dict[str, DataType]:
        """
        This function make first representation of DataTypes
        :param data:
        :return dict of str and DataType:
        """
        data_types = {}
        # NOTE can be parallelized
        for name, data in data.items():
            derived_from = data.get('derived_from')
            version = data.get('version')
            data_type = DataType(self.identifier_generator(), name, data, version)
            data_type.dependencies['data_types'] = data_type.dependencies['data_types'].union(
                self.check_schema_in_entity(data, data_type.dependencies['data_types']))
            data_type.dependencies['data_types'] = data_type.dependencies['data_types'].union(
                self.check_property_in_entity(data, data_type.dependencies['data_types']))
            if derived_from:
                data_type.derived_from.add(derived_from)
            data_types[name] = data_type
        return data_types

    def prepare_capability_types(self, data: dict) -> dict[str, CapabilityType]:
        capability_types = {}
        for name, data in data.items():
            derived_from = data.get('derived_from')
            version = data.get('version')
            capability_type = CapabilityType(self.identifier_generator(), name, data, version)
            capability_type.dependencies['data_types'] = capability_type.dependencies['data_types'].union(
                self.check_property_in_entity(data, capability_type.dependencies['data_types']))
            capability_type.dependencies['data_types'] = capability_type.dependencies['data_types'].union(
                self.check_property_in_entity(data, capability_type.dependencies['data_types'], key_name='attributes'))
            valid_source_types = data.get('valid_source_types')
            if valid_source_types:
                for node_type_name in valid_source_types:
                    capability_type.dependencies['node_types'].add(node_type_name)
            if derived_from:
                capability_type.derived_from.add(derived_from)
            capability_types[name] = capability_type
        return capability_types

    def prepare_artifact_types(self, data: dict) -> dict[str, ArtifactType]:
        artifact_types = {}
        for name, data in data.items():
            derived_from = data.get('derived_from')
            version = data.get('version')
            artifact_type = ArtifactType(self.identifier_generator(), name, data, version)
            artifact_type.dependencies['data_types'] = artifact_type.dependencies['data_types'].union(
                self.check_property_in_entity(data, artifact_type.dependencies['data_types']))
            if derived_from:
                artifact_type.derived_from.add(derived_from)
            artifact_types[name] = artifact_type
        return artifact_types

    def prepare_interface_types(self, data: dict) -> dict[str, InterfaceType]:
        interface_types = {}
        for name, data in data.items():
            derived_from = data.get('derived_from')
            version = data.get('version')
            interface_type = InterfaceType(self.identifier_generator(), name, data, version)
            interface_type.dependencies['data_types'] = interface_type.dependencies['data_types'].union(
                self.check_property_in_entity(data, interface_type.dependencies['data_types']))
            if derived_from:
                interface_type.derived_from.add(derived_from)
            interface_types[name] = interface_type
        return interface_types

    def prepare_relationship_types(self, data: dict) -> dict[str, RelationshipType]:
        relationship_types = {}
        for name, data in data.items():
            derived_from = data.get('derived_from')
            version = data.get('version')
            relationship_type = RelationshipType(self.identifier_generator(), name, data, version)
            relationship_type.dependencies['data_types'] = relationship_type.dependencies['data_types'].union(
                self.check_property_in_entity(data, relationship_type.dependencies['data_types'])
            )
            relationship_type.dependencies['data_types'] = relationship_type.dependencies['data_types'].union(
                self.check_property_in_entity(data, relationship_type.dependencies['data_types'], key_name='attributes')
            )
            interface_types, data_types, artifacts, artifacts_types = self.check_interface_in_entity(data,
                                                                                                     relationship_type)
            relationship_type.dependencies['interface_types'] = interface_types
            relationship_type.dependencies['data_types'] = \
                relationship_type.dependencies['data_types'].union(data_types)
            relationship_type.dependencies['artifacts'].update(artifacts)
            relationship_type.dependencies['artifacts_types'].update(artifacts_types)
            valid_target_types = data.get('valid_target_types')
            if valid_target_types:
                if type(valid_target_types) != list:
                    raise f"valid_target_types is not list in relationship_type, name:{name}"
                relationship_type.dependencies['capability_types'].update(valid_target_types)
            if derived_from:
                relationship_type.derived_from.add(derived_from)
            relationship_types[name] = relationship_type
        return relationship_types

    def prepare_node_types(self, data: dict) -> dict[str, NodeType]:
        node_types = {}
        for name, data in data.items():
            derived_from = data.get('derived_from')
            version = data.get('version')
            node_type = NodeType(self.identifier_generator(), name, data, version)
            node_type.dependencies['data_types'].update(
                self.check_property_in_entity(data, node_type.dependencies['data_types']))
            node_type.dependencies['data_type'].update(
                self.check_property_in_entity(data, node_type.dependencies['data_types'], key_name='attributes'))
            interface_types, data_types, artifacts, artifacts_types = self.check_interface_in_entity(data,
                                                                                                     node_type)
            node_type.dependencies['interface_types'].update(interface_types)
            node_type.dependencies['data_types'].update(data_types)
            node_type.dependencies['artifacts'].update(artifacts)
            node_type.dependencies['artifact_types'].update(artifacts_types)
            # NOTE CAPABILITY DEFINITION
            capability_definition = data.get('capabilities')
            if capability_definition:
                for capability_name, capability_data in capability_definition.items():
                    if type(capability_data) == str:
                        node_type.dependencies['capability_types'].add(capability_data)
                    else:
                        capability_type = capability_data.get('type')
                        if capability_type is None:
                            raise f"In capability {capability_name} in node_type {name} no type"
                        node_type.dependencies['capability_types'].add(capability_type)
                        node_type.dependencies['data_types'].update(
                            self.check_property_in_entity(capability_data, node_type.dependencies['data_types']))
                        node_type.dependencies['data_types'].update(
                            self.check_property_in_entity(capability_data, node_type.dependencies['data_types'],
                                                          key_name='attributes'))
                        valid_source_types = capability_data.get('valid_source_types')
                        if valid_source_types:
                            node_type.dependencies['node_types'].update(valid_source_types)
            # NOTE ARTIFACT DEFINITION
            artifact_definition = data.get('artifacts')
            if artifact_definition:
                for artifact_name, artifact_value in artifact_definition.items():
                    if type(artifact_value) == str:
                        artifact = ArtifactDefinition(artifact_name, artifact_value, node_type)
                        self.artifact_definition[artifact_name] = artifact
                    else:
                        artifact_type = artifact_value.get('type')
                        if artifact_type is None:
                            raise f"In artifact definition {artifact_name}, " \
                                  f"in node_type {name} artifact type is missing"
                        node_type.dependencies['artifact_types'].add(artifact_type)
                        artifact = ArtifactDefinition(artifact_name, artifact_value, node_type)
                        self.artifact_definition[artifact_name] = artifact
            # NOTE REQUIREMENT DEFINITION
            requirement_definitions = data.get('requirements')
            if requirement_definitions:
                for requirement_definition in requirement_definitions:
                    if type(requirement_definition) != dict:
                        raise f"Wrong type of entity in requirements in node_type {name}"
                    elif len(requirement_definition) > 1:
                        raise f"Requirement definition dict is too long in node_type {name}"
                    else:
                        for requirement_name, requirement_data in requirement_definition.items():
                            if type(requirement_data) == str:
                                node_type.dependencies['capability_types'].add(requirement_data)
                            else:
                                capability = requirement_data.get('capability')
                                if capability is None:
                                    raise f"Capability in requirement definition {requirement_name} in data_type {name}"
                                node_type.dependencies['capability_types'].add(capability)
                                node_type.dependencies['node_types'].add(requirement_data.get('node'))
                                relationship = requirement_data.get('relationship')
                                if type(relationship) == str:
                                    node_type.dependencies['relationship_types'].add(relationship)
                                else:
                                    if relationship.get('type') is None:
                                        raise f"In relationship in requirement_definition {requirement_name} " \
                                              f"in node_type {name}"
                                    node_type.dependencies['relationship_types'].add(relationship.get('type'))
                                    interface_types, data_types, artifacts, artifacts_types =\
                                        self.check_interface_in_entity(relationship, node_type)
                                    node_type.dependencies['interface_types'].update(interface_types)
                                    node_type.dependencies['data_types'].update(data_types)
                                    node_type.dependencies['artifacts'].update(artifacts)
                                    node_type.dependencies['artifact_types'].update(artifacts_types)

            if derived_from:
                node_type.derived_from.add(derived_from)

        return node_types

    def prepare_group_types(self, data: dict) -> dict[str: GroupType]:
        group_types = {}
        for name, data in data.items():
            derived_from = data.get('derived_from')
            version = data.get('version')
            group_type = GroupType(self.identifier_generator(), name, data, version)
            group_type.dependencies['data_types'].update(
                self.check_property_in_entity(data, group_type.dependencies['data_types']))
            group_type.dependencies['data_type'].update(
                self.check_property_in_entity(data, group_type.dependencies['data_types'], key_name='attributes'))
            members = data.get('members')
            if members:
                group_type.dependencies['node_type'].update(members)
            if derived_from:
                group_type.derived_from.add(derived_from)
        return group_types

    def prepare_policy_types(self, data: dict) -> dict[str: PolicyType]:
        policy_types = {}
        for name, data in data.items():
            derived_from = data.get('derived_from')
            version = data.get('version')
            policy_type = PolicyType(self.identifier_generator(), name, data, version)
            policy_type.dependencies['data_types'].update(
                self.check_property_in_entity(data, policy_type.dependencies['data_types']))
            targets = data.get('targets')
            if targets:
                for target in targets:
                    if self.node_types.get(target):
                        policy_type.dependencies['node_types'].add(target)
                    elif self.group_types.get(target):
                        policy_type.dependencies['policy_types'].add(target)
                    else:
                        raise f"In policy_type {name} target type is missing {target}"
            triggers = data.get('triggers')
            if triggers:
                for trigger_name, trigger_data in triggers.items():
                    target_filter = trigger_data.get('target_filter')
                    if target_filter:
                        node = target_filter.get('node')
                        if node is None:
                            raise f"node in target_filter in trigger {trigger_name} in policy_type {name}"
                        policy_type.dependencies['node_types'].add(node)
            if derived_from:
                policy_type.derived_from.add(derived_from)
        return policy_types

    def check_interface_in_entity(self, data: dict, father_node) -> tuple[set[str], set[str], set[str], set[str]]:
        interface_types = set()
        data_types = set()
        artifacts = set()
        artifacts_types = set()
        interfaces: dict = data.get('interfaces')
        if interfaces:
            for interface_name, interface_data in interfaces.items():
                interface_type = interface_data.get('type')
                if interface_type is None:
                    raise Exception('In interface definition, name:' + interface_name + 'type is undefined')
                interface_types.add(interface_type)
                data_types = data_types.union(
                    self.check_property_in_entity(interface_data, data_types, key_name='inputs'))
                operation_artifacts, operation_artifact_types, operation_data_types = self.check_operation_in_entity(
                    interface_data, father_node)
                artifacts = artifacts.union(operation_artifacts)
                artifacts_types = artifacts_types.union(operation_artifact_types)
                data_types = data_types.union(operation_data_types)
                artifacts = artifacts.union(self.check_notification_in_entity(interface_data))
        return interface_types, data_types, artifacts, artifacts_types

    @staticmethod
    def check_notification_in_entity(data):
        artifacts = set()
        notifications: dict = data.get('notifications')
        if notifications:
            for notification_name, notification_data in notifications.items():
                if len(notification_data.items()) == 1 and type(notification_data.__getitem__(0)) == str:
                    artifacts.add(notification_data.__getitem__(0))
                else:
                    primary = notification_data.get('primary')
                    if primary:
                        artifacts.add(artifacts)
                    dependencies = notification_data.get('dependencies')
                    if dependencies:
                        for artifact_name in dependencies:
                            artifacts.add(artifact_name)
        return artifacts

    def check_operation_in_entity(self, data: dict, father_node) -> tuple[set[str], set[str], set[str]]:
        artifacts = set()
        artifact_types = set()
        data_types = set()
        operation: dict = data.get('operations')
        if operation:
            for operation_name, operation_data in operation.items():
                if len(operation_data.items()) == 1 and type(operation_data.__getitem__(0)) == str:
                    artifacts.add(operation_data.__getitem__(0))
                else:
                    data_types = data_types.union(self.check_parameter_in_entity(operation_data))
                    implementation = operation_data.get('implementation')
                    if implementation:
                        # TODO check that primary and dependencies have same type
                        if type(implementation) == str:
                            artifacts.add(implementation)
                        else:
                            primary = implementation.get('primary')
                            if primary:
                                if type(primary) == str:
                                    artifacts.add(primary)
                                else:
                                    primary: dict
                                    if len(primary) > 1:
                                        raise "Primary in operation_definition, name:" + operation_name + "is too long"
                                    # TODO make artifact_definition_parser
                                    for artifact_name, artifact_value in primary.items():
                                        artifact_definition = ArtifactDefinition(artifact_name,
                                                                                 artifact_value,
                                                                                 father_node)
                                        if self.artifact_definition.get(artifact_name):
                                            raise "Such artifact_definition already exists, name:" + artifact_name
                                        self.artifact_definition[artifact_name] = artifact_definition
                                        if artifact_value.get('type'):
                                            artifact_types.add(artifact_value.get('type'))
                            dependencies = implementation.get('dependencies')
                            if dependencies:
                                if type(dependencies) != list:
                                    raise "Dependencies in operation_definition, name:" + operation_name + "is not list"
                                if len(dependencies) > 1:
                                    if type(dependencies[0]) == str:
                                        for artifact_name in dependencies:
                                            if type(artifact_name) != str:
                                                raise "Mixed type of artifact in dependencies of" \
                                                      " operation_definition, name" + operation_name
                                            artifacts.add(artifact_name)
                                    else:
                                        for artifact_data in dependencies:
                                            # TODO make artifact_definition_parser
                                            if type(artifact_data) != dict:
                                                raise "Mixed type of artifact in dependencies of" \
                                                      " operation_definition, name" + operation_name
                                            if len(artifact_data) > 1:
                                                raise "artifact_definition is too long in dependencies of " \
                                                      "operation_definition, name" + operation_name
                                            for artifact_name, artifact_value in artifact_data:
                                                artifact_definition = ArtifactDefinition(artifact_name,
                                                                                         artifact_value,
                                                                                         father_node)
                                                if self.artifact_definition.get(artifact_name):
                                                    raise f"Such artifact_definition already exists," \
                                                          f" name:{artifact_name} "
                                                self.artifact_definition[artifact_name] = artifact_definition
                                                if artifact_value.get('type'):
                                                    artifact_types.add(artifact_value.get('type'))
        return artifacts, artifact_types, data_types

    def check_parameter_in_entity(self, data: dict) -> set[str]:
        data_types = set()
        parameters: dict = data.get('inputs')
        if parameters:
            for parameter_name, parameter_data in parameters.items():
                data_type = parameters.get('type')
                if data_type:
                    data_types.add(data_type)
                data_types = data_types.union(self.check_schema_in_entity(parameter_data, data_types))
                # NOTE value expression parser?
        return data_types

    def check_property_in_entity(self, data: dict, result: set[str], key_name='properties') -> set[str]:
        properties: dict = data.get(key_name)
        if properties:
            # NOTE can be parallelized
            for property_name, property_value in properties.items():
                result = result.union(self.get_property_dependencies(property_value, property_name))
        return result

    def check_schema_in_entity(self, data: dict, result: set[str]) -> set[str]:
        """
        This function checks if there is key_schema or entry_schema in this object
        It returns set of required data_types for  key_schema or entry_schema and their nested schemas
        :param data: dict
        :param result: set[str]
        :return result: set[str]
        """
        key_schema: dict = data.get('key_schema')
        if key_schema:
            result = result.union(self.get_schema_dependencies(key_schema))
        entry_schema: dict = data.get('entry_schema')
        if entry_schema:
            result = result.union(self.get_schema_dependencies(entry_schema))
        return result

    def get_property_dependencies(self, data: dict, name: str) -> set[str]:
        """
        This function returns all dependencies of property_definition and attribute_definition
        :param data: dict
        :param name: str
        :return result: srt[str]
        """
        data_type: str = data.get('type')
        result = set()
        if data_type is None:
            raise Exception('In property definition, name:' + name + 'type is undefined')
        result.add(data_type)
        result = result.union(self.check_schema_in_entity(data, result))
        return result

    def get_schema_dependencies(self, data: dict) -> set[str]:
        """
        This function returns all dependencies of schema_definition
        :param data: dict
        :return result: set[str]
        """
        data_type: str = data.get('type')
        result = set()
        if data_type is None:
            raise Exception('in schema, type is undefined')
        result.add(data_type)
        result = result.union(self.check_schema_in_entity(data, result))
        return result


with open("test.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)
    test = TypeStorage(data_loaded)
    t1 = set()
    t2 = set('asd')
    t1.union(t2)
    print(t1)
    print(test)
