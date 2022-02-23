

class Vertex:
    def __init__(self, name, typeOfVertex, requirements, vid=None):
        self.name = name
        self.type = typeOfVertex
        self.requirements = requirements
        self.vid = vid

class AssignationOfProperties(Vertex):
