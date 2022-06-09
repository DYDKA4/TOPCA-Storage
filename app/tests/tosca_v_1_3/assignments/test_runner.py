import unittest
import TestAttribute
import TestCapability
import TestProperty
import TestRequirement

calcTestSuite = unittest.TestSuite()
calcTestSuite.addTest(unittest.makeSuite(TestAttribute.TestAttribute))
calcTestSuite.addTest(unittest.makeSuite(TestCapability.TestCapability))
calcTestSuite.addTest(unittest.makeSuite(TestCapability.TestCapability))
calcTestSuite.addTest(unittest.makeSuite(TestProperty.TestProperty))
calcTestSuite.addTest(unittest.makeSuite(TestRequirement.TestRequirement))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(calcTestSuite)
