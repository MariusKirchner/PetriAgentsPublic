__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

import copy
import random

from Backend.BackendStorage.Bacteria.PetriNet.Edge import Edge
from Backend.BackendStorage.Bacteria.PetriNet.Place import Place
from Backend.BackendStorage.Bacteria.PetriNet.Transition import Transition


class PetriNet:

    def __init__(self):
        self.placeIDList = []
        self.transitionIDList = []
        self.edgeIDList = []
        self.placeDict = {}
        self.transitionDict = {}
        self.edgeDict = {}

    def addPlace(self, id, name, tokens, preTransitionIDs, postTransitionIDs):
        self.placeIDList.append(id)
        self.placeDict[id] = Place(id, name, tokens, preTransitionIDs, postTransitionIDs)
        for i in preTransitionIDs:
             if self.edgeIDList == []:
                 if type(i) is tuple:
                     self.addEdge(i[1], i[0], id, "TP")
                 else:
                     self.addEdge(1, i, id, "TP")
             else:
                 if type(i) is tuple:
                     self.addEdge(i[1], i[0], id, "TP")
                 else:
                     self.addEdge(1, i, id, "TP")
        for i in postTransitionIDs:
             if self.edgeIDList == []:
                 if type(i) is tuple:
                     self.addEdge(i[1], id, i[0], "PT")
                 else:
                     self.addEdge(1, id, i, "PT")
             else:
                 if type(i) is tuple:
                     self.addEdge(i[1], id, i[0], "PT")
                 else:
                     self.addEdge(1, id, i, "PT")

    def addTransition(self, id, name, prePlaceIDs, postPlaceIDs, priority=3):
        self.transitionIDList.append(id)
        self.transitionDict[id] = Transition(id, name, [], [], priority)
        tempprePlaceIDs = []
        for i in prePlaceIDs:
            tempprePlaceIDs.append(i)
        tempPostPlaceIDs = []
        for i in postPlaceIDs:
            tempPostPlaceIDs.append(i)
        for i in tempprePlaceIDs:
            if not self.edgeIDList:
                if type(i) is tuple:
                    self.addEdge(i[1], self.placeDict[i[0]], self.transitionDict[id], "PT")
                else:
                    self.addEdge(1, self.placeDict[i], self.transitionDict[id], "PT")
            else:
                if type(i) is tuple:
                    self.addEdge(i[1], self.placeDict[i[0]], self.transitionDict[id], "PT")
                else:
                    self.addEdge(1, self.placeDict[i], self.transitionDict[id], "PT")
        for i in tempPostPlaceIDs:
            if not self.edgeIDList:
                if type(i) is tuple:
                    self.addEdge(i[1], self.transitionDict[id], self.placeDict[i[0]], "TP")
                else:
                    self.addEdge(1, self.transitionDict[id], self.placeDict[i], "TP")
            else:
                if type(i) is tuple:
                    self.addEdge(i[1], self.transitionDict[id], self.placeDict[i[0]], "TP")
                else:
                    self.addEdge(1, self.transitionDict[id], self.placeDict[i], "TP")

    def addEdge(self, weight, source, sink, edgeType):
        self.edgeIDList.append((source.id, sink.id, edgeType))
        self.edgeDict[(source.id, sink.id, edgeType)] = Edge((source.id, sink.id, edgeType), weight, source.id, sink.id, edgeType)
        if type(source) == Place:
            self.placeDict[source.id].addPostTransition(sink.id)
            self.transitionDict[sink.id].addPrePlace(source.id)
        else:
            self.placeDict[sink.id].addPreTransition(source.id)
            self.transitionDict[source.id].addPostPlace(sink.id)

    def getPlaceByName(self, name):
        for i in self.placeIDList:
            if name == self.placeDict[i].name:
                return self.placeDict[i]
        print("Place not found")
        print(name)
        return None

    def getTransitionByName(self, name):
        for i in self.transitionIDList:
            if name == self.transitionDict[i].name:
                return self.transitionDict[i]
        print("Transition not found")
        print(name)
        return None

    def deletePlace(self, id):
        #delete Edges (add references to edges in places and transitions)


        #delete from connected transitions
        for i in (self.placeDict[id].preTransitions):
            self.transitionIDList[i].delPostPlace(id)
        for i in (self.placeDict[id].postTransitions):
            self.transitionIDList[i].delPrePlace(id)

        #delete out of placeIDList and dict

        pass

    def deleteTransition(self):
        pass

    def deleteEdge(self):
        pass

    def printPlaces(self):
        for i in self.placeIDList:
            print("Place " + self.placeDict[i].name + ": " + str(self.placeDict[i].tokens))

    def printTransitions(self):
        for i in self.transitionIDList:
            print("Transition with ID: " + str(i) + " and name: " + self.transitionDict[i].name)

    def printEdges(self):
        for i in self.edgeIDList:
            print("Edge with ID: " + str(i) + " connects preNode with ID: " + str(self.edgeDict[i].source) + " to postNode with ID: " + str(self.edgeDict[i].sink) + " with a weight of: " + str(self.edgeDict[i].weight))

    def isTransitionEnabled(self, transitionID):
        enabled = True
        for prePlaceID in self.transitionDict[transitionID].prePlaceIDs:
            if self.placeDict[prePlaceID].tokens < self.edgeDict[(prePlaceID, transitionID, "PT")].weight:
                enabled = False
                break
        return enabled
# fix for input/transition (input doesnt fire because only look for postTrans of all places)
    def simulateStep(self):
        priorityDict = {}
        listOfPriorities = []
        for transitionID in self.transitionIDList:
            currTransition = self.transitionDict[transitionID]
            if self.isTransitionEnabled(transitionID):
                if currTransition.priority in priorityDict:
                    priorityDict[currTransition.priority].append(transitionID)
                else:
                    priorityDict[currTransition.priority] = [transitionID]
                    listOfPriorities.append(currTransition.priority)
        listOfPriorities.sort()
        for priority in listOfPriorities:
            currTransitionList = priorityDict[priority]
            random.shuffle(currTransitionList)
            for currTrans in currTransitionList:
                if self.isTransitionEnabled(currTrans):
                    for prePlaceID in self.transitionDict[currTrans].prePlaceIDs:
                        self.placeDict[prePlaceID].tokens = self.placeDict[prePlaceID].tokens - self.edgeDict[(prePlaceID, currTrans, "PT")].weight
                    for postPlaceID in self.transitionDict[currTrans].postPlaceIDs:
                        self.placeDict[postPlaceID].tokens = self.placeDict[postPlaceID].tokens + self.edgeDict[(currTrans, postPlaceID, "TP")].weight



        """tempPlaceList = copy.deepcopy(self.placeIDList)
        random.shuffle(tempPlaceList)
        totalFireList = []
        for i in tempPlaceList:
            tempPostTrans = copy.deepcopy(self.placeDict[i].postTransitionIDs)
            activatableTrans = []
            for j in tempPostTrans:
                activatable = True
                for x in self.transitionDict[j].prePlaceIDs:
                    if self.placeDict[x].tokens < self.edgeDict[(x, j, "PT")].weight:
                        activatable = False
                        break
                if activatable:
                    activatableTrans.append(j)
            if activatableTrans:
                transitionToFire = random.choice(activatableTrans)
                if transitionToFire not in totalFireList:
                    totalFireList.append(transitionToFire)
                    for x in self.transitionDict[transitionToFire].prePlaceIDs:
                        self.placeDict[x].tokens = self.placeDict[x].tokens - self.edgeDict[(x, transitionToFire, "PT")].weight
        for i in totalFireList:
            for x in self.transitionDict[i].postPlaceIDs:
                self.placeDict[x].tokens = self.placeDict[x].tokens + self.edgeDict[(i, x, "TP")].weight
                #print("I fired a transition and added tokens somewhere")"""