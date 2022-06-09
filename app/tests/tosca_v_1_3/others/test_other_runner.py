import unittest
import TestConstraintClause
import TestDirectives
import TestMetadata
import TestNodeTemplate
import TestRelationshipTemplate

otherTestSuite = unittest.TestSuite()
otherTestSuite.addTest(unittest.makeSuite(TestConstraintClause.TestConstraintClause))
otherTestSuite.addTest(unittest.makeSuite(TestDirectives.TestDirectives))
otherTestSuite.addTest(unittest.makeSuite(TestDirectives.TestDirectives))
otherTestSuite.addTest(unittest.makeSuite(TestMetadata.TestMetadata))
otherTestSuite.addTest(unittest.makeSuite(TestNodeTemplate.TestNodeTemplate))
otherTestSuite.addTest(unittest.makeSuite(TestRelationshipTemplate.TestRelationshipTemplate))


runner = unittest.TextTestRunner(verbosity=2)
runner.run(otherTestSuite)
