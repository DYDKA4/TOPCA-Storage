import unittest
import TestArtifact
import TestCapability
import TestData
import TestGroup
import TestInterface
import TestNode
import TestPolicy

typesTestSuite = unittest.TestSuite()
typesTestSuite.addTest(unittest.makeSuite(TestArtifact.TestArtifact))
typesTestSuite.addTest(unittest.makeSuite(TestCapability.TestCapability))
typesTestSuite.addTest(unittest.makeSuite(TestData.TestData))
typesTestSuite.addTest(unittest.makeSuite(TestGroup.TestGroup))
typesTestSuite.addTest(unittest.makeSuite(TestInterface.TestInterface))
typesTestSuite.addTest(unittest.makeSuite(TestNode.TestNode))
typesTestSuite.addTest(unittest.makeSuite(TestPolicy.TestPolicy))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(typesTestSuite)
