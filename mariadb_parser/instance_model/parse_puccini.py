import copy

def create_value_atom(node, definition):
    # print(definition)

    meta = None
    if '$meta' in definition.keys():
        meta = definition['$meta']

    if '$functionCall' in definition.keys():
        return create_function(
            node,
            meta,
            definition['$functionCall']
        )

    if '$primitive' in definition.keys() and definition['$primitive'] is None:
        return Primitive(
            node,
            meta,
            definition['$primitive']
        )

    if meta is not None and meta['type'] == 'map':
        return Map(node, meta, definition['$primitive'])

    if meta is not None and meta['type'] == 'list':
        return List(node, meta, definition['$list'])

    return create_value(
        node,
        meta,
        definition['$primitive']
    )


def create_value(node, meta, primitive):
    # print(definition)
    # print(meta)
    # print(primitive)

    # if '$functionCall' in definition.keys():
    #   return create_function(node, type_def, definition)

    # if '$list' in definition or type_def['name'] == 'list':
    #   return List(node, type_def, definition)

    if meta is None:
        return Primitive(node, {}, primitive)

    if meta['type'] == 'version':
        return Version(node, meta, primitive)

    if meta['type'] in {'scalar-unit.time', 'scalar-unit.size'}:
        return ScalarUnit(node, meta, primitive)

    if meta['type'] in {'integer', 'string', 'boolean', 'tosca::PortDef'}:
        return Primitive(node, meta, primitive)

    raise RuntimeError('unknown primitive')
    # return String(node, type_def, definition['$value'])


def create_function(node, meta, function_call):
    # print(meta)
    # print(function_call)

    if function_call['name'] == 'tosca.function.get_input':
        return GetInput(node, meta, function_call['arguments'])

    if function_call['name'] == 'tosca.function.get_property':
        return GetProperty(node, meta, function_call['arguments'])

    if function_call['name'] == 'tosca.function.get_attribute':
        return GetAttribute(node, meta, function_call['arguments'])

    if function_call['name'] == 'tosca.function.concat':
        return Concat(node, meta, function_call['arguments'])

    raise RuntimeError(f'unknown function {function_call}')


class ValueInstance:
    def __init__(self, node, meta):
        self.node = node
        self.meta = meta

    def render(self):
        return self.value

    def set(self, value):
        self.value = value

    def get(self):
        raise RuntimeError('Unimplemented get')


class Primitive(ValueInstance):
    """
    Represents string, boolean
    """

    def __init__(self, node, meta, primitive):
        super().__init__(node, meta)
        self.value = primitive

    def get(self):
        return self.value


class Version(ValueInstance):
    def __init__(self, node, meta, primitive):
        super().__init__(node, meta)
        self.value = primitive['$string']

    def get(self):
        return self.value


class ScalarUnit(ValueInstance):
    def __init__(self, node, meta, primitive):
        super().__init__(node, meta)
        self.value = primitive['$number']

    def get(self):
        return self.value


class List(ValueInstance):
    def __init__(self, node, meta, list_primitives):
        super().__init__(node, meta)

        if list_primitives is None:
            self.values = None
            return

        self.values = [create_value_atom(node, e) for e in list_primitives]

    def render(self):
        if self.values is None:
            return None
        return [v.render() for v in self.values]

    def get(self):
        if self.values is None:
            return None
        return [v.get() for v in self.values]


class Map(ValueInstance):
    def __init__(self, node, meta, primitive):
        super().__init__(node, meta)

        if primitive is None:
            self.values = None
            return

        self.values = dict()
        for e in primitive:
            key = e['$key']['$primitive']
            self.values[key] = create_value(node, e['$information']['type'], e)

    def render(self):
        if self.values is None:
            return None
        values = dict()
        for key, value in self.values.items():
            values[key] = value.render()
        return values

    def get(self):
        if self.values is None:
            return None
        values = dict()
        for key, value in self.values.items():
            values[key] = value.get()
        return values


class GetInput(ValueInstance):
    def __init__(self, node, meta, args):
        super().__init__(node, meta)
        self.input_name = args[0]['$primitive']

    def render(self):
        return {
            'get_input': [self.input_name],
        }

    def get(self):
        return self.node.topology.find_input(self.input_name).get()


class GetProperty(ValueInstance):
    def __init__(self, node, meta, args):
        super().__init__(node, meta)
        self.args = [e['$primitive'] for e in args]

    def render(self):
        return {
            'get_property': self.args,
        }

    def get(self):
        # print('GETPROP', self.args)
        start = self.args[0]
        # try:
        attr = None

        if start == 'SELF':
            attr = self.node.find_property(self.args[1:])
        elif start == 'SOURCE':
            attr = self.node.source.find_property(self.args[1:])
        elif start == 'TARGET':
            attr = self.node.target.find_property(self.args[1:])
        else:
            attr = self.node.topology.nodes[start].find_property(self.args[1:])

        if attr is None:
            return None

        return attr.get()

        # except RuntimeError:
        #   raise RuntimeError(f'{self.node.topology.name}: cannot find property from node {self.node.name}: {self.args}')


class GetAttribute(ValueInstance):
    def __init__(self, node, meta, args):
        super().__init__(node, meta)
        self.args = [e['$primitive'] for e in args]

    def render(self):
        return {
            'get_attribute': self.args,
        }

    def get(self):
        # print('GETATTR', self.args)
        start = self.args[0]
        try:
            attr = None
            if start == 'SELF':
                attr = self.node.find_attribute(self.args[1:])
            elif start == 'SOURCE':
                attr = self.node.source.find_attribute(self.args[1:])
            elif start == 'TARGET':
                attr = self.node.target.find_attribute(self.args[1:])
            else:
                attr = self.node.topology.nodes[start].find_attribute(self.args[1:])

            if attr is None:
                return None
            return attr.get()

        except RuntimeError:
            raise RuntimeError(
                f'{self.node.topology.name}: cannot find attribute from node {self.node.name}: {self.args}')


class AttributeMapping(ValueInstance):
    def __init__(self, node, meta, mapping):
        super().__init__(node, meta)
        self.args = [e['$primitive'] for e in mapping]

    def render(self):
        return self.args

    def get(self):
        return self.value.get()

    def set(self, value):
        self.value = value

        print(f'SET {self.args}')
        start = self.args[0]
        try:
            attr = None

            if start == 'SELF':
                attr = self.node.find_attribute(self.args[1:])
            elif start == 'SOURCE':
                attr = self.node.source.find_attribute(self.args[1:])
            elif start == 'TARGET':
                attr = self.node.target.find_attribute(self.args[1:])
            else:
                attr = self.node.topology.nodes[start].find_attribute(self.args[1:])

            if attr is None:
                return

            attr.set(value)

        except RuntimeError:
            raise RuntimeError(
                f'{self.node.topology.name}: cannot find attribute from node {self.node.name}: {self.args}')


class Concat(ValueInstance):
    def __init__(self, node, type_def, args):
        super().__init__(node, type_def)
        self.args = []
        for arg in args:
            if '$primitive' in arg.keys():
                self.args.append(Primitive(node, {}, arg['$primitive']))
            else:
                # print(arg)
                self.args.append(create_function(node, {}, arg['$functionCall']))

    def render(self):
        return [a.render() for a in self.args]

    def get(self):
        strings = [a.get() for a in self.args]
        return ''.join(strings)


class AttributeInstance:
    def __init__(self, node, location, definition, is_property=False):
        self.node = node
        self.location = location
        self.mapping = None
        self.is_property = is_property
        self.definition = copy.deepcopy(definition)
        self.value = create_value_atom(node, self.definition)

    def render(self):
        return self.get()
        # if self.mapping is None:
        #   return {
        #     'value': self.get(),
        #     'mapping': None,
        #   }
        # return {
        #   'value': self.get(),
        #   'mapping': self.mapping.location
        # }

    def map(self, other):
        self.mapping = other
        if self.is_property:
            self.mapping.set(self.value)
        else:
            self.set(self.mapping.value)

        # self.set(self.mapping.get())

    def get(self):
        if self.mapping is not None:
            mapped = self.mapping.get()
            if mapped is not None:
                return mapped

        return self.value.get()

    def update(self, diff):
        print(diff)
        self.value.set(diff)

        # if 'value' in diff.keys():
        #   print(diff['value'])
        #   self.set(Primitive(self.node, {}, diff['value']))
        # if 'mapping' in diff.keys():
        #   mapping = diff['mapping']
        #   author = self.node.metadata['substitution_author']
        #   topology_name = self.node.metadata['substitution_name']
        #   topology = instance.get_topology(author, topology_name)
        #   if len(mapping) == 1:
        #     self.map(topology.inputs[mapping[0]])
        #   elif len(mapping) == 2:
        #     self.map(topology.nodes[mapping[0]].attributes[mapping[1]])
        #   elif len(mapping) == 3:
        #     if isinstance(self.node, NodeInstance):
        #       self.map(topology.nodes[mapping[0]].capabilities[mapping[1]].attributes[mapping[2]])
        #     else:
        #       node = topology.nodes[mapping[0]]
        #       for req in node.requirements:
        #         if req.name == mapping[1]:
        #       self.map(topology.nodes[mapping[0]].capabilities[mapping[1]].attributes[mapping[2]])
        #   else:
        #     raise RuntimeError('cannot map')

    def set(self, value):
        self.value = value
        if self.mapping is not None:
            self.mapping.set(value)
            # print(f'UPDATED ATTR {self.node.topology.name} {self.node.name} : {self.value.get()}')


class CapabilityInstance:
    def __init__(self, name, node, definition):
        self.name = copy.deepcopy(name)
        self.node = node

        self.definition = copy.deepcopy(definition)
        self.find_type()

        self.attributes = {}

        for prop_name, prop_def in self.definition['properties'].items():
            self.attributes[prop_name] = AttributeInstance(
                self.node,
                [self.node.name, self.name, prop_name],
                prop_def,
                is_property=True
            )

        for attr_name, attr_def in self.definition['attributes'].items():
            self.attributes[attr_name] = AttributeInstance(
                self.node,
                [self.node.name, self.name, attr_name],
                attr_def
            )

    def render(self):
        render_properties = {}
        render_attributes = {}
        for attr_name, attr in self.attributes.items():
            if attr.is_property:
                render_properties[attr_name] = attr.render()
            else:
                render_attributes[attr_name] = attr.render()
        return {
            'type': self.type,
            'properties': render_properties,
            'attributes': render_attributes
        }

    def update(self, diff):
        if 'attributes' in diff.keys():
            for attr_name, attr_diff in diff['attributes'].items():
                self.attributes[attr_name].update(attr_diff)

        if 'properties' in diff.keys():
            for prop_name, prop_diff in diff['properties'].items():
                self.attributes[prop_name].update(prop_diff)

    def find_type(self):
        seen = set(self.definition['types'].keys())
        for type_name, type_body in self.definition['types'].items():
            if 'parent' in type_body.keys():
                seen.remove(type_body['parent'])
        self.type = seen.pop()

    def find_property(self, args):
        path = args[0]
        print(f'CAP ATTRIBUTES: {self.attributes.keys()}')
        if path in self.attributes.keys():
            attr = self.attributes[path]
            if not attr.is_property:
                raise RuntimeError(f'there is the attribute with name {path}, but it is not a property')
            return attr
        return None

    def find_attribute(self, args):
        path = args[0]
        if path in self.attributes.keys():
            return self.attributes[path]
        return None


class OperationInstance:
    def __init__(self, node, definition):
        self.definition = copy.deepcopy(definition)
        self.implementation = None
        self.node = node

        if self.definition['implementation'] != '':
            self.implementation = self.definition['implementation']

        self.inputs = {}
        for input_name, input_def in self.definition['inputs'].items():
            self.inputs[input_name] = AttributeInstance(
                node,
                [],
                input_def,
                is_property=True
            )

        self.outputs = {}
        for output_name, output_def in self.definition['outputs'].items():
            self.outputs[output_name] = AttributeMapping(node, output_def['$meta'], output_def['$list'])

    def render(self):
        render_inputs = {}
        for input_name, input_body in self.inputs.items():
            render_inputs[input_name] = input_body.render()

        render_outputs = {}
        for output_name, output_body in self.outputs.items():
            render_outputs[output_name] = output_body.render()

        return {
            'implementation': self.implementation,
            'inputs': render_inputs,
            'outputs': render_outputs
        }


class InterfaceInstance:
    def __init__(self, node, definition):
        self.definition = copy.deepcopy(definition)
        self.abstract = True
        self.node = node

        self.find_type()

        self.inputs = {}
        for input_name, input_def in self.definition['inputs'].items():
            self.inputs[input_name] = AttributeInstance(
                node,
                [],
                input_def,
                is_property=True
            )

        self.operations = {}
        for op_name, op_def in self.definition['operations'].items():
            self.operations[op_name] = OperationInstance(node, op_def)
            if self.operations[op_name].implementation is not None:
                self.abstract = False

    def find_type(self):
        seen = set(self.definition['types'].keys())
        for type_name, type_body in self.definition['types'].items():
            if 'parent' in type_body.keys():
                seen.remove(type_body['parent'])
        self.type = seen.pop()

    def render(self):
        return {
            'type': self.type,
            'operations': {op_name: op.render() for op_name, op in self.operations.items()}
        }


class RelationshipInstance:
    def __init__(self, name, source, target, definition):
        self.name = name
        self.source = source
        self.target = target
        self.definition = copy.deepcopy(definition)

        self.types = copy.deepcopy(self.definition['types'])
        self.find_type()

        self.attributes = {}

        for prop_name, prop_def in self.definition['properties'].items():
            self.attributes[prop_name] = AttributeInstance(
                self,
                [self.source.name, self.name],
                prop_def,
                is_property=True
            )

        for attr_name, attr_def in self.definition['attributes'].items():
            self.attributes[attr_name] = AttributeInstance(
                self,
                [self.source.name, self.name],
                attr_def
            )

        self.interfaces = {}
        for interface_name, interface_def in self.definition['interfaces'].items():
            self.interfaces[interface_name] = InterfaceInstance(self, interface_def)

    def update(self, diff):
        if 'attributes' in diff.keys():
            for attr_name, attr_diff in diff['attributes'].items():
                self.attributes[attr_name].update(attr_diff)

        if 'properties' in diff.keys():
            for prop_name, prop_diff in diff['properties'].items():
                self.attributes[prop_name].update(prop_diff)

    def render(self):
        render_properties = {}
        render_attributes = {}
        for attr_name, attr in self.attributes.items():
            if attr.is_property:
                render_properties[attr_name] = attr.render()
            else:
                render_attributes[attr_name] = attr.render()
        return {
            'type': self.type,
            'properties': render_properties,
            'attributes': render_attributes,
            'interfaces': {interface_name: interface.render() for interface_name, interface in self.interfaces.items()},
        }

    def find_type(self):
        seen = set(self.types.keys())
        for type_name, type_body in self.types.items():
            if 'parent' in type_body.keys():
                seen.remove(type_body['parent'])
        self.type = seen.pop()


class NodeInstance:
    def __init__(self, name, topology, definition):
        self.name = copy.deepcopy(name)
        self.topology = topology
        self.abstract = True

        self.definition = copy.deepcopy(definition)

        self.types = copy.deepcopy(self.definition['types'])
        self.find_type()

        self.directives = copy.deepcopy(self.definition['directives'])
        self.metadata = {
            'substitution': None,
            'selection': None,
        }

        self.attributes = {}

        for prop_name, prop_def in self.definition['properties'].items():
            self.attributes[prop_name] = AttributeInstance(self, [self.name], prop_def, is_property=True)

        for attr_name, attr_def in self.definition['attributes'].items():
            self.attributes[attr_name] = AttributeInstance(self, [self.name], attr_def)

        self.capabilities = {}
        for cap_name, cap_def in self.definition['capabilities'].items():
            self.capabilities[cap_name] = CapabilityInstance(cap_name, self, cap_def)

        self.interfaces = {}
        for interface_name, interface_def in self.definition['interfaces'].items():
            self.interfaces[interface_name] = InterfaceInstance(self, interface_def)
            if not self.interfaces[interface_name].abstract:
                self.abstract = False

        self.requirements = []

    def update(self, diff):
        if 'metadata' in diff.keys():
            for m_key, m_value in diff['metadata'].items():
                self.metadata[m_key] = m_value

        if 'attributes' in diff.keys():
            for attr_name, attr_diff in diff['attributes'].items():
                self.attributes[attr_name].update(attr_diff)

        if 'properties' in diff.keys():
            for prop_name, prop_diff in diff['properties'].items():
                self.attributes[prop_name].update(prop_diff)

        if 'capabilities' in diff.keys():
            for cap_name, cap_diff in diff['capabilities'].items():
                self.capabilities[cap_name].update(cap_diff)

    def render(self):
        render_properties = {}
        render_attributes = {}
        for attr_name, attr in self.attributes.items():
            if attr.is_property:
                render_properties[attr_name] = attr.render()
            else:
                render_attributes[attr_name] = attr.render()
        return {
            'type': self.type,
            'directives': self.directives,
            'metadata': self.metadata,
            'properties': render_properties,
            'attributes': render_attributes,
            'capabilities': {cap_name: cap.render() for cap_name, cap in self.capabilities.items()},
            'interfaces': {interface_name: interface.render() for interface_name, interface in self.interfaces.items()},
            'requirements': [
                {
                    req.name: {
                        'node': req.target.name if req.target is not None else None,
                        'capability': None,
                        'relationship': req.render(),
                    }
                } for req in self.requirements
            ]
        }

    def find_type(self):
        seen = set(self.types.keys())
        for type_name, type_body in self.types.items():
            if 'parent' in type_body.keys():
                seen.remove(type_body['parent'])
        self.type = seen.pop()

    def find_property(self, args):
        path = args[0]
        rest = args[1:]

        if path in self.attributes.keys():
            attr = self.attributes[path]
            if not attr.is_property:
                raise RuntimeError(f'there is the attribute with name {path}, but it is not a property')
            return attr

        # print(f'CAPABILITIES: {self.capabilities.keys()}')
        if path in self.capabilities.keys():
            return self.capabilities[path].find_property(rest)

        for r in self.requirements:
            if r.name == path and r.target is not None:
                return r.target.find_attribute(rest)

        return None

    def find_attribute(self, args):
        path = args[0]
        rest = args[1:]

        if path in self.attributes.keys():
            return self.attributes[path]

        if path in self.capabilities.keys():
            return self.capabilities[path].find_attribute(rest)

        for r in self.requirements:
            if r.name == path and r.target is not None:
                return r.target.find_attribute(rest)

        return None


class TopologyTemplateInstance:
    def __init__(self, name, definition):
        self.name = copy.deepcopy(name)
        self.definition = copy.deepcopy(definition)

        self.inputs = {}
        for input_name, input_def in self.definition['inputs'].items():
            self.inputs[input_name] = AttributeInstance(
                self,
                [input_name],
                input_def,
                is_property=True
            )

        self.nodes = {}
        for node_name, node_def in self.definition["nodeTemplates"].items():
            node = NodeInstance(node_name, self, node_def)
            self.nodes[node_name] = node

        for node_name, node in self.nodes.items():
            for req_def in node.definition['requirements']:
                # print(f"{node_name} - {req_def['name']}")
                target = None
                if req_def['nodeTemplateName'] != '':
                    target = self.nodes[req_def['nodeTemplateName']]
                node.requirements.append(RelationshipInstance(
                    req_def['name'],
                    node,
                    target,
                    req_def['relationship']
                ))

    def render(self):
        render_inputs = {}
        for input_name, input_body in self.inputs.items():
            render_inputs[input_name] = input_body.render()
        return {
            'inputs': render_inputs,
            'nodes': {node_name: node.render() for node_name, node in self.nodes.items()},
            'substitution_mappings': self.definition['substitution'],
        }

    def update(self, diff):
        if 'topology' not in diff.keys():
            return
        elif 'nodes' not in diff['topology'].keys():
            return

        for node_name, node_diff in diff['topology']['nodes'].items():
            self.nodes[node_name].update(node_diff)

    def find_input(self, input_name):
        if input_name not in self.inputs.keys():
            raise RuntimeError(f'no input named {input_name}')
        return self.inputs[input_name]
