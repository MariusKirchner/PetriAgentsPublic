class netLogoCompartment:
    def __init__(self, name, id, minX, maxX, minY, maxY, lrCont, tbCont, diffRate, diffBool, flowDir, flowRate, flowBool):
        self.name = name
        self.id = id
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.lrCont = lrCont
        self.tbCont = tbCont
        self.diffRate = diffRate
        self.diffBool = diffBool
        self.flowDir = flowDir
        self.flowRate = flowRate
        self.flowBool = flowBool
