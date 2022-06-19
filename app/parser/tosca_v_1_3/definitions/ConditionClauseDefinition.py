# And clause
# and: <list_of_condition_clause_definition>

# Or clause
# or: <list_of_condition_clause_definition>

# Not clause
# not: <list_of_condition_clause_definition>

# Direct assertion definition
# <attribute_name>: <list_of_constraint_clauses>
from app.parser.tosca_v_1_3.others.ConstraintСlause import constraint_clause_parser


class ConditionClauseDefinition:
    def __init__(self, type_condition: str):
        self.vid = None
        self.type = type_condition
        self.operands = {
            'not': [],
            'or': [],
            'and': [],
            'assert': []
        }
        self.vertex_type_system = 'ConditionClauseDefinition'


def sub_parser(condition_clause, condition, operation):
    operand = ConditionClauseDefinition(operation)
    for sub_condition in condition_clause.get(operation):
        sub_condition_structure = None
        for sub_condition_key, sub_condition_value in sub_condition.items():
            if sub_condition_key not in {'and', 'or', 'not'}:
                assert_dict = {sub_condition_key: []}
                for constraint_clauses in sub_condition_value:
                    assert_dict[sub_condition_key]. \
                        append(constraint_clause_parser(constraint_clauses))
                    operand.operands['assert'].append(assert_dict)
            else:
                operand_2 = condition_clause_definition_parser(sub_condition_key,
                                                               sub_condition)
                sub_condition_structure = ConditionClauseDefinition(operation)
                sub_condition_structure.operands[sub_condition_key].append(operand_2)
        if sub_condition_structure:
            condition.operands[operation].append(sub_condition_structure)
    if operand.operands['assert']:
        condition.operands[operation].append(operand)
    pass


def condition_clause_definition_parser(type_condition: str, data: dict) -> ConditionClauseDefinition:
    condition = ConditionClauseDefinition(type_condition)
    if type(data) == dict:
        if data.get(type_condition):
            for condition_clause in data.get(type_condition):
                for key in condition_clause.keys():
                    if key == 'not':
                        sub_parser(condition_clause, condition, 'not')

                    elif key == 'or':
                        sub_parser(condition_clause, condition, 'or')

                    elif key == 'and':
                        sub_parser(condition_clause, condition, 'and')
                    else:
                        for attribute_name, constraint_clauses in condition_clause.items():
                            assert_dict = {attribute_name: []}
                            for conditions_clauses in constraint_clauses:
                                assert_dict[attribute_name].append(constraint_clause_parser(conditions_clauses))
                            condition.operands['assert'].append(assert_dict)
    return condition
