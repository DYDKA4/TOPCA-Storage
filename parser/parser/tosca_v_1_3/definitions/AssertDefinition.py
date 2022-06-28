from parser.parser.tosca_v_1_3.others.ConstraintСlause import constraint_clause_parser


class AssertDefinition:
    def __init__(self, attribute_name: str):
        self.vid = None
        self.attribute_name = attribute_name
        self.constraint_clauses = []
        self.vertex_type_system = 'AssertDefinition'


def assert_definition_parser(attribute_name, constraint_clauses) -> AssertDefinition:
    assert_definition = AssertDefinition(attribute_name)
    for conditions_clauses in constraint_clauses:
        assert_definition.constraint_clauses.append(constraint_clause_parser(conditions_clauses))
    return  assert_definition