__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

import json
from xml.dom import minidom

from Backend.BackendStorage.Bacteria.PetriNet.PetriNetObject import PetriNet
from Backend.BackendStorage.PAProject import petriAgentProject


def loadProject(filehandler):
    print("Loading")
    #change project values according to new info
    newProject = petriAgentProject()
    doc = minidom.parse(filehandler)
    newProject.maxXCor = doc.getElementsByTagName("maxXCor")[0].childNodes[0].data
    newProject.maxYCor = doc.getElementsByTagName("maxYCor")[0].childNodes[0].data
    newProject.ticks = doc.getElementsByTagName("Ticks")[0].childNodes[0].data
    newProject.lrCont = doc.getElementsByTagName("lrCont")[0].childNodes[0].data
    newProject.tbCont = doc.getElementsByTagName("tbCont")[0].childNodes[0].data
    newProject.diffRate = doc.getElementsByTagName("diffRate")[0].childNodes[0].data
    newProject.diffBool = doc.getElementsByTagName("diffBool")[0].childNodes[0].data
    newProject.flowRate = doc.getElementsByTagName("flowRate")[0].childNodes[0].data
    newProject.flowDir = doc.getElementsByTagName("flowDir")[0].childNodes[0].data
    newProject.flowBool = doc.getElementsByTagName("flowBool")[0].childNodes[0].data
    newProject.molOutFlowNorth = doc.getElementsByTagName("molOutFlowNorth")[0].childNodes[0].data
    newProject.molOutFlowEast = doc.getElementsByTagName("molOutFlowEast")[0].childNodes[0].data
    newProject.molOutFlowSouth = doc.getElementsByTagName("molOutFlowSouth")[0].childNodes[0].data
    newProject.molOutFlowWest = doc.getElementsByTagName("molOutFlowWest")[0].childNodes[0].data
    newProject.bacOutFlowNorth = doc.getElementsByTagName("bacOutFlowNorth")[0].childNodes[0].data
    newProject.bacOutFlowEast = doc.getElementsByTagName("bacOutFlowEast")[0].childNodes[0].data
    newProject.bacOutFlowSouth = doc.getElementsByTagName("bacOutFlowSouth")[0].childNodes[0].data
    newProject.bacOutFlowWest = doc.getElementsByTagName("bacOutFlowWest")[0].childNodes[0].data
    newProject.bacFlowRate = doc.getElementsByTagName("bacFlowRate")[0].childNodes[0].data
    newProject.bacDiffRate = doc.getElementsByTagName("bacDiffRate")[0].childNodes[0].data
    newProject.diffmode = doc.getElementsByTagName("diffmode")[0].childNodes[0].data
    newProject.bacRotDiff = doc.getElementsByTagName("bacRotDiff")[0].childNodes[0].data
    newProject.bacVelo = doc.getElementsByTagName("bacVelo")[0].childNodes[0].data
    newProject.diffConstant = doc.getElementsByTagName("diffConstant")[0].childNodes[0].data
    newProject.patchLength = doc.getElementsByTagName("patchLength")[0].childNodes[0].data
    newProject.timePerTickDefault = doc.getElementsByTagName("timePerTickDefault")[0].childNodes[0].data
    newProject.patchColor = doc.getElementsByTagName("patchColor")[0].childNodes[0].data
    newProject.patchColorIncrement = doc.getElementsByTagName("patchColorIncrement")[0].childNodes[0].data
    newProject.patchColorMolecule = doc.getElementsByTagName("patchColorMolecule")[0].childNodes[0].data

    for bac in doc.getElementsByTagName("Bacteria"):
        tempPetri = PetriNet()
        for place in bac.getElementsByTagName("Place"):
            tempPetri.addPlace(place.childNodes[1].childNodes[0].data, place.childNodes[3].childNodes[0].data, place.childNodes[5].childNodes[0].data, [], [])
            #print(place.toxml())
        for transition in bac.getElementsByTagName("Transition"):
            tempPetri.addTransition(transition.childNodes[1].childNodes[0].data, transition.childNodes[3].childNodes[0].data, [], [])
            #print(transition.toxml())
        for edge in bac.getElementsByTagName("Edge"):
            if edge.childNodes[4].childNodes[0].data == "PT":
                tempPetri.addEdge(edge.childNodes[1].childNodes[0].data, tempPetri.placeDict[edge.childNodes[3].childNodes[0].data], tempPetri.transitionDict[edge.childNodes[5].childNodes[0].data], edge.childNodes[7].childNodes[0].data)
            else:
                tempPetri.addEdge(edge.childNodes[1].childNodes[0].data, tempPetri.transitionDict[edge.childNodes[3].childNodes[0].data], tempPetri.placeDict[edge.childNodes[5].childNodes[0].data], edge.childNodes[7].childNodes[0].data)
            #print(edge.toxml())
        print(bac.childNodes)
        newProject.addBacteria(bac.childNodes[1].childNodes[0].data, tempPetri)
        newProject.bacteriaNameDict[bac.childNodes[1].childNodes[0].data].MOI = bac.childNodes[3].childNodes[0].data
        newProject.bacteriaNameDict[bac.childNodes[1].childNodes[0].data].shapeRepresentation = bac.childNodes[5].childNodes[0].data
        newProject.bacteriaNameDict[bac.childNodes[1].childNodes[0].data].colorRepresentation = json.loads(bac.childNodes[7].childNodes[0].data)


    for flow in doc.getElementsByTagName("Flow"):
        newProject.addinoutFlow(newProject.dictOfEnvironmentMolecules[flow.childNodes[1].childNodes[0].data], bool(flow.childNodes[3].childNodes[0].data), int(flow.childNodes[5].childNodes[0].data), int(flow.childNodes[7].childNodes[0].data), int(flow.childNodes[9].childNodes[0].data), int(flow.childNodes[11].childNodes[0].data), int(flow.childNodes[13].childNodes[0].data), int(flow.childNodes[15].childNodes[0].data), int(flow.childNodes[17].childNodes[0].data))

    for envmol in doc.getElementsByTagName("EnvironmentMolecule"):
        print(envmol.childNodes[3].childNodes[0].data)
        newProject.dictOfEnvironmentMolecules[envmol.childNodes[1].childNodes[0].data].distArea = json.loads(envmol.childNodes[3].childNodes[0].data)
        newProject.dictOfEnvironmentMolecules[envmol.childNodes[1].childNodes[0].data].distAmount = envmol.childNodes[5].childNodes[0].data
    return newProject