from Backend.BackendStorage.NetLogoBackend.EnvironmentMolecule import EnvironmentMolecule
from Backend.BackendStorage.NetLogoBackend.NetLogoCompartment import netLogoCompartment
from Backend.BackendStorage.NetLogoBackend.NetLogoSettings import netLogoSettings
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from Backend.BackendStorage.Bacteria.Bacteria import bacteria
from Backend.Input import SBMLReadFactory
from Backend.BackendStorage.NetLogoBackend.Inflow import Inflow

class petriAgentProject:
    def __init__(self):
        self.listOfBacteriaIDs = []
        self.listOfBacteriaNames = []
        self.bacteriaIDDict = {}
        self.bacteriaNameDict = {}
        self.listOfCompartmentIDs = []
        # Comment for Compartment
        #self.compartmentDict = {}
        #self.compartmentRelationDict = {}
        self.netLogoSettings = netLogoSettings(100, 100)
        self.listOfEnvironmentMolecules = []
        self.dictOfEnvironmentMolecules = {}
        self.maxXCor = 100
        self.maxYCor = 50
        self.ticks = 10000
        self.lrCont = 1
        self.tbCont = 1
        self.diffRate = 100
        self.diffBool = 1
        self.flowDir = "E"
        self.flowRate = 100
        self.flowBool = 1
        self.bacFlowRate = 0
        self.bacDiffRate = 0
        self.flows = []
        # Comment for Compartment
        #defaultCompartment = netLogoCompartment("Default", 0, 0, self.maxXCor, 0, self.maxYCor, self.lrCont, self.tbCont, self.diffRate, self.diffBool, self.flowDir, self. flowRate, self.flowBool)
        #self.listOfCompartmentIDs.append(0)
        #self.compartmentDict[0] = defaultCompartment
        self.moleculeOutFlow = 0
        self.bacteriaOutflow = 0
        # make these bacteriaspecific? if needed
        self.diffmode = 0

    def addBacteria(self, bacteriaName, bacteriaPetri):
        # TODO: only if name not in there yet? or give individualIDs, change default of molnumber
        print("Adding Bacteria species")
        newID = len(self.listOfBacteriaIDs) + 1
        newBacteria = bacteria(newID, bacteriaName, bacteriaPetri, 20)
        self.listOfBacteriaIDs.append(newID)
        self.listOfBacteriaNames.append(bacteriaName)
        self.bacteriaIDDict[newID] = newBacteria
        self.bacteriaNameDict[bacteriaName] = newBacteria
        for envMolecule in newBacteria.listOfEnvPlaces:
            if envMolecule not in self.listOfEnvironmentMolecules:
                newEnvMolecule = EnvironmentMolecule(len(self.listOfEnvironmentMolecules), envMolecule, "random", [[0, 0], [self.maxXCor, self.maxYCor]], 100, [newID])
                self.dictOfEnvironmentMolecules[envMolecule] = newEnvMolecule
                self.listOfEnvironmentMolecules.append(envMolecule)
            else:
                self.dictOfEnvironmentMolecules[envMolecule].involvedBacIDs.append(newID)

    def delBacteriaByName(self, bacteriaName):
        bacToDelete = self.bacteriaNameDict[bacteriaName]
        for envMolecule in bacToDelete.listOfEnvPlaces:
            if len(self.dictOfEnvironmentMolecules[envMolecule].involvedBacIDs) == 1:
                self.listOfEnvironmentMolecules.remove(envMolecule)
                self.dictOfEnvironmentMolecules.pop(envMolecule)
            else:
                self.dictOfEnvironmentMolecules[envMolecule].involvedBacIDs.remove(bacToDelete.ID)
        self.bacteriaIDDict.pop(bacToDelete.ID)
        self.listOfBacteriaIDs.remove(bacToDelete.ID)
        self.listOfBacteriaNames.remove(bacteriaName)
        self.bacteriaNameDict.pop(bacteriaName)

    def addCompartment(self, name, x1, y1, x2, y2):
        print([name, x1, y1, x2, y2])
        if int(x1) < int(x2):
            lowerX = int(x1)
            higherX = int(x2)
        else:
            lowerX = int(x2)
            higherX = int(x1)
        if int(y1) < int(y2):
            lowerY = int(y1)
            higherY = int(y2)
        else:
            lowerY = int(y2)
            higherY = int(y1)
        # Comment for Compartment
        #newCompartment = netLogoCompartment(name, len(self.listOfCompartmentIDs), lowerX, higherX, lowerY, higherY, self.lrCont, self.tbCont, self.diffRate, self.diffBool, self.flowDir, self. flowRate, self.flowBool)
        #idea: make this specific for each molecule and agent type
        # Comment for Compartment
        #for compartmentID in self.listOfCompartmentIDs:
        #    self.compartmentRelationDict[(compartmentID, len(self.listOfCompartmentIDs))] = [0, 0]
        #    self.compartmentRelationDict[(len(self.listOfCompartmentIDs), compartmentID)] = [0, 0]
        #self.listOfCompartmentIDs.append(len(self.listOfCompartmentIDs))
        #self.compartmentDict[len(self.listOfCompartmentIDs) - 1] = newCompartment

    def addinoutFlow(self, molecule, inout, time, starttime, endtime, amount, area, start, end):
        if area == 0:
            start = 0
            end = self.maxYCor
        if time == 0:
            starttime = 0
            endtime = self.ticks
        self.flows.append(Inflow(molecule, inout, time, starttime, endtime, amount, area, start, end))

