_author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

import time
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor
import tkinter.filedialog

import datetime
import nl4py
import os

from Backend.BackendStorage.NetLogoBackend.NetLogoProjectFactory import createNetLogoProject
from Backend.Input import SBMLReadFactory, LoadProject, OpenConfig
from Backend.NetLogoConnection import NetLogoExecution
from Backend.Output import SaveProject
from Frontend import ConfigWindow


def updateProject(mainProject):
    mainProject.maxXCor = maxXCorDefault.get()
    mainProject.maxYCor = maxYCorDefault.get()
    mainProject.ticks = tickAmount.get()
    mainProject.lrCont = leftRightVar.get()
    mainProject.tbCont = topBottomVar.get()
    mainProject.diffRate = diffusionRateDefault.get()
    mainProject.flowRate = flowRateDefault.get()
    mainProject.flowDir = flowDirectionDefault.get()
    mainProject.diffBool = diffusionCheck.get()
    mainProject.flowBool = flowCheck.get()
    mainProject.moleculeOutFlowNorth = moleculeOutflowNorth.get()
    mainProject.moleculeOutFlowEast = moleculeOutflowEast.get()
    mainProject.moleculeOutFlowSouth = moleculeOutflowSouth.get()
    mainProject.moleculeOutFlowWest = moleculeOutflowWest.get()
    mainProject.bacteriaOutflowNorth = bacteriaOutflowNorth.get()
    mainProject.bacteriaOutflowEast = bacteriaOutflowEast.get()
    mainProject.bacteriaOutflowSouth = bacteriaOutflowSouth.get()
    mainProject.bacteriaOutflowWest = bacteriaOutflowWest.get()
    mainProject.diffmode = compDiff.get()
    mainProject.bacFlowRate = bacFlowRateDefault.get()
    mainProject.bacDiffRate = bacDiffRateDefault.get()
    mainProject.bacRotDiff = bacRotDiff.get()
    mainProject.bacVelo = bacVelo.get()
    mainProject.diffConstant = diffConstant.get()
    mainProject.patchLength = patchLength.get()
    mainProject.timePerTickDefault = timePerTickDefault.get()
    mainProject.patchColorMolecule = moleculeOption.get()
    mainProject.patchColorIncrement = moleculeIncrement.get()
    colorDict = {"Red":19, "Orange":29, "Brown":39, "Yellow":49, "Green":59, "Lime":69, "Turqouise":79, "Cyan":89, "LightBlue":99, "Blue":109, "Violet":119, "Magenta":129, "Pink":139}
    mainProject.patchColor = colorDict[patchColorOption.get()]


def updateGUI(mainProject):
    maxXCorDefault.set(mainProject.maxXCor)
    maxYCorDefault.set(mainProject.maxYCor)
    tickAmount.set(mainProject.ticks)
    leftRightVar.set(mainProject.lrCont)
    topBottomVar.set(mainProject.tbCont)
    diffusionRateDefault.set(mainProject.diffRate)
    bacteriaOutflowNorth.set(mainProject.bacteriaOutflowNorth)
    bacteriaOutflowEast.set(mainProject.bacteriaOutflowEast)
    bacteriaOutflowSouth.set(mainProject.bacteriaOutflowSouth)
    bacteriaOutflowWest.set(mainProject.bacteriaOutflowWest)
    moleculeOutflowNorth.set(mainProject.moleculeOutFlowNorth)
    moleculeOutflowEast.set(mainProject.moleculeOutFlowEast)
    moleculeOutflowSouth.set(mainProject.moleculeOutFlowSouth)
    moleculeOutflowWest.set(mainProject.moleculeOutFlowWest)
    compDiff.set(mainProject.diffmode)
    timePerTickDefault.set(mainProject.timePerTickDefault)
    patchLength.set(mainProject.patchLength)
    diffConstant.set(mainProject.diffConstant)
    bacVelo.set(mainProject.bacVelo)
    bacRotDiff.set(mainProject.bacRotDiff)
    diffusionCheck.set(mainProject.diffBool)
    diffusionRateDefault.set(mainProject.diffRate)
    flowRateDefault.set(mainProject.flowRate)
    bacFlowRateDefault.set(mainProject.bacFlowRate)
    bacDiffRateDefault.set(mainProject.bacDiffRate)
    flowCheck.set(mainProject.flowBool)
    flowDirectionDefault.set(mainProject.flowDir)
    moleculeOption.set(mainProject.patchColorMolecule)
    moleculeIncrement.set(mainProject.patchColorIncrement)
    patchColorOption.set(mainProject.patchColor)
    updateTables(mainProject)

def startSimulation(mainProject, amount, foldername, guimode, posmode, window, config):
    updateProject(mainProject)
    print("Starting Simulation")
    print("Writing the NetLogoFile")
    netLogoProjectFilepath = createNetLogoProject(mainProject)
    timezone = datetime.timezone.utc
    format = '%Y-%m-%dT%H%M%S%z'
    rawtime = r'{}'.format(datetime.datetime.now(tz=timezone).strftime(format))
    currdir = os.getcwd()
    resultdir = os.path.join(currdir, 'results')
    newfolder = '' + foldername + '_' + rawtime
    newfolderdir = os.path.join(resultdir, newfolder)
    if not os.path.isdir(newfolderdir):
        os.makedirs(newfolderdir)
    print("Saving the project file with it")
    projectfile = newfolder + ".xml"
    projectfilepath = os.path.join(newfolderdir, projectfile)
    SaveProject.saveProject(mainProject, projectfilepath)
    tablefolderdir = os.path.join(newfolderdir, 'tables')
    if not os.path.isdir(tablefolderdir):
        os.makedirs(tablefolderdir)
    NetLogoExecution.executeNetLogoProject(mainProject, netLogoProjectFilepath, amount, tablefolderdir, guimode, posmode, window, config)

def startSimulationQueue(mainProject, root, config):
    updateProject(mainProject)
    newWindow = Toplevel(root)
    tempFrame = ttk.Frame(newWindow, padding=10)
    tempFrame.grid()
    amount = StringVar(tempFrame)
    amount.set("1")
    ttk.Label(tempFrame, text="How often should this simulation be run? ").grid(column=0, row=0)
    Entry(tempFrame, textvariable=amount).grid(column=1, row=0)
    ttk.Label(tempFrame, text="Simulationresultfoldername (if left empty, it will default to just the current time): ").grid(column=0, row=1)
    foldername = StringVar(tempFrame)
    Entry(tempFrame, textvariable=foldername).grid(column=1, row=1)
    ttk.Label(tempFrame, text="Graphical representation of NetLogo?").grid(column=0, row=2)
    guimode = BooleanVar(tempFrame)
    guimode.set(True)
    Checkbutton(tempFrame, variable=guimode, onvalue=True, offvalue=False).grid(column=1, row=2)
    ttk.Label(tempFrame, text="Save position of turtles (LARGE FILES! Currently only in nonguimode)").grid(column=0, row=3)
    posMode = BooleanVar(tempFrame)
    posMode.set(False)
    Checkbutton(tempFrame, variable=posMode, onvalue=True, offvalue=False).grid(column=1, row=3)
    Button(tempFrame, text="Start this setup", command=lambda: startSimulation(mainProject, amount.get(), foldername.get(), guimode.get(), posMode.get(), root, config)).grid(column=0, row=4)



def createProjectFile(mainProject):
    updateProject(mainProject)
    filehandler = tkinter.filedialog.asksaveasfilename(title="Saving project at...", filetypes=(("paproject", "*.xml"), ("All files", "*.*")))
    if ".xml" not in filehandler:
        filehandler += ".xml"
    print("Creating ProjectFile")
    SaveProject.saveProject(mainProject, filehandler)

def loadProjectFile(projectHolder, bacteriaTab, bacteriaTabDict):
    updateProject(projectHolder.currProject)
    #TODO: ask if user really wants to load in a new one or wants to save the old project first
    print("Loading ProjectFile")
    for bacName in projectHolder.currProject.listOfBacteriaNames:
        delBacteria(projectHolder.currProject, bacName, bacteriaTab, bacteriaTabDict)
    filehandler = tkinter.filedialog.askopenfilename(title="Loading project from...", filetypes=(("paproject", ".xml"), ("All files", "*.*")))
    file = open(filehandler, 'r', encoding='utf8')
    newMainProject = LoadProject.loadProject(file)
    projectHolder.currProject = newMainProject
    #TODO: Test this!
    updateGUI(newMainProject)
    updateTables(newMainProject)
    updateProject(newMainProject)
    for bacName in projectHolder.currProject.listOfBacteriaNames:
        addBacteria(projectHolder.currProject, bacName, bacteriaTab, bacteriaTabDict, True)

def addBacteria(mainProject, bacteriaName, bacteriaTab, bacteriaTabDict, loadinBool):
    if bacteriaName not in mainProject.listOfBacteriaNames or loadinBool:
        if not loadinBool:
            filetypes = (("sbml files", "*.xml"), ("All files", "*.*"))
            filename = tkinter.filedialog.askopenfilename(title="Open a SBML File", filetypes=filetypes)
            newPetri = SBMLReadFactory.readSBML(filename)
            mainProject.addBacteria(bacteriaName, newPetri)
        newBacteria = mainProject.bacteriaNameDict[bacteriaName]
        newBacteriaTab = ttk.Frame(bacteriaTab)
        bacteriaTabDict[bacteriaName] = newBacteriaTab
        bacteriaTab.add(newBacteriaTab, text= "Bac" + str(mainProject.bacteriaNameDict[bacteriaName].ID) + ": " + bacteriaName)

        currNameDefault = StringVar(newBacteriaTab, value=newBacteria.name)
        currMOIDefault = StringVar(newBacteriaTab, value=newBacteria.MOI)
        currShapeDefault = StringVar(newBacteriaTab, value=newBacteria.shapeRepresentation)
        currFlagellaDefault = BooleanVar(newBacteriaTab, value=False)

        def changesOnBacteria():
            newName = currNameDefault.get()
            newMOI = currMOIDefault.get()
            newShape = currShapeDefault.get()
            newFlagella = currFlagellaDefault.get()
            if bacteriaName != newName:
                mainProject.bacteriaNameDict[newName] = mainProject.bacteriaNameDict[bacteriaName]
                mainProject.bacteriaNameDict.pop(bacteriaName)
                mainProject.bacteriaNameDict[newName].name = newName
                mainProject.listOfBacteriaNames.remove(bacteriaName)
                mainProject.listOfBacteriaNames.append(newName)
            mainProject.bacteriaNameDict[newName].MOI = newMOI
            mainProject.bacteriaNameDict[newName].shapeRepresentation = newShape
            mainProject.bacteriaNameDict[newName].flagella = newFlagella
            updateTables(mainProject)
            return True

        ttk.Label(newBacteriaTab, text="Change the name: ").grid(column=0, row=0)
        Entry(newBacteriaTab, textvariable=currNameDefault, validate="focusout", validatecommand=changesOnBacteria).grid(column=1, row=0)

        ttk.Label(newBacteriaTab, text="Change the MOI: ").grid(column=0, row=1)
        Entry(newBacteriaTab, textvariable=currMOIDefault, validate="focusout", validatecommand=changesOnBacteria).grid(column=1, row=1)

        ttk.Label(newBacteriaTab, text="Change the colour: ").grid(column=0, row=2)
        currColorDefault = StringVar(newBacteriaTab, value=newBacteria.colorRepresentation)
        style = ttk.Style()
        style.configure("colorButtonStyle.TFrame", background=currColorDefault)
        ttk.Button(newBacteriaTab, text="CurrentColor", style="colorButtonStyle.TFrame", command=lambda: changeColorBacteria(mainProject, currNameDefault.get(), style)).grid(column=1, row=2, ipadx=20, ipady=20)

        shapes = ["bacteria 1", "bacteria 3", "circle", "dot", "square", "star", "triangle", "sheep", "wolf", "car", "plane"]
        ttk.Label(newBacteriaTab, text="Change the shape: ").grid(column=0, row=3)
        OptionMenu(newBacteriaTab, currShapeDefault, *shapes, command=lambda x=None: changesOnBacteria()).grid(column=1, row=3)

        #ttk.Label(newBacteriaTab, text="Should this bacteria have a visual representation of flagella? ").grid(column=0, row=4)
        #ttk.Checkbutton(newBacteriaTab, variable=currFlagellaDefault, command= lambda x=None: changesOnBacteria()).grid(column=1, row=4)

        ttk.Label(newBacteriaTab, text="Environment molecules of this bacteria: ").grid(column=0, row=5)
        if (len(mainProject.bacteriaNameDict[currNameDefault.get()].listOfEnvPlaces) // 4) == 0:
            ttk.Label(newBacteriaTab, text=", ".join(mainProject.bacteriaNameDict[currNameDefault.get()].listOfEnvPlaces)).grid(column=0, row=6)
        else:
            for i in range(0, (len(mainProject.bacteriaNameDict[currNameDefault.get()].listOfEnvPlaces) // 4)):
                ttk.Label(newBacteriaTab, text=", ".join(mainProject.bacteriaNameDict[currNameDefault.get()].listOfEnvPlaces[(0 + 4 * i):(4 + 4 * i)]) + ",").grid(column=0, row=6 + i)
            ttk.Label(newBacteriaTab, text=", ".join(mainProject.bacteriaNameDict[currNameDefault.get()].listOfEnvPlaces[(0 + 4 * (i + 1)):])).grid(column=0, row=6 + i + 1)

        columnNames = ("BehaviourPlaceName", "CurrentBehaviour")
        behaviourTree = ttk.Treeview(newBacteriaTab, columns=columnNames, show="headings")
        #comment back in for variable behaviours
        #behaviourTree.bind("<Double-1>", lambda e: openBehaviourDetails(mainProject, behaviourTree, newBacteriaTab, currNameDefault))
        for column in columnNames:
            behaviourTree.heading(column, text=column)
            behaviourTree.grid(column=2, row=0, rowspan=10)
        clearTable(behaviourTree)
        for behaviourPlaceID in mainProject.bacteriaNameDict[bacteriaName].listOfBehPlaceIDs:
            behaviourTree.insert("", "end", values=(mainProject.bacteriaNameDict[bacteriaName].petriNet.placeDict[behaviourPlaceID].name, mainProject.bacteriaNameDict[bacteriaName].dictOfBehPlaces[behaviourPlaceID]))
        updateTables(mainProject)
    else:
        # TODO: make more beautiful messages for user errors
        pass

def delBacteria(mainProject, bacteriaName, bacteriaTab, bacteriaTabDict):
    print("Deleting Bacteria species")
    if bacteriaName in mainProject.listOfBacteriaNames:
        mainProject.delBacteriaByName(bacteriaName)
        bacteriaTab.forget(bacteriaTabDict[bacteriaName])
    updateTables(mainProject)

def rgbToHex(rgb):
    return "#%02x%02x%02x" % rgb


def changeColorBacteria(mainProject, bacteriaName, style):
    print("Changing colour for a bacteria")
    tempColor = askcolor(title="Change colour for " + bacteriaName, initialcolor=rgbToHex(tuple(mainProject.bacteriaNameDict[bacteriaName].colorRepresentation)))
    tempList = list(tempColor[0])
    mainProject.bacteriaNameDict[bacteriaName].colorRepresentation = tempList
    style.configure("colorButtonStyle.TFrame", background=tempList)
    print(mainProject.bacteriaNameDict[bacteriaName].colorRepresentation)

def openBehaviourDetails(mainProject, behaviourTree, root, currNameDefault):
    def changesOnBehaviour():
        newBehaviour = currBehaviourDefault.get()
        mainProject.bacteriaNameDict[currNameDefault.get()].dictOfBehPlaces[mainProject.bacteriaNameDict[currNameDefault.get()].petriNet.getPlaceByName(currPlaceName).id] = newBehaviour
    def closeBehaviourDetails():
        clearTable(behaviourTree)
        for behaviourPlaceID in mainProject.bacteriaNameDict[currNameDefault.get()].listOfBehPlaceIDs:
            behaviourTree.insert("", "end", values=(mainProject.bacteriaNameDict[currNameDefault.get()].petriNet.placeDict[behaviourPlaceID].name, mainProject.bacteriaNameDict[currNameDefault.get()].dictOfBehPlaces[behaviourPlaceID]))
        newWindow.destroy()
    newWindow = Toplevel(root)
    tempFrame = ttk.Frame(newWindow, padding=10)
    tempFrame.grid()
    currItem = behaviourTree.focus()
    print(behaviourTree.item(currItem))
    currPlaceName = behaviourTree.item(currItem).get("values")[0]
    newWindow.title(currPlaceName)
    ttk.Label(tempFrame, text="Selected behaviour place: " + currPlaceName).grid(column=0, row=0)
    currBehaviourDefault = StringVar(tempFrame, value=mainProject.bacteriaNameDict[currNameDefault.get()].dictOfBehPlaces[mainProject.bacteriaNameDict[currNameDefault.get()].petriNet.getPlaceByName(currPlaceName).id])
    possibleBehaviour = ["Move", "Replication", "Death", "Size", "None"]
    ttk.Label(tempFrame, text="Change the assigned behaviour: ").grid(column=0, row=1)
    OptionMenu(tempFrame, currBehaviourDefault, *possibleBehaviour, command=lambda x=None: changesOnBehaviour()).grid(column=0, row=2)
    ttk.Button(tempFrame, text="Save and Close", command=lambda x=None: closeBehaviourDetails()).grid(column=0, row=3)
    newWindow.mainloop()

def openEnvironmentMoleculeDetails(mainProject, root):
    newWindow = Toplevel(root)
    tempFrame = ttk.Frame(newWindow, padding=10)
    tempFrame.grid()
    currItem = environmentTree.focus()
    currMolecule = mainProject.dictOfEnvironmentMolecules[environmentTree.item(currItem).get("values")[0]]
    newWindow.title(currMolecule.moleculeName)
    ttk.Label(tempFrame, text="Minimum x-Value: ").grid(column=0, row=0)
    currMinXDefault = StringVar(tempFrame, value=currMolecule.distArea[0][0])
    Entry(tempFrame, textvariable=currMinXDefault).grid(column=1, row=0)
    ttk.Label(tempFrame, text="Minimum y-Value: ").grid(column=0, row=1)
    currMinYDefault = StringVar(tempFrame, value=currMolecule.distArea[0][1])
    Entry(tempFrame, textvariable=currMinYDefault).grid(column=1, row=1)
    ttk.Label(tempFrame, text="Maximum x-Value: ").grid(column=0, row=2)
    currMaxXDefault = StringVar(tempFrame, value=currMolecule.distArea[1][0])
    Entry(tempFrame, textvariable=currMaxXDefault).grid(column=1, row=2)
    ttk.Label(tempFrame, text="Maximum y-Value: ").grid(column=0, row=3)
    currMaxYDefault = StringVar(tempFrame, value=currMolecule.distArea[1][1])
    Entry(tempFrame, textvariable=currMaxYDefault).grid(column=1, row=3)
    ttk.Label(tempFrame, text="How much of this should be spawned in this area?").grid(column=0, row=4)
    currAmountDefault = StringVar(tempFrame, value=currMolecule.distAmount)
    Entry(tempFrame, textvariable=currAmountDefault).grid(column=1, row=4)
    ttk.Button(tempFrame, text="Confirm changes", command=lambda: changesOnMolecule(newWindow, mainProject, currMolecule.moleculeName, currMinXDefault.get(), currMinYDefault.get(), currMaxXDefault.get(), currMaxYDefault.get(), currAmountDefault.get())).grid(column=0, row=5)
    ttk.Button(tempFrame, text="Add new flow option", command=lambda: addFlowOption(newWindow, mainProject)).grid(column=2, row=11)
    newWindow.mainloop()

def addFlowOption(newWindow, mainProject):
    def checkdisabled():
        pass
    tempWindow = Toplevel(newWindow)
    tempFrame = ttk.Frame(tempWindow, padding=10)
    tempFrame.grid()
    inOutVar = BooleanVar()
    inOutVar.set(True)
    ttk.Radiobutton(tempFrame, text="Inflow", variable=inOutVar, value=True, command= lambda: checkdisabled).grid(row=0, column=0)
    #TODO: Once implemented comment this back in
    #ttk.Radiobutton(tempFrame, text="Outflow", variable=inOutVar, value=False, command= lambda: checkdisabled).grid(row=0, column=1)
    timeVar = IntVar()
    #ttk.Radiobutton(tempFrame, text="At all timesteps", variable=timeVar, value=0, command= lambda: checkdisabled).grid(row=1, column=0)
    ttk.Radiobutton(tempFrame, text="At an intervall", variable=timeVar, value=1, command= lambda: checkdisabled).grid(row=1, column=1)
    ttk.Radiobutton(tempFrame, text="At a single timestep", variable=timeVar, value=2, command= lambda: checkdisabled).grid(row=1, column=2)
    ttk.Label(tempFrame, text="StartTime:").grid(row=2, column=0)
    startTimeDefault = IntVar(tempFrame, value=0)
    Entry(tempFrame, textvariable=startTimeDefault).grid(row=2, column=1)
    ttk.Label(tempFrame, text="EndTime:").grid(row=2, column=2)
    endTimeDefault = IntVar(tempFrame, value=0)
    Entry(tempFrame, textvariable=endTimeDefault).grid(row=2, column=3)
    ttk.Label(tempFrame, text="Amount of Molecule").grid(row=3, column=0)
    amountDefault = IntVar(tempFrame, value=0)
    Entry(tempFrame, textvariable=amountDefault).grid(row=3, column=1)
    areaVar = IntVar()
    #ttk.Radiobutton(tempFrame, text="Entire axis", variable=areaVar, value=0, command= lambda: checkdisabled).grid(row=4, column=0)
    ttk.Radiobutton(tempFrame, text="Part of axis", variable=areaVar, value=1, command= lambda: checkdisabled).grid(row=4, column=1)
    ttk.Radiobutton(tempFrame, text="Single position", variable=areaVar, value=2, command= lambda: checkdisabled).grid(row=4, column=2)
    ttk.Label(tempFrame, text="StartSpace:").grid(row=5, column=0)
    startSpaceDefault = IntVar(tempFrame, value=0)
    Entry(tempFrame, textvariable=startSpaceDefault).grid(row=5, column=1)
    ttk.Label(tempFrame, text="EndSpace:").grid(row=5, column=2)
    endSpaceDefault = IntVar(tempFrame, value=0)
    Entry(tempFrame, textvariable=endSpaceDefault).grid(row=5, column=3)
    currItem = environmentTree.focus()
    currMolecule = mainProject.dictOfEnvironmentMolecules[environmentTree.item(currItem).get("values")[0]]
    ttk.Button(tempFrame, text="Add Flowoption", command=lambda: addinoutFlow(newWindow,tempWindow, mainProject, currMolecule, inOutVar.get(), timeVar.get(), startTimeDefault.get(), endTimeDefault.get(), amountDefault.get(), areaVar.get(), startSpaceDefault.get(), endSpaceDefault.get())).grid(row=6, column=0)
    tempWindow.mainloop()



def addinoutFlow(newWindow, tempWindow, mainProject, molecule, inout, time, starttime, endtime, amount, area, start, end):
    mainProject.addinoutFlow(molecule, inout, time, starttime, endtime, amount, area, start, end)
    updateTables(mainProject)
    tempWindow.destroy()
    newWindow.destroy()


def changesOnMolecule(newWindow, mainProject, moleculeName, minX, minY, maxX, maxY, amount):
    mainProject.dictOfEnvironmentMolecules[moleculeName].distArea = [[minX, minY], [maxX, maxY]]
    mainProject.dictOfEnvironmentMolecules[moleculeName].distAmount = amount
    updateTables(mainProject)
    newWindow.destroy()


def clearTable(treeview):
   for item in treeview.get_children():
      treeview.delete(item)

def updateTables(mainProject):
    clearTable(environmentTree)
    for envMolecule in mainProject.dictOfEnvironmentMolecules:
        templist = []
        for i in mainProject.dictOfEnvironmentMolecules[envMolecule].involvedBacIDs:
            templist.append(mainProject.bacteriaIDDict[i].name)
        environmentTree.insert("", "end", values=(envMolecule, len(mainProject.dictOfEnvironmentMolecules[envMolecule].involvedBacIDs), templist))
    # Comment for Compartment
    #clearTable(compartmentTree)
    #for compartmentID in mainProject.listOfCompartmentIDs:
    #    coord = [mainProject.compartmentDict[compartmentID].minX, mainProject.compartmentDict[compartmentID].maxX, mainProject.compartmentDict[compartmentID].minY, mainProject.compartmentDict[compartmentID].maxY]
    #    compartmentTree.insert("", "end", values=(mainProject.compartmentDict[compartmentID].name, coord, "NotYetImplemented"))
    clearTable(inOutMolTree)
    for flow in mainProject.flows:
        if flow.inout:
            tempType = "Inflow";
        else:
            tempType = "Outflow";
        inOutMolTree.insert("", "end", values=(flow.molecule.moleculeName, tempType, flow.finalTime, flow.amount, flow.finalArea))

def diffusionCheckboxChange(mainProject, checkboxVar):
    mainProject.diffBool = checkboxVar.get()
    print(mainProject.diffBool)

def flowCheckboxChange(mainProject, checkboxVar):
    mainProject.flowBool = checkboxVar.get()
    print(mainProject.flowBool)

def addCompartment(mainProject, root):
    newWindow = Toplevel(root)
    tempFrame = ttk.Frame(newWindow, padding=10)
    tempFrame.grid()
    ttk.Label(tempFrame, text="CompartmentName: ").grid(column=0, row=0)
    currNameDefault = StringVar(tempFrame)
    Entry(tempFrame, textvariable=currNameDefault).grid(column=1, row=0)
    ttk.Label(tempFrame, text="Corner1 X Coordinate: ").grid(column=0, row=1)
    corner1XCoord = StringVar(tempFrame)
    Entry(tempFrame, textvariable=corner1XCoord).grid(column=1, row=1)
    ttk.Label(tempFrame, text="Corner1 Y Coordinate: ").grid(column=0, row=2)
    corner1YCoord = StringVar(tempFrame)
    Entry(tempFrame, textvariable=corner1YCoord).grid(column=1, row=2)
    ttk.Label(tempFrame, text="Corner2 X Coordinate: ").grid(column=0, row=3)
    corner2XCoord = StringVar(tempFrame)
    Entry(tempFrame, textvariable=corner2XCoord).grid(column=1, row=3)
    ttk.Label(tempFrame, text="Corner2 Y Coordinate: ").grid(column=0, row=4)
    corner2YCoord = StringVar(tempFrame)
    Entry(tempFrame, textvariable=corner2YCoord).grid(column=1, row=4)
    #compartment code
    #idea: Add restriction variability for molecules and species
    #idea: Add possibility to modify compartment settings
    #idea: PREVENT COMPARTMENT WITH LARGER NUMBERS THAN DEFAULT
    #idea: PREVENT WRONG INPUTS (everywhere btw)
    ttk.Button(tempFrame, text="Confirm changes", command=lambda: addNewCompartment(mainProject, newWindow, currNameDefault.get(), corner1XCoord.get(), corner1YCoord.get(), corner2XCoord.get(), corner2YCoord.get())).grid(column=0, row=5)
    newWindow.mainloop()

def addNewCompartment(mainProject, newWindow, name, x1, y1, x2, y2):
    mainProject.addCompartment(name, x1, y1, x2, y2)
    updateTables(mainProject)
    newWindow.destroy()

def mainWindow(projectHolder):
    root = Tk()
    root.title("PetriAgents MainWindow")

    parentTab = ttk.Notebook(root)

    settingsTab = ttk.Frame(parentTab)
    bacteriaTab = ttk.Notebook(parentTab)
    environmentTab = ttk.Frame(parentTab)
    #Comment for Compartment
    #compartmentTab = ttk.Frame(parentTab)

    changeBacteriaTab = ttk.Frame(bacteriaTab)

    parentTab.add(settingsTab, text="General Settings")
    parentTab.add(bacteriaTab, text="Bacteria")
    parentTab.add(environmentTab, text="Environment")
    # Comment for Compartment
    #parentTab.add(compartmentTab, text="Compartments")

    bacteriaTab.add(changeBacteriaTab, text="Add or remove Bacteria")

    parentTab.pack(expand=1, fill="both")

    bacteriaTabDict = {}

    global maxXCorDefault
    ttk.Label(settingsTab, text="Maximum X Coordinate").grid(column=0, row=0)
    maxXCorDefault = StringVar(settingsTab, value="100")
    Entry(settingsTab, textvariable=maxXCorDefault).grid(column=1, row=0)
    global maxYCorDefault
    ttk.Label(settingsTab, text='Maximum Y Coordinate').grid(column=0, row=1)
    maxYCorDefault = StringVar(settingsTab, value="50")
    Entry(settingsTab, textvariable=maxYCorDefault).grid(column=1, row=1)
    global tickAmount
    ttk.Label(settingsTab, text="Ticks").grid(column=0, row=2)
    tickAmount = StringVar(settingsTab, value="10000")
    Entry(settingsTab, textvariable=tickAmount).grid(column=1, row=2)
    global bacteriaOutflowNorth
    global bacteriaOutflowEast
    global bacteriaOutflowSouth
    global bacteriaOutflowWest
    ttk.Label(settingsTab, text="Bacteria outflow possible at which borders?").grid(column=0, row=4)
    ttk.Label(settingsTab, text="North").grid(column=1, row=4)
    bacteriaOutflowNorth = IntVar(settingsTab, value=0)
    Checkbutton(settingsTab, variable=bacteriaOutflowNorth).grid(column=2, row=4)
    ttk.Label(settingsTab, text="East").grid(column=3, row=4)
    bacteriaOutflowEast = IntVar(settingsTab, value=1)
    Checkbutton(settingsTab, variable=bacteriaOutflowEast).grid(column=4, row=4)
    ttk.Label(settingsTab, text="South").grid(column=5, row=4)
    bacteriaOutflowSouth = IntVar(settingsTab, value=0)
    Checkbutton(settingsTab, variable=bacteriaOutflowSouth).grid(column=6, row=4)
    ttk.Label(settingsTab, text="West").grid(column=7, row=4)
    bacteriaOutflowWest = IntVar(settingsTab, value=0)
    Checkbutton(settingsTab, variable=bacteriaOutflowWest).grid(column=8, row=4)

    global moleculeOutflowNorth
    global moleculeOutflowEast
    global moleculeOutflowSouth
    global moleculeOutflowWest
    ttk.Label(settingsTab, text="Molecule outflow possible at which borders?").grid(column=0, row=5)
    ttk.Label(settingsTab, text="North").grid(column=1, row=5)
    moleculeOutflowNorth = IntVar(settingsTab, value=0)
    Checkbutton(settingsTab, variable=moleculeOutflowNorth).grid(column=2, row=5)
    ttk.Label(settingsTab, text="East").grid(column=3, row=5)
    moleculeOutflowEast = IntVar(settingsTab, value=1)
    Checkbutton(settingsTab, variable=moleculeOutflowEast).grid(column=4, row=5)
    ttk.Label(settingsTab, text="South").grid(column=5, row=5)
    moleculeOutflowSouth = IntVar(settingsTab, value=0)
    Checkbutton(settingsTab, variable=moleculeOutflowSouth).grid(column=6, row=5)
    ttk.Label(settingsTab, text="West").grid(column=7, row=5)
    moleculeOutflowWest = IntVar(settingsTab, value=0)
    Checkbutton(settingsTab, variable=moleculeOutflowWest).grid(column=8, row=5)

    global compDiff
    ttk.Label(settingsTab, text="Complex diffusion mode (Enables flows, outflows and rate changes)").grid(column=0, row=6)
    compDiff = IntVar(settingsTab, value=1)
    Checkbutton(settingsTab, variable=compDiff).grid(column=1, row=6)

    global timePerTickDefault
    ttk.Label(settingsTab, text="Time per Tick in ms").grid(column=0, row=7)
    timePerTickDefault = StringVar(settingsTab, value="1000")
    Entry(settingsTab, textvariable=timePerTickDefault).grid(column=1, row=7)
    global patchLength
    ttk.Label(settingsTab, text='Patch length and width in μm').grid(column=0, row=8)
    patchLength = StringVar(settingsTab, value="2000")
    Entry(settingsTab, textvariable=patchLength).grid(column=1, row=8)
    global diffConstant
    ttk.Label(settingsTab, text="Diffusion constant in in μm^2/s ").grid(column=0, row=9)
    diffConstant = StringVar(settingsTab, value="1000000")
    Entry(settingsTab, textvariable=diffConstant).grid(column=1, row=9)
    global bacVelo
    ttk.Label(settingsTab, text='Bacterial velocity in μm/s').grid(column=0, row=10)
    bacVelo = StringVar(settingsTab, value="25")
    Entry(settingsTab, textvariable=bacVelo).grid(column=1, row=10)
    global bacRotDiff
    ttk.Label(settingsTab, text="Bacterial rotational diffusion constant in degrees/s ").grid(column=0, row=11)
    bacRotDiff = StringVar(settingsTab, value="9")
    Entry(settingsTab, textvariable=bacRotDiff).grid(column=1, row=11)


    global leftRightVar
    ttk.Label(environmentTab, text="Left/Right Continuity").grid(column=0, row=2)
    leftRightVar = IntVar(value=0)
    Checkbutton(environmentTab, variable=leftRightVar).grid(column=1, row=2)
    global topBottomVar
    topBottomVar = IntVar(value=1)
    ttk.Label(environmentTab, text="Top/Bottom Continuity").grid(column=0, row=3)
    Checkbutton(environmentTab, variable=topBottomVar).grid(column=1, row=3)

    ttk.Label(changeBacteriaTab, text="Add Bacteria with name: ").grid(column=0, row=4)
    addBacteriaName = StringVar(changeBacteriaTab)
    Entry(changeBacteriaTab, textvariable=addBacteriaName).grid(column=1, row=4)
    Button(changeBacteriaTab, text="Add new bacteria species", command=lambda: addBacteria(projectHolder.currProject, addBacteriaName.get(), bacteriaTab, bacteriaTabDict, False)).grid(column=2, row=4)

    ttk.Label(changeBacteriaTab, text="Delete Bacteria with name: ").grid(column=0, row=5)
    delBacteriaName = StringVar(changeBacteriaTab)
    Entry(changeBacteriaTab, textvariable=delBacteriaName).grid(column=1, row=5)
    Button(changeBacteriaTab, text="Delete bacteria species", command=lambda: delBacteria(projectHolder.currProject, delBacteriaName.get(), bacteriaTab, bacteriaTabDict)).grid(column=2, row=5)


    global diffusionCheck
    diffusionCheck = IntVar(value=1)
    Checkbutton(environmentTab, text="Diffusion", variable=diffusionCheck, onvalue=1, offvalue=0, command=lambda: diffusionCheckboxChange(projectHolder.currProject, diffusionCheck)).grid(column=2, row=6)

    #comment back in if diffusionrate implemented
    global diffusionRateDefault
    ttk.Label(environmentTab, text='Diffusion Rate (only changeable in complex diffusion mode)').grid(column=0, row=6)
    diffusionRateDefault = StringVar(environmentTab, value="100")
    Entry(environmentTab, textvariable=diffusionRateDefault).grid(column=1, row=6)

    global flowRateDefault
    ttk.Label(environmentTab, text="Flow Rate (only changeable in complex diffusion mode)").grid(column=0, row=7)
    flowRateDefault = StringVar(environmentTab, value="100")
    Entry(environmentTab, textvariable=flowRateDefault).grid(column=1, row=7)

    # comment back in if flowrate implemented
    global bacFlowRateDefault
    ttk.Label(environmentTab, text="Bacteria Flow Rate (only changeable in complex diffusion mode)").grid(column=0, row=8)
    bacFlowRateDefault = StringVar(environmentTab, value="0")
    Entry(environmentTab, textvariable=bacFlowRateDefault).grid(column=1, row=8)

    global bacDiffRateDefault
    ttk.Label(environmentTab, text="Bacteria Diffusion Rate (only changeable in complex diffusion mode)").grid(column=0, row=9)
    bacDiffRateDefault = StringVar(environmentTab, value="0")
    Entry(environmentTab, textvariable=bacDiffRateDefault).grid(column=1, row=9)

    global flowCheck
    flowCheck = IntVar(value=1)
    Checkbutton(environmentTab, text="Flow", variable=flowCheck, onvalue=1, offvalue=0, command=lambda: flowCheckboxChange(projectHolder.currProject, flowCheck)).grid(column=2, row=7)

    #comment back in if flowdirection implemented
    global flowDirectionDefault
    #ttk.Label(environmentTab, text='Flow direction').grid(column=0, row=7)
    flowDirectionDefault = StringVar(environmentTab, value="E")
    #Entry(environmentTab, textvariable=flowDirectionDefault).grid(column=1, row=7)

    ttk.Label(environmentTab, text="Diffusion Rate and Flow Rate influence the standard deviation and the mean of the normal distribution").grid(column=0, row=10)
    ttk.Label(environmentTab, text="For Diffusion: 0: No Diffusion (sigma = 0), 100: Default Diffusion (sigma = 1)").grid(column=0, row=11)
    ttk.Label(environmentTab, text="For Flow: Mean of Normal Distribution used in x-axis diffusion. 0: No Flow (my = 0), 100: Defaultflow (my = 1)").grid(column=0, row=12)
    ttk.Label(environmentTab, text="Any other value scales accordingly into sigma and my by being divided by 100").grid(column=0, row=13)


    Button(settingsTab, text="Save this setup", command=lambda: createProjectFile(projectHolder.currProject)).grid(column=0, row=15)
    Button(settingsTab, text="Start this setup", command=lambda: startSimulationQueue(projectHolder.currProject, root, projectHolder.config)).grid(column=1, row=15)
    Button(settingsTab, text="Load a setup", command=lambda: loadProjectFile(projectHolder, bacteriaTab, bacteriaTabDict)).grid(column=2, row=15)

    #Button(settingsTab, text="Change Config", command=lambda: configHelper(projectHolder)).grid(column=0, row=16)

    #def configHelper(projectHolder):
    #    ConfigWindow.configWindow(projectHolder)
    #    projectHolder.config = OpenConfig.openConfig(os.getcwd() + "/config.xml")

    ttk.Label(settingsTab, text=" ").grid(column=0, row=17)
    ttk.Label(settingsTab, text=" ").grid(column=0, row=18)
    ttk.Label(settingsTab, text=" ").grid(column=0, row=19)

    ttk.Label(settingsTab, text="Version: 0.9.0").grid(column=0, row=20)
    ttk.Label(settingsTab, text="Release Date: 3rd of December 2025").grid(column=0, row=21)

    # Comment for Compartment
    #Button(compartmentTab, text="Add a compartment", command=lambda: addCompartment(projectHolder.currProject, root)).grid(column=3, row=0)



    environmentColumnNames = ("EnvironmentMoleculeName", "NumberOfBacteriaInvolved", "ListOfBacteriaInvolved")
    global environmentTree
    environmentTree = ttk.Treeview(environmentTab, columns=environmentColumnNames, show="headings")
    environmentTree.bind("<Double-1>", lambda e: openEnvironmentMoleculeDetails(projectHolder.currProject, root))
    for column in environmentColumnNames:
        environmentTree.heading(column, text=column)
    environmentTree.grid(column=4, row=0, rowspan=10)

    ttk.Label(environmentTab, text="Environment molecule used for coloring").grid(column=5, row=0)
    global moleculeOption
    moleculeOption = ttk.Combobox(environmentTab, values=projectHolder.currProject.getListOfEnvironmentMolecules() + ["No Coloring"], state="readonly", postcommand=lambda: changeEnvs())
    def changeEnvs():
        moleculeOption["values"] = projectHolder.currProject.getListOfEnvironmentMolecules() + ["No Coloring"]
    moleculeOption.current(0)
    moleculeOption.grid(column=6, row=0)

    ttk.Label(environmentTab, text="Discrete increment for molecule numbers that cause patch color").grid(column=5, row=1)
    global moleculeIncrement
    moleculeIncrement = StringVar(environmentTab, value="5")
    Entry(environmentTab, textvariable=moleculeIncrement).grid(column=6, row=1)

    ttk.Label(environmentTab, text="Color for patch coloring").grid(column=5, row=2)
    global patchColorOption
    colorOptions = ["Red", "Orange", "Brown", "Yellow", "Green", "Lime", "Turqouise", "Cyan", "LightBlue", "Blue", "Violet", "Magenta", "Pink"]
    patchColorOption = ttk.Combobox(environmentTab, values=colorOptions, state="readonly")
    patchColorOption.current(0)
    patchColorOption.grid(column=6, row=2)
    # Comment for Compartment
    #compartmentColumnNames = ("CompartmentName", "Corners in X1, X2, Y1, Y2", "RestrictionsFor")
    #global compartmentTree
    #compartmentTree = ttk.Treeview(compartmentTab, columns=compartmentColumnNames, show="headings")
    #for column in compartmentColumnNames:
    #    compartmentTree.heading(column, text=column)
    #compartmentTree.grid(column=4, row=0, rowspan=10)
    inOutMolColumnNames = ("Molecule", "In/Out", "Time", "Amount", "Area")
    global inOutMolTree
    inOutMolTree = ttk.Treeview(environmentTab, columns=inOutMolColumnNames, show="headings")
    inOutMolTree.bind("<Double-1>", lambda e: (projectHolder.currProject, root))  # TODO: add delete function for flows
    for column in inOutMolColumnNames:
        inOutMolTree.heading(column, text=column)
    inOutMolTree.grid(column=4, row=11, rowspan=10, columnspan=3)
    updateTables(projectHolder.currProject)
    root.mainloop()


mainPetriDict = {}
bacteriaTreeDict = {}
environmentTreeDict = {}