import unittest

from parser.linker.tosca_v_1_3.definitions.ArtifactDefinition import link_artifact_definition
from parser.parser.tosca_v_1_3.definitions.ArtifactDefinition import ArtifactDefinition
from parser.parser.tosca_v_1_3.definitions.ServiceTemplateDefinition import ServiceTemplateDefinition
from parser.parser.tosca_v_1_3.types.ArtifactType import ArtifactType


class TestArtifactDefinition(unittest.TestCase):
    def setUp(self):
        self.service_template = ServiceTemplateDefinition('test_service')
        self.service_template.artifact_types.append(ArtifactType('artifact_type'))
        self.artifact = ArtifactDefinition('artifact_definition')

    def test_link_artifact_type(self):
        self.artifact.type = 'artifact_type'
        link_artifact_definition(self.service_template, self.artifact)
        self.assertEqual(self.service_template.artifact_types[0], self.artifact.type.get('type')[1])

if __name__ == '__main__':
    unittest.main()
