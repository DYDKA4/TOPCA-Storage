from app import communication_with_nebula as cwn


class Vertex:
    def __init__(self, name, vertex_type_tosca):
        self.vid = None
        self.vertex_type_tosca = vertex_type_tosca
        self.vertex_type_system = 'Vertex'
        self.name = name
        self.requirements = {} # хз как сделать лучше
        self.capabilities = []
        self.properties = []

    def generate_vid(self):
        if self.vertex_type_system is None:
            assert 0, 'vertex_type_system is None'
        else:
            self.vid = self.vertex_type_system + str(
                cwn.number_of_entities(cwn.chose_of_space(), self.vertex_type_system))

    def set_vid(self, vid):
        self.vid = vid

    def __str__(self):
        return f'{hex(id(self))}, {self.vid}, {self.vertex_type_tosca}, {self.vertex_type_system}, {self.name}, {self.requirements}, ' \
               f'{self.capabilities}, {self.properties}'

    def __repr__(self):
        return repr(vars(self))


class AssignmentVertex(Vertex):
    def __init__(self, name, vertex_type='AssignmentVertex'):
        super().__init__(name, vertex_type)
        self.vertex_type_system = 'AssignmentVertex'

    def add_requirements(self, obj, link_type):
        # проверка condition для дочерних классов
        self.requirements[obj] = link_type

    def add_capabilities(self, obj):
        self.capabilities.append(obj)

    def add_properties(self, obj):
        self.properties.append(obj)

    def __repr__(self):
        return hex(id(self))


class ClusterName(Vertex):
    def __init__(self, name, pure_yaml):
        super().__init__(name, 'ClusterName')
        self.vertex_type_system = 'ClusterName'
        self.pure_yaml = pure_yaml


class AssignmentCapabilities(Vertex):
    def __init__(self, name, vertex_type='AssignmentCapabilities'):
        super().__init__(name, vertex_type)
        self.vertex_type_system = 'AssignmentCapabilities'

    def add_properties(self, obj):
        self.properties.append(obj)

    def __str__(self):
        return f'{self.vid}, {self.vertex_type_tosca}, {self.vertex_type_system}, {self.name}, {self.requirements}, ' \
               f'{self.capabilities}, {self.properties}'


class AssignmentProperties(Vertex):
    def __init__(self, value_name, value, name='null', vertex_type='AssignmentProperties'):
        super().__init__(name, vertex_type)
        self.value_name = value_name
        self.value = value
        self.vertex_type_system = 'AssignmentProperties'

    def __str__(self):
        return f'{self.vid}, {self.vertex_type_tosca}, {self.vertex_type_system}, {self.name}, {self.requirements}, ' \
               f'{self.capabilities}, {self.properties}'


class DefinitionCapabilities(Vertex):
    def __init__(self, name, vertex_type='DefinitionCapabilities'):
        super().__init__(name, vertex_type)
        self.vertex_type_system = 'DefinitionCapabilities'

    def add_properties(self, obj):
        self.properties.append(obj)


class DefinitionVertex(Vertex):
    def __init__(self, name, vertex_type='DefinitionRequirements'):
        super().__init__(name, vertex_type)
        self.vertex_type_system = 'DefinitionRequirements'

    def add_requirements(self, obj, link_type):
        # проверка condition для дочерних классов
        self.requirements[obj] = link_type

    def add_capabilities(self, obj):
        self.capabilities.append(obj)

    def add_properties(self, obj):
        self.properties.append(obj)

    def __repr__(self):
        return hex(id(self))

class DefinitionProperties(Vertex):
    def __init__(self, name, vertex_type='DefinitionProperties'):
        super().__init__(name, vertex_type)
        self.vertex_type_system = 'DefinitionProperties'

# a = Vertex('YA', 'BlockStorage')
# b = Vertex('BB', 'Compute')
# a.generate_vid()
# b.generate_vid()
# a.set_requirements(b)
#
# a.print()
