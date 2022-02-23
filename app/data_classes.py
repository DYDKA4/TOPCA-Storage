import communication_with_nebula as cwn


class Vertex:
    def __init__(self, name, typeOfVertex = None, requirements=None):
        self.vid = None
        self.session = None
        self.typeOfVertex = typeOfVertex
        self.name = name
        self.requirements = requirements

    def generate_vid(self):
        if self.typeOfVertex is None:
            assert 0, 'typeOfVertex is None'
        else:
            self.vid = self.typeOfVertex + cwn.number_of_entities(cwn.chose_of_space(), self.typeOfVertex)

    def set_vid(self, vid):
        self.vid = vid


a = Vertex(name='YA',)
a.generate_vid()
print(a.vid)