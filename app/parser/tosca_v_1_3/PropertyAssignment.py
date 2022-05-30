# <property_name>: <property_value> | { <property_value_expression> }

class PropertyAssignment:
    def __init__(self, name: str, value: str):
        self.vid = None
        self.name = name
        self.value = value
        self.vertex_type_system = 'PropertyAssignment'
