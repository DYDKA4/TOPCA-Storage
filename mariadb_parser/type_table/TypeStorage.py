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
                                             'policy_types': set()}

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
        if data.get('data_types'):
            self.data_types = self.prepare_data_types(data.get('data_types'))
            # TODO ADD DERIVED FROM FINDER
        if data.get('capability_types'):
            self.capability_types = self.prepare_capability_types(data.get('capability_types'))
            # TODO ADD DERIVED FROM FINDER
        if data.get('artifact_types'):
            self.artifact_types = self.prepare_artifact_types(data.get('artifact_types'))
        if data.get('interface_types'):
            self.interface_types = self.prepare_interface_types(data.get('interface_types'))

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
