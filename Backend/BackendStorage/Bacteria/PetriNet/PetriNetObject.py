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
        print("addPlaceStart: ", self.getPlaceByID(id).name)
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
        print("addPlaceEnd: ", postTransitionIDs, self.edgeIDList)
        # postTransitionID's is empty
        for i in postTransitionIDs:
            print("addPlace: ", postTransitionIDs)
            if self.edgeIDList == []:
                if type(i) is tuple:
                    print("addPlacePOST: ", i[1], id, i[0])
                    self.addEdge(i[1], id, i[0], "PT")
                else:
                    self.addEdge(1, id, i, "PT")
            else:
                if type(i) is tuple:
                    self.addEdge(i[1], id, i[0], "PT")
                else:
                    self.addEdge(1, id, i, "PT")


    def addTransition(self, id, name, prePlaceIDs, postPlaceIDs, priority=2):
        self.transitionIDList.append(id)
        self.transitionDict[id] = Transition(id, name, [], [], priority)
        tempprePlaceIDs = []
        # For loop through prePlaceID's
        # Adds PrePlaces to a temporary list
        for i in prePlaceIDs:
            tempprePlaceIDs.append(i)
            print("TEST1 PRE: ", i)
            if type(i) is tuple:
                print("TUPEL: ", i[1])
        tempPostPlaceIDs = []
        print("prePlaceIDs: ", prePlaceIDs, " tempprePlaceIDs: ", tempprePlaceIDs)
        # For loop through PostPlaceID's
        # Adds PostPlaces to a temporary list
        for i in postPlaceIDs:
            tempPostPlaceIDs.append(i)
            print("TEST2 POST: ", i)
        print("postPlaceIDs: ", postPlaceIDs, " temppostPlaceIDs: ", tempPostPlaceIDs)
        # For loop through temporary PrePlaceID's
        for i in tempprePlaceIDs:
            print("TEST3 PRE: ", i, self.edgeIDList, tempprePlaceIDs)
            #
            if not self.edgeIDList:
                # TODO if isn't used
                if type(i) is tuple:
                    self.addEdge(i[1], self.placeDict[i[0]], self.transitionDict[id], "PT")
                    print("Edge", i, i[1])
                else:
                    self.addEdge(1, self.placeDict[i], self.transitionDict[id], "PT")
                    print("EdgeELSE", self.placeDict[i].name, self.transitionDict[id].name)
            else:
                print("Edge2")
                if type(i) is tuple:
                    print("Edge3 TUPEL: ", i[1])
                    self.addEdge(i[1], self.placeDict[i[0]], self.transitionDict[id], "PT")
                    print("Edge2 if: ",self.placeDict[i[0]].name, self.transitionDict[id].name )
                else:
                    self.addEdge(1, self.placeDict[i], self.transitionDict[id], "PT")
                    print("Edge2 else: ",self.placeDict[i].name, self.transitionDict[id].name)
        print("TEST5: ", tempPostPlaceIDs)
        for i in tempPostPlaceIDs:

            print("TEST5 POST: ", i, self.edgeIDList)
            if not self.edgeIDList:
                print("TEST4 POST: ", i, self.edgeIDList)
                if type(i) is tuple:
                    self.addEdge(i[1], self.transitionDict[id], self.placeDict[i[0]], "TP")
                else:
                    self.addEdge(1, self.transitionDict[id], self.placeDict[i], "TP")
            else:
                if type(i) is tuple:
                    self.addEdge(i[1], self.transitionDict[id], self.placeDict[i[0]], "TP")
                else:
                    self.addEdge(1, self.transitionDict[id], self.placeDict[i], "TP")

        print("AddTransition: ", tempprePlaceIDs)

    def addEdge(self, weight, source, sink, edgeType):
        self.edgeIDList.append((source.id, sink.id, edgeType))
        self.edgeDict[(source.id, sink.id, edgeType)] = Edge((source.id, sink.id, edgeType), weight, source.id, sink.id, edgeType)
        print("in addEdge: ", source.id, sink.id, edgeType)
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
                print('TransID',transID)
                return self.transitionDict[i]

            #return print("Transition ID not found")

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

    # Finds edge between
    # TODO (0, 1, 'TP') gefunden gibt kein 0 1 PT. Nicht sicher verstanden
    def findEdge(self, pre, post):
        foundSource = [x[0] for x in self.edgeIDList]
        foundSink = [y[1] for y in self.edgeIDList]
        if pre == None:
            pass


        print("In findEdge Pre ", pre, "post ", post)

        print(foundSource)
        print(foundSink)
        for i in range(len(foundSource)-1):
            numSource = foundSource[i]
            numSink = foundSink[i]

            if numSource == pre and numSink == post:
                print("SourceID:", numSource," SinkID:", numSink)
                print("Output: ", self.edgeIDList[i])

                return self.edgeIDList[i]

        print("Edge not found")

        return self.edgeDict


    # this function simulates a single step
    """Schritt für Schritt Transitionen. Alle Transitionen anschauen, 
    bestimme welche aktiviert sind, 
    wähle eine die schaltet, schalte diese, fange von vorne an.
    Gleiche Transition kann mehrfach schalten, wenn sie weiter aktiviert ist, auch
    wenn andere Transitionen ebenfalls aktiviert sind."""
    #TODO priority ist für synchronen Schritt?
    def simulateAsynchronousStep(self):
        chooseToFire = []
        # Go through all transitions and check if they're enabled.
        # Append them to list, to choose randomly which fires.
        #TODO is random choosing okay?

        for transitionKey in self.transitionDict:
            if self.isTransitionEnabled(transitionKey):
                chooseToFire.append(transitionKey)
                print('Transition:', transitionKey, " is enabled")
            else:
                print("Transition: ", transitionKey, " is disabled")

        # TODO: Choose randomly? which transition fires.

        if len(chooseToFire) == 0:
            print("No transition enabled. Firing not possible.")
            print('List of enabled transitions: ', chooseToFire)
            print("List with transitions is empty.")
        else:
            # Choose random enabled transition
            transToFire = random.choice(chooseToFire)
            chosenTrans = self.getTransitionByID(transToFire)
            # Get pre- and post-place. Check if they're existing
            print("Transition ",chosenTrans.id , "PrePlaces : ", chosenTrans.prePlaceIDs)
            print("TRANSITION Inhalt: ", chosenTrans.prePlaceIDs)

            # Query if PrePlace does exist, otherwise choose different transition
            if len(chosenTrans.prePlaceIDs) >= 1:

                #try:
                    # Choose prePlace randomly
                    prePlace = self.getPlaceByID(random.choice(chosenTrans.prePlaceIDs))
                    print("PrePlace", prePlace.name,"has ", prePlace.tokens, " tokens")
                    print("PrePlace Test: ", prePlace)



                    # Check if PostPlace exists, otherwise choose new transition
                    if len(chosenTrans.postPlaceIDs) >= 1:

                            # Choose random PostPlace and get place object
                            postPlace = self.getPlaceByID(random.choice(chosenTrans.postPlaceIDs))
                            print("PostPlace", postPlace.name, "has ", postPlace.tokens, " tokens")

                            try:
                                sourcePlace = self.edgeDict.keys()
                               # print("All edges: ", sourcePlace)
                                edge = self.findEdge(prePlace.id, postPlace.id)
                                weight = self.edgeDict[edge].weight
                                #print("TRY", edge)
                                print("Weightausgabe: ", weight, edge)
                                # If edge weight <= prePlaceToken update pre- and post-place
                                if weight <= prePlace.tokens:
                                    print("Bevore firing PrePlace", prePlace.tokens, " PostPlace", postPlace.tokens)
                                    # Updating pre- and post-places
                                    prePlace.tokens -= weight
                                    postPlace.tokens += weight
                                    print("After firing PrePlace", prePlace.tokens, " ", "PostPlace", postPlace.tokens)
                                    return prePlace, postPlace
                                else:
                                    print("No firing possible.")
                            except (AttributeError, TypeError):
                                if AttributeError:
                                    print("Attribute error")
                                if TypeError:
                                    print("TypeError")



                    else:
                        print("No postPlace available")

                        # If no PostPlace exists, only update PrePlace
                        print("No PostPlace found. System is leaking.")
                        print("PrePlace before update: ", prePlace.tokens)
                        prePlace.tokens -=1

                        print("Updated PrePlace: ", prePlace.tokens)

               # except IndexError:
                   # print("No prePlace available")
            # If no PrePlace exists, transition is source.
            # Only update PostPlace
            else:
                # Choose random PostPlace of transition
                # Add query to check for edge weigh
                print("No prePlace available")

                postPlace = self.getPlaceByID(random.choice(chosenTrans.postPlaceIDs))
                print("PostPlace token bevore: ", postPlace.tokens, postPlace.name)
                # Update PostPlace token
                prePlace = None
                #postPlace.tokens += 1
                if prePlace is None:
                    print("HIER")

                    #edge = self.findEdge(postPlace.id, postPlace.id)
                    # weight = self.edgeDict[edge].weight
                    for j in self.edgeDict.keys():
                        print("Key: ", j)
                    #print("Try EDGE: ", edge.weight, edge.id)
                    for i in self.edgeDict.values():
                        print(i.weight)
                        print(i.source, i.sink)
                        if i.sink == postPlace.id:
                            weight = i.weight
                            print("PostPlace Token: ", postPlace.tokens)
                            postPlace.tokens -= weight
                            print("New PostPlace Token: ", postPlace.tokens)

                    print("No PrePlace found. Only update postPlace")
                    print("PostPlace token: ", postPlace.tokens)




                # print("TRY", edge)



    # TODO function just ends -> recursive call for transitionlist or implement function in an outside loop?









