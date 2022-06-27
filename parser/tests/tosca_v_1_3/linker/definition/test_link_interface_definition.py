import unittest

from parser.linker.tosca_v_1_3.definitions.InterfaceDefinition import link_interface_definition
from parser.parser.tosca_v_1_3.definitions.InterfaceDefinition import InterfaceDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.InterfaceType import InterfaceType


class TestInterfaceDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.interface_types.append(InterfaceType('interface_type'))
        self.interface = InterfaceDefinition('interface_definition')

    def test_link_interface_type(self):
        self.interface.type = 'interface_type'
        link_interface_definition(self.service_template, self.interface)
        self.assertEqual(self.service_template.interface_types[0], self.interface.type.get('type')[1])


if __name__ == '__main__':
    unittest.main()
