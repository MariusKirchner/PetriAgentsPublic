import copy
from Backend.BackendStorage.Bacteria.IndividualBacteria import individualBacteria


class bacteria:
    def __init__(self, id, name, petriNet, MOI):
        self.ID = id
        self.name = name
        self.petriNet = petriNet
        self.dictOfBehPlaces = {}
        self.dictOfEnvPlaces = {}
        self.listOfBehPlaceIDs = []
        self.listOfEnvPlaces = []
        self.MOI = MOI
        self.listOfIndividuals = []
        self.dictOfIndividuals = {}
        self.colorRepresentation = [0, 0, 0]
        self.shapeRepresentation = "bacteria 1"
        self.flagella = False
        for placeID in petriNet.placeIDList:
            if petriNet.placeDict[placeID].name[:4] == "Env_":
                self.listOfEnvPlaces.append(petriNet.placeDict[placeID].name[4:])
                self.dictOfEnvPlaces[placeID] = petriNet.placeDict[placeID].name[4:]
            elif petriNet.placeDict[placeID].name[:4] == "Beh_":
                self.listOfBehPlaceIDs.append(placeID)
                if petriNet.placeDict[placeID].name[4:] == "Repl" or petriNet.placeDict[placeID].name[4:] == "Replication" or petriNet.placeDict[placeID].name[4:] == "repl":
                    self.dictOfBehPlaces[placeID] = "Replication"
                elif petriNet.placeDict[placeID].name[4:] == "Size" or petriNet.placeDict[placeID].name[4:] == "size":
                    self.dictOfBehPlaces[placeID] = "Size"
                elif petriNet.placeDict[placeID].name[4:] == "Move" or petriNet.placeDict[placeID].name[4:] == "move":
                    self.dictOfBehPlaces[placeID] = "Move"
                elif petriNet.placeDict[placeID].name[4:] == "Death" or petriNet.placeDict[placeID].name[4:] == "death":
                    self.dictOfBehPlaces[placeID] = "Death"
                else:
                    self.dictOfBehPlaces[placeID] = "None"
        print("added a bacteria with name" + self.name)

    def changeMOI(self, newMOI):
        self.MOI = newMOI

    def addIndividual(self, ID):
        tempIndividual = individualBacteria(ID, copy.deepcopy(self.petriNet), self.ID)
        self.dictOfIndividuals[ID] = tempIndividual
        self.listOfIndividuals.append(ID)

    def delIndividual(self, ID):
        self.listOfIndividuals.remove(ID)
        self.dictOfIndividuals.pop(ID)
