import unittest

from parser.linker.tosca_v_1_3.types.InterfaceType import link_interface_type
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.InterfaceType import InterfaceType


class TestInterfaceType(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.interface_types.append(InterfaceType('interface_type_parent'))
        self.interface = InterfaceType('interface_type')
        self.service_template.interface_types.append(self.interface)

    def test_link_derived_from(self):
        self.interface.derived_from = 'interface_type_parent'
        link_interface_type(self.service_template, self.interface)
        self.assertEqual(self.service_template.interface_types[0], self.interface.derived_from.get('derived_from')[1])

if __name__ == '__main__':
    unittest.main()
