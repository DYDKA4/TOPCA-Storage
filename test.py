import unittest

from parser.tests.tosca_v_1_3.parser.assignments import TestAttribute


class TestJsonParser(unittest.TestCase):

    def test_definition(self):
        self.TestAttribute = TestAttribute


if __name__ == "__main__":
    unittest.main()
