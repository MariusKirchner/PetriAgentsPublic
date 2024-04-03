class EnvironmentMolecule:

    def __init__(self, moleculeID, moleculeName, distMode, distArea, distAmount, involvedBacIDs):
        self.moleculeID = moleculeID
        self.moleculeName = moleculeName
        #artefact of earlier, maybe use it in the future
        self.distMode = distMode
        self.distArea = distArea
        self.distAmount = distAmount
        self.involvedBacIDs = involvedBacIDs


