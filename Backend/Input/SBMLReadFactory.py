__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

from Backend.BackendStorage.Bacteria.PetriNet.PetriNetObject import PetriNet
import libsbml

def readSBML(filename):
    tempPetri = PetriNet()
    reader = libsbml.SBMLReader()
    document = reader.readSBMLFromFile(filename)
    model = document.getModel()
    currid = 0
    for s in model.getListOfSpecies():
        tempPetri.addPlace(currid, s.getName(), s.getInitialAmount(), [], [])
        currid += 1
    tempPetri.printPlaces()
    for r in model.getListOfReactions():
        tempPrePlaceList = []
        for i in r.getListOfReactants():
            for s in model.getListOfSpecies():
                if s.getId() == i.getSpecies():
                    tempName = s.getName()
                    break
            id = tempPetri.getPlaceByName(tempName).id
            if i.getStoichiometry() != 1:
                tempTuple = (id, i.getStoichiometry())
                tempPrePlaceList.append(tempTuple)
            else:
                tempPrePlaceList.append(id)
        tempPostPlaceList = []
        for i in r.getListOfProducts():
            for s in model.getListOfSpecies():
                if s.getId() == i.getSpecies():
                    tempName = s.getName()
                    break
            id = tempPetri.getPlaceByName(tempName).id
            if i.getStoichiometry() != 1:
                tempTuple = (id, i.getStoichiometry())
                tempPostPlaceList.append(tempTuple)
            else:
                tempPostPlaceList.append(id)
        print("test")
        print(r.getName().split("_")[-1])
        if r.getName().split("_")[-1].isdigit():
            tempPetri.addTransition(currid, r.getName(), tempPrePlaceList, tempPostPlaceList, int(r.getName().split("_")[-1]))
        else:
            tempPetri.addTransition(currid, r.getName(), tempPrePlaceList, tempPostPlaceList)
        currid += 1
    tempPetri.printPlaces()
    tempPetri.printTransitions()
    tempPetri.printEdges()
    return tempPetri
