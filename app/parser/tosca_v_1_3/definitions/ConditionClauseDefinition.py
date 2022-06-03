# And clause
# and: <list_of_condition_clause_definition>

# Or clause
# or: <list_of_condition_clause_definition>

# Not clause
# not: <list_of_condition_clause_definition>

# Direct assertion definition
# <attribute_name>: <list_of_constraint_clauses>
from app.parser.tosca_v_1_3.definitions.AssertionDefinition import assertion_definition


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


def condition_clause_definition_parser(type_condition: str, data: dict) -> ConditionClauseDefinition:
    condition = ConditionClauseDefinition(type_condition)
    for condition_clause in data:
        if condition_clause.get('not'):
            operand = condition_clause_definition_parser('not', condition_clause.get('not'))
            condition.operands['not'].append(operand)
        elif condition_clause.get('or'):
            operand = condition_clause_definition_parser('or', condition_clause.get('or'))
            condition.operands['or'].append(operand)
        elif condition_clause.get('and'):
            operand = condition_clause_definition_parser('and', condition_clause.get('and'))
            condition.operands['and'].append(operand)
        else:
            for attribute_name, attribute_value in condition_clause.items():
                condition.operands['assert'].append(assertion_definition(attribute_name,attribute_value))

    return condition
