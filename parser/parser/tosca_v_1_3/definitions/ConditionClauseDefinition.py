# And clause
# and: <list_of_condition_clause_definition>

# Or clause
# or: <list_of_condition_clause_definition>

# Not clause
# not: <list_of_condition_clause_definition>

# Direct assertion definition
# <attribute_name>: <list_of_constraint_clauses>
from parser.parser.tosca_v_1_3.definitions.AssertDefinition import assert_definition_parser
from parser.parser.tosca_v_1_3.others.ConstraintСlause import constraint_clause_parser


class ConditionClauseDefinition:
    def __init__(self, type_condition: str):
        self.vid = None
        self.type = type_condition
        self.condition_not = []
        self.condition_or = []
        self.condition_and = []
        self.condition_assert = []
        self.vertex_type_system = 'ConditionClauseDefinition'





def condition_clause_definition_parser(type_condition: str, data: dict) -> ConditionClauseDefinition:
    condition = ConditionClauseDefinition(type_condition)
    if type(data) == dict:
        if data.get(type_condition):
            for condition_clause in data.get(type_condition):
                for key in condition_clause.keys():
                    if key == 'not':
                        vertex = condition_clause_definition_parser(key, condition_clause)
                        condition.condition_not.append(vertex)
                        # sub_parser(condition_clause, condition, 'not')

                    elif key == 'or':
                        vertex = condition_clause_definition_parser(key, condition_clause)
                        condition.condition_or.append(vertex)
                        # sub_parser(condition_clause, condition, 'or')

                    elif key == 'and':
                        vertex = condition_clause_definition_parser(key, condition_clause)
                        condition.condition_and.append(vertex)
                        # sub_parser(condition_clause, condition, 'and')
                    else:
                        for attribute_name, constraint_clauses in condition_clause.items():
                            assert_dict = {attribute_name: []}
                            condition.condition_assert.append(assert_definition_parser(attribute_name,
                                                                                       constraint_clauses))
                            # for conditions_clauses in constraint_clauses:
                            #     condition.condition_assert.append(constraint_clause_parser(conditions_clauses))
                            #     # assert_dict[attribute_name].append(constraint_clause_parser(conditions_clauses))
                            # condition.operands['assert'].append(assert_dict)
    return condition
