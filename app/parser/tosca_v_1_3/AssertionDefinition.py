# <attribute_name>: <list_of_constraint_clauses>
from app.parser.tosca_v_1_3.ConstraintСlause import constraint_clause_parser


class AssertionDefinition:
    def __init__(self, attribute_name):
        self.vid = None
        self.vertex_type_system = 'AssertionDefinition'
        self.list_of_constraint_clauses = []
        self.attribute_name = attribute_name


def assertion_definition(attribute_name: str,data: dict) -> AssertionDefinition:
    assertion = AssertionDefinition(attribute_name)
    for constraint_clause in data:
        assertion.list_of_constraint_clauses.append(constraint_clause_parser(constraint_clause))
    return assertion
