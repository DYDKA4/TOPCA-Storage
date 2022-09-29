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
import json


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


operator_keynames = {'equal', 'greater_than', 'greater_or_equal', 'less_than', 'less_or_equal', 'in_range',
                     'valid_values', 'length', 'min_length', 'max_length', 'pattern', 'schema'}


def short_notation(constraint: ConstraintClause, data):
    constraint.set_operator('equal')
    constraint.set_value(str(data))


def constraint_clause_parser(data: dict) -> ConstraintClause:
    constraint = ConstraintClause()
    if type(data) != dict:
        if type(data) != str:
            short_notation(constraint, json.dumps(data))
        else:
            short_notation(constraint, data)
    else:
        for operator, scalar_value in data.items():
            if operator not in operator_keynames:
                short_notation(constraint, {operator: scalar_value})
            else:
                short_notation(constraint, json.dumps(data))
    return constraint
