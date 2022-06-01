# Short notation
# <property_name>: <property_constraint_clause>

# <property_name>:
#   - <property_constraint_clause_1>
#   - ...
#   - <property_constraint_clause_n>
from app.parser.tosca_v_1_3.ConstraintСlause import ConstraintClause, constraint_clause_parser


class PropertyFilterDefinition:
    def __init__(self, name: str):
        self.vid = None
        self.name = name
        self.vertex_type_system = 'PropertyFilterDefinition'
        self.property_constraint = None
        self.property_constraint_list = []

    def set_property_constraint(self, property_constraint: ConstraintClause):
        self.property_constraint = property_constraint

    def add_property_constraint_list(self, property_constraint_list: ConstraintClause):
        self.property_constraint_list.append(property_constraint_list)


def property_filter_definition_parser(name: str, data: dict) -> PropertyFilterDefinition:
    property_filter = PropertyFilterDefinition(name)
    if type(data) == list:
        for property_constraint_clause in data:
            property_filter.add_property_constraint_list(constraint_clause_parser(property_constraint_clause))
    else:
        property_filter.set_property_constraint(constraint_clause_parser(data))
    return property_filter

