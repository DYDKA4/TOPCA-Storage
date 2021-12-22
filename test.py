import unittest
from app import json_parser
import json


# class TestJsonParser(unittest.TestCase):
#
#     # setUp method is overridden from the parent class TestCase
#
#     def Multiple_Block_Storage_attached_to_different_Servers(self):
#         with open('tests/test_inputs/Multiple Block Storage attached to different Servers.json') as f:
#             data = json.load(f)
#             with open('tests/results/Multiple Block Storage attached to different Servers.txt') as out:
#                 print(out)
#                 self.assertEqual(self.parser(data), out)
#         self.assertEqual(1, 1)
#         # self.assertEqual(self.parser)
#
#     def ABOBA(self):
#         self.assertEqual(1, 2)
#     #
#
# def test_multiply(self):
#
#
# def test_divide(self):


class TestJsonParser(unittest.TestCase):

    def test_Multiple_Block_Storage_attached_to_different_Servers(self):
        with open('tests/test_inputs/Multiple Block Storage attached to different Servers.json') as f:
            data = json.load(f)
            with open('tests/results/Multiple Block Storage attached to different Servers.txt') as out:
                result = out.read()
                answer = str(json_parser.parser(data))
                self.assertEqual(result, answer)

    def test_Server_bound_to_a_new_network(self):
        with open('tests/test_inputs/Server bound to a new network.json') as f:
            data = json.load(f)
            with open('tests/results/Server bound to a new network.txt') as out:
                result = out.read()
                answer = str(json_parser.parser(data))
                self.assertEqual(result, answer)

    def test_Server_bound_to_three_networks(self):
        with open('tests/test_inputs/Server bound to three networks.json') as f:
            data = json.load(f)
            with open('tests/results/Server bound to three networks.txt') as out:
                result = out.read()
                answer = str(json_parser.parser(data))
                self.assertEqual(result, answer)

    def test_Single_Block_Storage_shared_by_2Tier_Application_with_custom_AttachesTo_Type_and_implied_relationships(
            self):
        with open('tests/test_inputs/Single Block Storage shared by 2-Tier Application with custom AttachesTo'
                  ' Type and implied relationships.json') as f:
            data = json.load(f)
            with open('tests/results/Single Block Storage shared by 2-Tier Application with custom AttachesTo'
                      ' Type and implied relationships.txt') as out:
                result = out.read()
                answer = str(json_parser.parser(data))
                self.assertEqual(result, answer)

    def test_Two_servers_bound_to_a_single_network(self):
        with open('tests/test_inputs/Two servers bound to a single network.json') as f:
            data = json.load(f)
            with open('tests/results/Two servers bound to a single network.txt') as out:
                result = out.read()
                answer = str(json_parser.parser(data))
                self.assertEqual(result, answer)

    def test_Using_a_custom_AttachesTo_Relationship_Type(self):
        with open('tests/test_inputs/Using-a-custom-AttachesTo-Relationship-Type.json') as f:
            data = json.load(f)
            with open('tests/results/Using-a-custom-AttachesTo-Relationship-Type.txt') as out:
                result = out.read()
                answer = str(json_parser.parser(data))
                self.assertEqual(result, answer)

    def test_Using_Relationship_Templat_of_type_AttachesTo(self):
        with open('tests/test_inputs/Using-Relationship-Templat-of-type-AttachesTo.json') as f:
            data = json.load(f)
            with open('tests/results/Using-Relationship-Templat-of-type-AttachesTo.txt') as out:
                result = out.read()
                answer = str(json_parser.parser(data))
                self.assertEqual(result, answer)

    def test_Using_the_normative_AttachesTo_Relationship_Type(self):
        with open('tests/test_inputs/Using-the-normative-AttachesTo-Relationship-Type.json') as f:
            data = json.load(f)
            with open('tests/results/Using-the-normative-AttachesTo-Relationship-Type.txt') as out:
                result = out.read()
                answer = str(json_parser.parser(data))
                self.assertEqual(result, answer)

    def test_WebServer_DBMS_2_Nodejs_with_PayPal_Sample_App_and_MongoDB_on_separate_instances(self):
        with open('tests/test_inputs/WebServer-DBMS 2 Nodejs with PayPal Sample App and MongoDB'
                  ' on separate instances.json') as f:
            data = json.load(f)
            with open('tests/results/WebServer-DBMS 2 Nodejs with PayPal Sample App and MongoDB'
                      ' on separate instances.txt') as out:
                result = out.read()
                answer = str(json_parser.parser(data))
                self.assertEqual(result, answer)

    def test_WordPress_MySQL_single_instance(self):
        with open('tests/test_inputs/WordPress + MySQL, single instance.json') as f:
            data = json.load(f)
            with open('tests/results/WordPress + MySQL, single instance.txt') as out:
                result = out.read()
                answer = str(json_parser.parser(data))
                self.assertEqual(result, answer)


if __name__ == "__main__":
    unittest.main()
