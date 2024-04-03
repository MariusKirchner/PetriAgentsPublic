__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

class Edge:
    def __init__(self, id, weight, source, sink, edgeType):
        self.id = id
        self.weight = weight
        self.source = source
        self.sink = sink
        self.edgeType = edgeType
