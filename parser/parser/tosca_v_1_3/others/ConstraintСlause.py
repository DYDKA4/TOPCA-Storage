# # Scalar grammar
# < operator >: < scalar_value >
# # Dual scalar grammar
# < operator >: [ < scalar_value_1 >, < scalar_value_2 >]
# # List grammar
# < operator >: [ < value_1 >, < value_2 >, ..., < value_n >]
# # Regular expression (regex) grammar
# pattern: < regular_expression_value >
# # Schema grammar
# complete

class ConstraintClause:
    def __init__(self):
        self.operator = None
        self.vertex_type_system = 'ConstraintClause'
        self.vid = None
        self.value = None

    def set_operator(self, operator: str):
        self.operator = operator

    def set_value(self, value: str):
        self.value = value


def constraint_clause_parser(data: dict) -> ConstraintClause:
    constraint = ConstraintClause()
    if type(data) != dict:
        constraint.set_operator('equal')
        constraint.set_value(str(data))
    else:
        for operator, scalar_value in data.items():
            constraint.set_operator(operator)
            constraint.set_value(str(scalar_value))
    return constraint
