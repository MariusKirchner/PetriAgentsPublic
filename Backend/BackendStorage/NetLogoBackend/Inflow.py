__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

class Inflow:

    def __init__(self,  molecule, inout, time, starttime, endtime, amount, area, start, end):
        self.molecule = molecule
        self.inout = inout
        self.time = time
        #artefact of earlier, maybe use it in the future
        self.starttime = starttime
        self.endtime = endtime
        self.amount = amount
        self.area = area
        self.start = start
        self.end = end
        if area == 2:
            self.finalArea = (start, start)
        else:
            self.finalArea = (start, end)
        if time == 2:
            self.finalTime = (starttime, starttime)
        else:
            self.finalTime = (starttime, endtime)



