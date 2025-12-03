__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"
import copy
import os
from Backend.Input import OpenConfig
import nl4py

import ast
import gc
import time
import re

from Backend.BackendStorage.PAProject import petriAgentProject
from Frontend import MainWindow
from Backend.BackendStorage.Bacteria.PetriNet import PetriNetObject
from IntermediateProject import intermediateProject
from Frontend import ConfigWindow
from Backend.BackendStorage import Config

if __name__ == '__main__':
    mainProject = petriAgentProject()
    if not os.path.exists(os.getcwd() + "/config.xml"):
        ConfigWindow.configWindow(Config.PetriAgentConfig("None"))
    newConfig = OpenConfig.openConfig(os.getcwd() + "/config.xml")
    projectHolder = intermediateProject(mainProject, newConfig)
    MainWindow.mainWindow(projectHolder)

#quit to not open netlogo for every test of the GUI
quit()
# everything after this is just for reference stuff

startTime = time.time()

print("Starting Netlogo from Python")
#linux
nl4py.initialize('/home/MariusKirchner/Desktop/NetLogo-6.2.2-64/NetLogo 6.2.2/')
#windows has to be changed still
#nl4py.initialize(r"D:\UniversityPrograms\NetLogo6.3.0")
n = nl4py.netlogo_app()
#linux
modelPath = "/home/MariusKirchner/Desktop/PetriAgents/BacteriaPetriAgents.nlogo"
#windows has to be changed still
#modelPath = r"C:\Users\Marius MainPC\Desktop\PhD\Salmonella\PetriAgents\ExamplePetriNetAgent.desktop.nlogo"
n.open_model(modelPath)
n.command("setup")
time.sleep(1)
n.command("setup")
tick = 0
maxxcor = int(float(n.report("xSize")))
maxycor = int(float(n.report("ySize")))
print(maxxcor)
print(maxycor)
environmentPetri = PetriNet()
currentPatchStatus = n.report("patchesReport")
currentPatchStatus = ast.literal_eval(currentPatchStatus)
#The following needs to be done just once, but TokenDistribution later!!!
currid = 0
time2 = time.time()
print("initial --- %s seconds ---" % (time2 - startTime))
for i in currentPatchStatus:
    environmentPetri.addPlace(currid, "Patch" + "_" + str(int(i[1])) + "_" + str(int(i[0])) + "_Nut", 0, [], [])
    currid += 1
#add initial and end places
for y in range(0, maxycor + 1):
    environmentPetri.addPlace(currid, "Patch" + "_" + str(y) + "_" + "-1" + "_Nut", 5, [], [])
    currid += 1
    environmentPetri.addPlace(currid, "Patch" + "_" + str(y) + "_" + str(maxxcor + 1) + "_Nut", 0, [], [])
    currid += 1
#produce 5 incoming transitions for each place
for x in range(0, maxxcor + 2):
    for y in range(0, maxycor + 1):
        tempsink = environmentPetri.getPlaceByName("Patch" + "_" + str(y) + "_" + str(x) + "_Nut")
        if y == 0:
            tempsource = environmentPetri.getPlaceByName("Patch" + "_" + str(maxycor) + "_" + str(x) + "_Nut")
        else:
            tempsource = environmentPetri.getPlaceByName("Patch" + "_" + str(y - 1) + "_" + str(x) + "_Nut")
        environmentPetri.addTransition(currid, tempsource.name + "_" + tempsink.name + "_NutTrans", [tempsource.id], [tempsink.id])
        if y == 0:
            tempsource = environmentPetri.getPlaceByName("Patch" + "_" + str(maxycor) + "_" + str(x - 1) + "_Nut")
        else:
            tempsource = environmentPetri.getPlaceByName("Patch" + "_" + str(y - 1) + "_" + str(x - 1) + "_Nut")
        environmentPetri.addTransition(currid + 1, tempsource.name + "_" + tempsink.name + "_NutTrans", [tempsource.id], [tempsink.id])
        tempsource = environmentPetri.getPlaceByName("Patch" + "_" + str(y) + "_" + str(x - 1) + "_Nut")
        environmentPetri.addTransition(currid + 2, tempsource.name + "_" + tempsink.name + "_NutTrans", [tempsource.id], [tempsink.id])
        if y == maxycor:
            tempsource = environmentPetri.getPlaceByName("Patch" + "_" + str(0) + "_" + str(x - 1) + "_Nut")
        else:
            tempsource = environmentPetri.getPlaceByName("Patch" + "_" + str(y + 1) + "_" + str(x - 1) + "_Nut")
        environmentPetri.addTransition(currid + 3, tempsource.name + "_" + tempsink.name + "_NutTrans", [tempsource.id], [tempsink.id])
        if y == maxycor:
            tempsource = environmentPetri.getPlaceByName("Patch" + "_" + str(0) + "_" + str(x) + "_Nut")
        else:
            tempsource = environmentPetri.getPlaceByName("Patch" + "_" + str(y + 1) + "_" + str(x) + "_Nut")
        environmentPetri.addTransition(currid + 4, tempsource.name + "_" + tempsink.name + "_NutTrans", [tempsource.id], [tempsink.id])
        currid += 5
        #print(currid)
for i in currentPatchStatus:
    pass
maxpreID = currid
time3 = time.time()
print("patchplaces and transitions--- %s seconds ---" % (time3 - time2))
while tick <= 1000:     #100 ticks = 1s
    timego = time.time()
    n.command("go")
    time3 = time.time()
    print("go--- %s seconds ---" % (time3 - timego))
    if True: #tick % 10 == 0:
        print("PetriNetSim at Tick #" + str(tick))
        currentBacteriaStatus = n.report("bacterias")
        currentBacteriaStatus = ast.literal_eval(currentBacteriaStatus)
        #for i in currentBacteriaStatus:
        #    if str(i[0]) == "0.0":
        #        print("BacteriaID = " + str(i[0]))
        #        print("X Coordinate = " + str(i[1]))
        #        print("Y Coordinate = " + str(i[2]))
        #        print("NutrientAmount = " + str(i[3]))
        #        print("Age = " + str(i[4]))
        #        print("Size = " + str(i[5]))
        currentPatchStatus = n.report("patchesReport")
        currentPatchStatus = ast.literal_eval(currentPatchStatus)
        #for i in currentPatchStatus:
        #    if (str(i[0]) == "1.0" and str(i[1]) == "1.0"):
        #       print(i)
        #The following needs to be done in each step, do later
        tempPetri = copy.deepcopy(environmentPetri)
        moveIDs = []
        sizeIDs = []
        replIDs = []
        nutIDs = []
        time4 = time.time()
        print("reporters and init and deepcopy--- %s seconds ---" % (time4 - time3))
        for i in currentBacteriaStatus:
            tempPetri.addPlace(maxpreID, "Bac" + "_" + str(i[0]) + "_Nut", int(i[3]), [], [])
            tempPetri.addPlace(maxpreID + 1, "Bac" + "_" + str(i[0]) + "_Size", int(i[5]), [], [])
            tempPetri.addPlace(maxpreID + 2, "Bac" + "_" + str(i[0]) + "_Move", 0, [], [])
            tempPetri.addPlace(maxpreID + 3, "Bac" + "_" + str(i[0]) + "_Repl", 0, [], [])
            tempPetri.addTransition(maxpreID + 4, "Bac_" + str(i[0]) + "_NutSizeTrans", [maxpreID], [maxpreID + 1])
            tempPetri.addTransition(maxpreID + 5, "Bac_" + str(i[0]) + "_NutMoveTrans", [maxpreID], [maxpreID + 2])
            tempPetri.addTransition(maxpreID + 6, "Bac_" + str(i[0]) + "_SizeReplTrans", [(maxpreID + 1, 10)], [maxpreID + 3])
            tempPetri.addTransition(maxpreID + 7, "PatchBac_" + str(i[0]) + "_" + str(round(i[2])) + "_" + str(round(i[1])) + "_Nut", [tempPetri.getPlaceByName("Patch_" + str(round(i[2])) + "_" + str(round(i[1])) + "_Nut").id], [maxpreID])
            moveIDs.append(maxpreID + 2)
            sizeIDs.append(maxpreID + 1)
            replIDs.append(maxpreID + 3)
            nutIDs.append(maxpreID)
            maxpreID += 8
        for i in currentPatchStatus:
            tempPetri.getPlaceByName("Patch_" + str(int(i[1])) + "_" + str(int(i[0])) + "_Nut").tokens = int(i[2])
        time5 = time.time()
        print("addbacteriaplaces and transitions--- %s seconds ---" % (time5- time4))
        tempPetri.simulateStep()
        time6 = time.time()
        print("simulationstep--- %s seconds ---" % (time6 - time5))
        #fix nutrients on initialsites not getting removed!
        for i in nutIDs:
            tempBacID = tempPetri.placeDict[i].name[4: len(tempPetri.placeDict[i].name) - 4]
            n.command("setBacteriaNut " + tempBacID + " " + str(tempPetri.placeDict[i].tokens))
        for i in moveIDs:
            tempBacID = tempPetri.placeDict[i].name[4: len(tempPetri.placeDict[i].name) - 5]
            n.command("setBacteriaMove " + tempBacID + " " + str(tempPetri.placeDict[i].tokens))
        for i in sizeIDs:
            tempBacID = tempPetri.placeDict[i].name[4: len(tempPetri.placeDict[i].name) - 5]
            n.command("setBacteriaSize " + tempBacID + " " + str(tempPetri.placeDict[i].tokens))
        for i in replIDs:
            tempBacID = tempPetri.placeDict[i].name[4: len(tempPetri.placeDict[i].name) - 5]
            n.command("setBacteriaRepl " + tempBacID + " " + str(tempPetri.placeDict[i].tokens))
        time7 = time.time()
        print("set bacteria stuff in Netlogo--- %s seconds ---" % (time7 - time6))
        totalcommandlist = []
        for i in range(0, maxycor + 1):
            for j in range(0, maxxcor + 1):
                tempcommand = []
                #timetest1 = time.time()
                correspondingPlace = tempPetri.getPlaceByName("Patch_" + str(i) + "_" + str(j) + "_Nut")
                #timetest2 = time.time()
                environmentPetri.getPlaceByName(correspondingPlace.name).tokens = correspondingPlace.tokens
                #timetest3 = time.time()
                #n.command("setPatchNutrient " + str(j) + ".0 " + str(i) + ".0 " + str(correspondingPlace.tokens))
                tempcommand.append(re.sub("'", "", str(j) + ".0 " + str(i) + ".0 " + str(correspondingPlace.tokens)))
                #timetest4 = time.time()
                #print("getPlaceByName took--- %s seconds ---" % (timetest2 - timetest1))
                #print("set tokens in environment took--- %s seconds ---" % (timetest3 - timetest2))
                #print("set patch stuff in netlogo took--- %s seconds ---" % (timetest4 - timetest3))
                totalcommandlist.append(tempcommand)
        commandlistStr = re.sub("'", "", str(totalcommandlist))
        timetest1 = time.time()
        print("preludeinpythonwork for patchupdates--- %s seconds ---" % (timetest1 - time7))
        n.command("setPlacesTotal " + re.sub(",", "", commandlistStr))
        time8 = time.time()
        print("set patch stuff in netlogo--- %s seconds ---" % (time8 - timetest1))
        del tempPetri
        gc.collect()
        time9 = time.time()
        print("garbage collection--- %s seconds ---" % (time9 - time8))

    print(tick)
    tick += 1
    print("total time for this tick--- %s seconds ---" % (time9 - timego))
print("Finished the simulation, closing netLogo")
#n.close_model()
