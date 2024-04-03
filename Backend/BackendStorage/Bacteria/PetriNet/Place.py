__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

class Place:
    def __init__(self, id, name, tokens, preTransitionIDs, postTransitionIDs):
        self.id = id
        self.name = name
        self.tokens = tokens
        self.preTransitionsIDs = preTransitionIDs
        self.postTransitionIDs = postTransitionIDs

    def changeTokens(self, tokenChange):
        self.tokens = self.tokens + tokenChange

    def addPreTransition(self, transitionID):
        self.preTransitionsIDs.append(transitionID)

    def addPostTransition(self, transitionID):
        self.postTransitionIDs.append(transitionID)

    def delPreTransition(self, transitionID):
        self.preTransitionsIDs.remove(transitionID)

    def delPostTransition(self, transitionID):
        self.postTransitionIDs.remove(transitionID)
