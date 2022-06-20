import unittest

from parser.tests.tosca_v_1_3.assignments import TestAttribute, TestCapability, TestProperty, TestRequirement

assignmentTestSuite = unittest.TestSuite()
assignmentTestSuite.addTest(unittest.makeSuite(TestAttribute.TestAttribute))
assignmentTestSuite.addTest(unittest.makeSuite(TestCapability.TestCapability))
assignmentTestSuite.addTest(unittest.makeSuite(TestProperty.TestProperty))
assignmentTestSuite.addTest(unittest.makeSuite(TestRequirement.TestRequirement))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(assignmentTestSuite)
