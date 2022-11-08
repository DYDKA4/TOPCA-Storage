import unittest

from parser_nebula.tests.tosca_v_1_3.parser.types import TestCapability, TestData, TestGroup, TestPolicy, TestRelationship
from parser_nebula.tests.tosca_v_1_3.parser.types import TestNode, TestInterface, TestArtifact


def test_types_runner():
    typesTestSuite = unittest.TestSuite()
    typesTestSuite.addTest(unittest.makeSuite(TestArtifact.TestArtifact))
    typesTestSuite.addTest(unittest.makeSuite(TestCapability.TestCapability))
    typesTestSuite.addTest(unittest.makeSuite(TestData.TestData))
    typesTestSuite.addTest(unittest.makeSuite(TestGroup.TestGroup))
    typesTestSuite.addTest(unittest.makeSuite(TestInterface.TestInterface))
    typesTestSuite.addTest(unittest.makeSuite(TestNode.TestNode))
    typesTestSuite.addTest(unittest.makeSuite(TestPolicy.TestPolicy))
    typesTestSuite.addTest(unittest.makeSuite(TestRelationship.TestRelationship))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(typesTestSuite)
