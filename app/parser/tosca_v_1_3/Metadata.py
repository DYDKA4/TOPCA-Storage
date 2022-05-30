#     <map of string>
# complete

class Metadata:
    def __init__(self, name: str, value: str):
        self.vid = None
        self.name = name
        self.value = value
        self.vertex_type_system = 'Metadata'
