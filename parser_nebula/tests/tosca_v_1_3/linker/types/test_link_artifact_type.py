import unittest

from parser_nebula.linker.tosca_v_1_3.types.ArtifactType import link_artifact_type
from parser_nebula.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser_nebula.parser.tosca_v_1_3.types.ArtifactType import ArtifactType


class TestArtifactType(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.artifact_types.append(ArtifactType('artifact_type_parent'))
        self.artifact = ArtifactType('artifact_type')
        self.service_template.artifact_types.append(self.artifact)

    def test_link_derived_from(self):
        self.artifact.derived_from = 'artifact_type_parent'
        link_artifact_type(self.service_template, self.artifact)
        self.assertEqual(self.service_template.artifact_types[0], self.artifact.derived_from.get('derived_from')[1])

if __name__ == '__main__':
    unittest.main()
