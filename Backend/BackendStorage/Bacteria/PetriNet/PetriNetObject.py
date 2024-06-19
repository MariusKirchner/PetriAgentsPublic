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

    """Creates places and their tokens. Includes Pre- and Posttransitions, 
    but they're not instantiated"""
    def addPlace(self, id, name, tokens, preTransitionIDs, postTransitionIDs):
        self.placeIDList.append(id)
        self.placeDict[id] = Place(id, name, tokens, preTransitionIDs, postTransitionIDs)

        # TODO: preTransitionIDs is empty postTransitionIDs also. For Loop isn't used
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

        # postTransitionID's is empty
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


    """Creates Transitions and includes Pre- and PostPlaces.
    These are added by instantiating. priority=2"""
    def addTransition(self, id, name, prePlaceIDs, postPlaceIDs, priority=2):
        self.transitionIDList.append(id)
        self.transitionDict[id] = Transition(id, name, [], [], priority)
        tempprePlaceIDs = []
        # For loop through prePlaceID's
        # Adds PrePlaces to a temporary list
        for i in prePlaceIDs:
            tempprePlaceIDs.append(i)
        tempPostPlaceIDs = []
        # For loop through PostPlaceID's
        # Adds PostPlaces to a temporary list
        for i in postPlaceIDs:
            tempPostPlaceIDs.append(i)
        # For loop through temporary PrePlaceID's
        # Add Pre- and Posttransition to PlaceObject here?
        for i in tempprePlaceIDs:

            if not self.edgeIDList:
                # TODO if isn't used
                if type(i) is tuple:
                    self.addEdge(i[1], self.placeDict[i[0]], self.transitionDict[id], "PT")
                else:
                    # self.placeDict[id] = Place(id, name, tokens, preTransitionIDs, postTransitionIDs)
                    self.addEdge(1, self.placeDict[i], self.transitionDict[id], "PT")
                    place = self.getPlaceByID(i)

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

    def getPlaceByID(self, placeID):
        for i in self.placeIDList:
            if i == placeID:
                print("Place found: ", self.placeDict[i].name)
                return self.placeDict[i]

        print("Place not found: ", i)

    def getTransitionByName(self, name):
        for i in self.transitionIDList:
            if name == self.transitionDict[i].name:
                return self.transitionDict[i]
        print("Transition not found")
        print(name)
        return None

    def getTransitionByID(self, transID):
        for i in self.transitionIDList:
            if transID == self.transitionDict[i].id:
                print('Transition found with ID:', transID)
                return self.transitionDict[i]



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







    # this function simulates a single step
    """Schritt für Schritt Transitionen. Alle Transitionen anschauen, 
    bestimme welche aktiviert sind, 
    wähle eine die schaltet, schalte diese, fange von vorne an.
    Gleiche Transition kann mehrfach schalten, wenn sie weiter aktiviert ist, auch
    wenn andere Transitionen ebenfalls aktiviert sind."""
    #TODO priority ist für synchronen Schritt?
    def simulateAsynchronousStep(self):
        chooseToFire = []
        priorityDict = {}
        listOfPriorities = []
        chosenTrans = None
        # Go through all transitions and check if they're enabled.
        # Append them to list, to choose randomly which fires.
        for transitionKey in self.transitionDict:
            if self.isTransitionEnabled(transitionKey):
                transToPriority = self.transitionDict[transitionKey]
                chooseToFire.append(transitionKey)
                """Check for priority in enabled transition list,
                add them to dictionary"""
                if transToPriority.priority in priorityDict:
                    priorityDict[transToPriority].append(transitionKey)
                else:
                    priorityDict[transToPriority] = [transitionKey]
                    listOfPriorities.append(transToPriority.priority)

                print('Transition:', transitionKey, " is enabled")
            else:
                print("Transition: ", transitionKey, " is disabled")

        # if no transition is enabled
        if len(chooseToFire) == 0:
            print("No transition enabled. Firing not possible.")
            print('List of enabled transitions: ', chooseToFire)
            print("List with transitions is empty.")
        else:
            # Sort list with priorities
            # Ordered list: highest priority on first index
            listOfPriorities.sort()
            # Check if priority exists and they're different.
            # If different priority's exist: use priority list
            if not self.identical(listOfPriorities):
                print("Transition will be chosen by priority...")
                for key, val in priorityDict.items():
                    print("Key Prio: ", key.priority, "Key Name: ", key.name)
                    # Choose transition with the highest priority <=> listOfPriorities[0]
                    if key.priority == listOfPriorities[0]:
                        chosenTrans = self.getTransitionByID(key.id)

            else:
                # otherwise: choose transition randomly
                # Choose random enabled transition
                transToFire = random.choice(chooseToFire)
                chosenTrans = self.getTransitionByID(transToFire)
                print("Transition will be chosen randomly...")

            print("Chosen transition: ",chosenTrans.name," [ID: ",chosenTrans.id,"]" , " with PrePlaces: ", chosenTrans.prePlaceIDs, " and PostPlaces: ", chosenTrans.postPlaceIDs)
            # Get pre- and post-place. Check if they're existing

            # TODO is no PrePlace exists
            if len(chosenTrans.prePlaceIDs) == 0:
                for j in chosenTrans.postPlaceIDs:
                    postPlace = self.getPlaceByID(j)
                    edgeTP = self.edgeDict[(chosenTrans.id, postPlace.id, 'TP')]
                    weightTP = edgeTP.weight
                    print("TEST")
                    print("No PrePlace but PostPlace. Before firing: ")
                    print("PrePlace: None", "| PrePlaceToken: None", "| PostPlace: ",
                          postPlace.name, "| PostPlaceToken: ", postPlace.tokens, "| WeightPT: No edge, no weight",
                          "| WeightTP: ", weightTP, "| PrePlaceID: None",  "| PostPlaceID", postPlace.id,
                          "| EdgeIDPT: no edge",  "| EdgeIDTP: ", edgeTP.id)

                    postPlace.tokens += weightTP
                    print("No PrePlace, but PostPlace. After firing: ")
                    print("PrePlace: None","| PrePlaceTokens: None","| PostPlace: ",
                          postPlace.name, "| PostPlaceToken: ", postPlace.tokens, "| WeightPT: No edge, no weight",
                           "| WeightTP: ", weightTP, "| PrePlaceID: None",  "| PostPlaceID",
                          postPlace.id, "| EdgeIDPT: None", "| EdgeIDTP", edgeTP.id)

            for i in chosenTrans.prePlaceIDs:

                # If no PostPlace exists, no loop throught empty list needed.
                if len(chosenTrans.postPlaceIDs) == 0:
                    prePlace = self.getPlaceByID(i)
                    edgePT = self.edgeDict[(prePlace.id, chosenTrans.id, 'PT')]
                    weightPT = edgePT.weight
                    print("PrePlace and no PostPlace. Before firing: ")
                    print("PrePlace: ",prePlace.name, "| PrePlaceToken: ", prePlace.tokens, "| PostPlaceTokens: System is leaking", "| WeightPT: ",
                          weightPT, "| WeightTP: None", "| PrePlaceID: ", prePlace.id, "| PostPlaceID: None"
                           "| EdgeIDPT: ", edgePT.id, "| EdgeIDTP: None")
                    # Adjust PrePlace token
                    prePlace.tokens -= weightPT
                    print("PrePlace and no PostPlace. After firing: ")
                    print("PrePlace: ",prePlace.name, "| PrePlaceToken: ", prePlace.tokens, "| PostPlaceTokens: System is leaking", "| WeightPT: ",
                          weightPT, "| WeightTP: None", "| PrePlaceID: ", prePlace.id, "| PostPlaceID: None"
                          "| EdgeIDPT: ", edgePT.id,"| EdgeIDTP: None")
                else:
                    for j in chosenTrans.postPlaceIDs:

                        # 3 cases: Pre- and PostPlace exist, just PrePlace exists, just PostPlace exists
                        if len(chosenTrans.prePlaceIDs) > 0 and len(chosenTrans.postPlaceIDs) > 0:
                            prePlace = self.getPlaceByID(i)
                            postPlace = self.getPlaceByID(j)

                            edgeTP = self.edgeDict[(chosenTrans.id, postPlace.id, 'TP')]
                            edgePT = self.edgeDict[(prePlace.id, chosenTrans.id, 'PT')]

                            weightTP = edgeTP.weight
                            weightPT = edgePT.weight
                            print("Bevore firing:")
                            print("PrePlace: ",prePlace.name, "| PrePlaceToken: ",prePlace.tokens,"| PostPlace: ", postPlace.name,"| PostPlaceToken: ", postPlace.tokens, "| WeightPT: ",weightPT,"| WeightTP: ", weightTP, "| PrePlaceID: " ,prePlace.id,"| PostPlaceID", postPlace.id, "| EdgeIDPT: ",edgePT.id, "| EdgeIDTP: " ,edgeTP.id)
                            # Don't need to check if weight<= number of tokens -> function isEnabled
                            prePlace.tokens -= weightPT
                            postPlace.tokens += weightTP
                            print("After firing: ")
                            print("PrePlace: ",prePlace.name, "| PrePlaceToken: ",prePlace.tokens,"| PostPlace: ", postPlace.name,"| PostPlaceTokens: ", postPlace.tokens, "| WeightPT: ",weightPT,"| WeightTP: ", weightTP,"| PrePlaceID :", prePlace.id,"| PostPlaceID", postPlace.id,"| EdgeIDPT: ", edgePT.id, "| EdgeIDTP: ", edgeTP.id)



    # Check if list entries are identical
    def identical(self, list):
        return all(i == list[0] for i in list)







