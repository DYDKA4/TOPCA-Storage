# # Scalar grammar
# < operator >: < scalar_value >
# # Dual scalar grammar
# < operator >: [ < scalar_value_1 >, < scalar_value_2 >]
# # List grammar
# < operator >: [ < value_1 >, < value_2 >, ..., < value_n >]
# # Regular expression (regex) grammar
# pattern: < regular_expression_value >
# # Schema grammar
class Constraint:
    def __init__(self):
        self.operator = None
        self.vertex_type_system = 'ConstraintClause'
        self.vid = None
        self.value = None

    def set_operator(self, operator: str):
        self.operator = operator

    def set_value(self, value: str):
        self.value = value


def constraint_parser(data: dict) -> Constraint:
    constraint = Constraint()
    for operator, scalar_value in data.items():
        constraint.set_operator(operator)
        constraint.set_value(str(scalar_value))
    return constraint
