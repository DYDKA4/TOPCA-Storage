import yaml


class DataType:
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
        self.identifier = identifier
        self.name: str = name
        self.type_of_type: str = 'data_type'
        self.version: str = version
        self.data = data
        self.derived_from: set[str] = set()
        self.derived_from_id: set[int] = set()
        self.dependencies: set[str] = set()
        self.dependencies_id: set[id] = set()


class TypeStorage:
    """
    TypeStorage class parse part of yaml file with type definition and prepare it to submit it into SQL database
    it consists of:
        data_types where stored dict where keys are name of DataType and value is DataType object
    """

    def __init__(self, data: dict):
        self.data = data
        self.data_types: dict[str, DataType] = {}
        if data.get('data_types'):
            self.data_types = self.prepare_data_types(data.get('data_types'))
            for data_type in self.data_types.values():
                self.data_type_linage(data_type)

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
            key_schema = data.get('key_schema')
            data_type = DataType(len(data_types), name, data, version)
            if key_schema:
                key_schema_dependencies = self.get_schema_dependencies(key_schema)
                data_type.dependencies = data_type.dependencies.union(key_schema_dependencies)
            entry_schema = data.get('entry_schema')
            if entry_schema:
                entry_schema_dependencies = self.get_schema_dependencies(entry_schema)
                data_type.dependencies = data_type.dependencies.union(entry_schema_dependencies)
            properties: dict = data.get('properties')
            if properties:
                # NOTE can be parallelized
                for property_name, property_value in properties.items():
                    data_type.dependencies = \
                        data_type.dependencies.union(self.get_property_dependencies(property_value, property_name))
            if derived_from:
                data_type.derived_from.add(derived_from)
            data_types[name] = data_type
        return data_types

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
        This function returns all dependencies of property_definition
        :param data: dict
        :param name: str
        :return result: srt[str]
        """
        data_type: str = data.get('type')
        result = set()
        if data_type is None:
            raise Exception('In property definition, name:' + name + 'type is undefined')
        result.add(data_type)
        result.union(self.check_schema_in_entity(data, result))
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
        result.union(self.check_schema_in_entity(data, result))
        return result

    def data_type_linage(self, data_type: DataType) -> None:
        """
        This method restores all previous derived from
        :param data_type: DataType
        :return: None
        """
        # todo доделать
        for derived_from in data_type.derived_from:
            derived_from: str
            derived_from_structure = self.data_types.get(derived_from)
            if derived_from_structure is None:
                raise Exception('No such data_type in derived_from from yaml file. DataType: ' + data_type.name)
            print(derived_from_structure)


with open("test.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)
    test = TypeStorage(data_loaded)
    print(test)
