__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

from Backend.BackendStorage.PAProject import petriAgentProject


class intermediateProject:
    def __init__(self, mainProject, config):
        self.currProject = mainProject
        self.config = config