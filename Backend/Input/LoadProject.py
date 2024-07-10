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
    for bac in doc.getElementsByTagName("bacteria")[0].childNodes:
        #print(bac.toxml())
        tempPetri = PetriNet()
        for place in bac.childNodes[0].childNodes:
            tempPetri.addPlace(place.childNodes[0].childNodes[0].data, place.childNodes[1].childNodes[0].data, place.childNodes[2].childNodes[0].data, [], [])
            #print(place.toxml())
        for transition in bac.childNodes[1].childNodes:
            tempPetri.addTransition(transition.childNodes[0].childNodes[0].data, transition.childNodes[1].childNodes[0].data, [], [])
            #print(transition.toxml())
        for edge in bac.childNodes[2].childNodes:
            if edge.childNodes[4].childNodes[0].data == "PT":
                tempPetri.addEdge(edge.childNodes[1].childNodes[0].data, tempPetri.placeDict[edge.childNodes[2].childNodes[0].data], tempPetri.transitionDict[edge.childNodes[3].childNodes[0].data], edge.childNodes[4].childNodes[0].data)
            else:
                tempPetri.addEdge(edge.childNodes[1].childNodes[0].data, tempPetri.transitionDict[edge.childNodes[2].childNodes[0].data], tempPetri.placeDict[edge.childNodes[3].childNodes[0].data], edge.childNodes[4].childNodes[0].data)
            #print(edge.toxml())
        newProject.addBacteria(bac.tagName, tempPetri)
    return newProject