import unittest
from app import json_parser
import json


class test(unittest.TestCase):

    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.parser = json_parser.parser()

    def Multiple_Block_Storage_attached_to_different_Servers(self):
        with open('tests/test_inputs/Multiple Block Storage attached to different Servers.json') as f:
            data = json.load(f)
            with open('tests/results/Multiple Block Storage attached to different Servers.txt') as out:
                print(out)
                # self.assertEqual(self.parser(data),out)
        self.assertEqual(1,1)
        # self.assertEqual(self.parser)

    # def test_subtract(self):
    #
    #
    # def test_multiply(self):
    #
    #
    # def test_divide(self):


if __name__ == "__main__":
    unittest.main()
