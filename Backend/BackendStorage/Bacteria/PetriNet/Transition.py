__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

class Transition:
    def __init__(self, id, name, prePlaceIDs, postPlaceIDs, priority):
        self.id = id
        self.name = name
        self.prePlaceIDs = prePlaceIDs
        self.postPlaceIDs = postPlaceIDs
        self.priority = priority

    def addPrePlace(self, placeID):
        self.prePlaceIDs.append(placeID)

    def addPostPlace(self, placeID):
        self.postPlaceIDs.append(placeID)

    def delPrePlace(self, placeID):
        self.prePlaceIDs.remove(placeID)

    def delPostPlace(self, placeID):
        self.postPlaceIDs.remove(placeID)