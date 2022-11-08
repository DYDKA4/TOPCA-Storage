# <property_name>: <property_value> | { <property_value_expression> }
# complete
import json


class PropertyAssignment:
    def __init__(self, name: str, value):
        self.vid = None
        self.name = name
        if type(value) == list:
            value: str
            value = json.dumps(value)
        self.value = value
        self.vertex_type_system = 'PropertyAssignment'
        self.get_property = None
        self.get_input = None

