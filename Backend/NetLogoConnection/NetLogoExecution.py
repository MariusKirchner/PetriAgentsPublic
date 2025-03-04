__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

import ast
import copy
import json
import platform
import time
import re
import csv
import nl4py
import os.path
from multiprocessing import Pool
import concurrent.futures

def executeNetLogoProject(mainProject, netLogoProjectFilepath, amount, folderpath, guimode, window):
    # create inflow data
    window.destroy()
    global allflows
    allflows = []
    for i in range(0, int(mainProject.ticks) + 1):
        allflows.append([])
    print(allflows)
    #todo fix flow length if tickamount is changed
    for flow in mainProject.flows:
        for currtick in range(flow.finalTime[0], flow.finalTime[1] + 1):
            allflows[currtick].append(["\"" + flow.molecule.moleculeName + "\"", flow.amount, flow.finalArea[0], flow.finalArea[1]])
    print(allflows)
    time1 = time.time()
    print("Executing NetLogoFile")
    print("Starting Netlogo from Python")

    # TODO: make user choose their NetLogoLocation
    # linux
    print(platform.platform()[0:7:])
    if platform.platform()[0:7:] == "Windows":
        if os.path.exists(r"D:\UniversityPrograms\NetLogo6.3.0"):
            # homepc
            nl4py.initialize(r"D:\UniversityPrograms\NetLogo6.3.0")
        elif os.path.exists(r"C:\Program Files\NetLogo 6.3.0"):
            # laptop
            nl4py.initialize(r"C:\Program Files\NetLogo 6.3.0")
        elif os.path.exists(r"C:\Program Files\NetLogo6.2.2"):
            # oldNLVersionTry
            nl4py.initialize(r"C:\Program Files\NetLogo6.2.2")
    else:
        if os.path.exists(r'/home/MariusKirchner/Desktop/Randomstuff/NetLogo-6.2.2-64/NetLogo 6.2.2/'):
            nl4py.initialize('/home/MariusKirchner/Desktop/Randomstuff/NetLogo-6.2.2-64/NetLogo 6.2.2/')
        elif os.path.exists(r'/opt/NetLogo-6.4.0.64/'):
            nl4py.initialize('/opt/Netlogo-6.4.0-64/lib/')

    if guimode:
        n = nl4py.netlogo_app()
        parentProject = copy.deepcopy(mainProject)
        for currRun in range(0, int(amount)):
            mainProject = copy.deepcopy(parentProject)
            time2 = time.time()
            # print("PreConfig--- %s seconds ---" % (time2 - time1))
            n.open_model(netLogoProjectFilepath)
            time3 = time.time()
            # print("Starting Netlogo--- %s seconds ---" % (time3 - time2))
            # setupstuff
            n.command("setup")
            n.command("setup")
            time4 = time.time()
            # print("double setup--- %s seconds ---" % (time4 - time3))
            csvfile = open(folderpath + r"\results" + str(currRun) + ".csv", "w", encoding="UTF8", newline="")
            csvwriter = csv.writer(csvfile)
            header = ["ticks"]
            for bacteria in mainProject.listOfBacteriaIDs:
                header.append(mainProject.bacteriaIDDict[bacteria].name)
                for behaviour in mainProject.bacteriaIDDict[bacteria].listOfBehPlaceIDs:
                    header.append(mainProject.bacteriaIDDict[bacteria].name +
                                  mainProject.bacteriaIDDict[bacteria].dictOfBehPlaces[behaviour])
            for envmol in mainProject.listOfEnvironmentMolecules:
                header.append(envmol)
            seperatorline = ["sep=,"]
            csvwriter.writerow(seperatorline)
            csvwriter.writerow(header)
            currentBacteriaStatus = n.report("bacteriaReport")
            currentBacteriaStatus = ast.literal_eval(currentBacteriaStatus)
            for i in currentBacteriaStatus:
                # print(i)
                for j in i:
                    mainProject.bacteriaIDDict[int(j[0])].addIndividual(int(j[1]), True)
            # runtime procedures
            time5 = time.time()
            # print("Setup the individuals--- %s seconds ---" % (time5 - time4))
            commandDict = {}
            for compartmentID in mainProject.listOfCompartmentIDs:
                for x in range(0, int(mainProject.maxXCor) + 1):
                    for y in range(0, int(mainProject.maxYCor) + 1):
                        if (x >= mainProject.compartmentDict[compartmentID].minX) and (
                                x <= mainProject.compartmentDict[compartmentID].maxX):
                            if (y >= mainProject.compartmentDict[compartmentID].minY) and (
                                    y <= mainProject.compartmentDict[compartmentID].maxY):
                                commandDict[(x, y)] = compartmentID
            commandList = [[list(key)[0], list(key)[1], value] for key, value in commandDict.items()]
            time5b = time.time()
            # print("First Step of the compartments--- %s seconds ---" % (time5b - time5))
            n.command("setCompartmentAll " + re.sub(",", "", str(commandList)))
            time5a = time.time()
            # print("Set up the compartments--- %s seconds ---" % (time5a - time5b))
            for i in range(0, int(parentProject.ticks)):
                newcsvline = [i]
                time6 = time.time()
                newIndividuals = n.report("newIndiv")
                newIndividuals = ast.literal_eval(newIndividuals)
                for j in newIndividuals:
                    mainProject.bacteriaIDDict[int(j[0])].addIndividual(int(j[1]), False)
                time7 = time.time()
                # print("Add new Individuals--- %s seconds ---" % (time7 - time6))
                deadIndividuals = n.report("deadIndiv")
                deadIndividuals = ast.literal_eval(deadIndividuals)
                for j in deadIndividuals:
                    mainProject.bacteriaIDDict[int(j[0])].delIndividual(int(j[1]))
                time8 = time.time()
                # print("Delete dead individuals--- %s seconds ---" % (time8 - time7))
                tempCommandList = []
                for singleflow in allflows[i]:
                    tempCommandList.append(singleflow)
                commandList = re.sub("'", "", str(tempCommandList))
                n.command("doinflowAll " + re.sub(",", "", str(commandList)))
                intakeReport = n.report("intake")
                intakeReport = ast.literal_eval(intakeReport)
                for j in intakeReport:
                    mainProject.bacteriaIDDict[int(j[0])].dictOfIndividuals[int(j[1])].petriNet.getPlaceByName(
                        "Env_" + j[2]).changeTokens(j[3])
                time9 = time.time()
                # print("Change Tokens for intakes--- %s seconds ---" % (time9 - time8))
                for k in mainProject.listOfBacteriaIDs:
                    for j in mainProject.bacteriaIDDict[k].listOfIndividuals:
                        mainProject.bacteriaIDDict[k].dictOfIndividuals[j].petriNet.simulateStep()
                time10 = time.time()
                # print("PetriNet Simulations --- %s seconds ---" % (time10 - time9))
                for k in mainProject.listOfBacteriaIDs:
                    totalCommandList = []
                    for j in mainProject.bacteriaIDDict[k].listOfIndividuals:
                        singleCommand = []
                        singleCommand.append(j)
                        for m in mainProject.bacteriaIDDict[k].listOfEnvPlaceIDs:
                            singleCommand.append(
                                str(mainProject.bacteriaIDDict[k].dictOfIndividuals[j].petriNet.placeDict[m].tokens))
                        totalCommandList.append(singleCommand)
                    commandString = re.sub("'", "", str(totalCommandList))
                    n.command("setBacteria" + str(k) + "PatchAll " + re.sub(",", "", commandString))
                # here
                time11 = time.time()
                # print("Change patch values for outputs--- %s seconds ---" % (time11 - time10))
                for k in mainProject.listOfBacteriaIDs:
                    totalCommandList = []
                    for j in mainProject.bacteriaIDDict[k].listOfIndividuals:
                        singleCommand = []
                        singleCommand.append(j)
                        for m in mainProject.bacteriaIDDict[k].listOfBehPlaceIDs:
                            if mainProject.bacteriaIDDict[k].dictOfBehPlaces[m] != "None":
                                singleCommand.append(str(
                                    mainProject.bacteriaIDDict[k].dictOfIndividuals[j].petriNet.placeDict[m].tokens))
                        totalCommandList.append(singleCommand)
                    commandString = re.sub("'", "", str(totalCommandList))
                    n.command("setBacteria" + str(k) + "BehAll " + re.sub(",", "", commandString))
                # TODO: CHECK IF THIS REALLY WORKS!! (looks good, but i just saw that flagella are different colors for multiple species)
                time13 = time.time()
                # print("Total for Commands for Bacteria Setters--- %s seconds ---" % (time13 - time11))
                n.command("go")
                time14 = time.time()
                # print("go command(including diffusion)--- %s seconds ---" % (time14 - time13))
                if i % 100 == 0:
                    print("currtick (mod 100): " + str(i))
                # write results
                for k in mainProject.listOfBacteriaIDs:
                    newcsvline.append(str(len(mainProject.bacteriaIDDict[k].listOfIndividuals)))
                    for behplace in mainProject.bacteriaIDDict[k].listOfBehPlaceIDs:
                        counter = 0
                        for bac in mainProject.bacteriaIDDict[k].listOfIndividuals:
                            if mainProject.bacteriaIDDict[k].dictOfIndividuals[bac].petriNet.placeDict[
                                behplace].tokens >= 1:
                                counter += 1
                        newcsvline.append(counter)
                patchreport = n.report("patchvalues")
                patchreporteval = ast.literal_eval(patchreport)
                for k in patchreporteval:
                    newcsvline.append(int(k))
                csvwriter.writerow(newcsvline)
            csvfile.close()
            n.close_model()
            print("Finished run number: " + str(currRun))
            # n.app.disposeWorkspace()
            # n.server_starter.shutdown_server()
    else:
        listofRuns = []
        listofParentProjects = []
        listofFilePaths = []
        listoffolderpaths = []
        for i in range(0, int(amount)):
            listofRuns.append(i)
            listofParentProjects.append(mainProject)
            listofFilePaths.append(netLogoProjectFilepath)
            listoffolderpaths.append(folderpath)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            #test(1)
            #print(listofRuns)
            executor.map(runSingleWorkspace, listofParentProjects, listofFilePaths, listofRuns, listoffolderpaths)
            #print("finished")
            #executor.map(test, listofRuns)
        pass
        #parentProject, netLogoProjectFilepath, currRun, folderpath

def runSingleWorkspace(parentProject, netLogoProjectFilepath, currRun, folderpath):
    print("Starting run number: " + str(currRun))
    #time1 = time.time()
    mainProject = copy.deepcopy(parentProject)
    n = nl4py.create_headless_workspace()
    n.open_model(netLogoProjectFilepath)
    #time2 = time.time()
    #print("PreConfig--- %s seconds ---" % (time2 - time1))
    #time3 = time.time()
    #print("Starting Netlogo--- %s seconds ---" % (time3 - time2))
    # setupstuff
    n.command("setup")
    n.command("setup")
    #time4 = time.time()
    #print("double setup--- %s seconds ---" % (time4 - time3))
    csvfile = open(folderpath + r"\results" + str(currRun) + ".csv", "w", encoding="UTF8", newline="")
    csvwriter = csv.writer(csvfile)
    header = ["ticks"]
    for bacteria in mainProject.listOfBacteriaIDs:
        header.append(mainProject.bacteriaIDDict[bacteria].name)
        for behaviour in mainProject.bacteriaIDDict[bacteria].listOfBehPlaceIDs:
            header.append(mainProject.bacteriaIDDict[bacteria].name +
                          mainProject.bacteriaIDDict[bacteria].dictOfBehPlaces[behaviour])
    for envmol in mainProject.listOfEnvironmentMolecules:
        header.append(envmol)
    seperatorline = ["sep=,"]
    csvwriter.writerow(seperatorline)
    csvwriter.writerow(header)
    currentBacteriaStatus = n.report("bacteriaReport")
    currentBacteriaStatus = ast.literal_eval(currentBacteriaStatus)
    for i in currentBacteriaStatus:
        # print(i)
        for j in i:
            mainProject.bacteriaIDDict[int(j[0])].addIndividual(int(j[1]), True)
    # runtime procedures
    #time5 = time.time()
    #print("Setup the individuals--- %s seconds ---" % (time5 - time4))
    commandDict = {}
    for compartmentID in mainProject.listOfCompartmentIDs:
        for x in range(0, int(mainProject.maxXCor) + 1):
            for y in range(0, int(mainProject.maxYCor) + 1):
                if (x >= mainProject.compartmentDict[compartmentID].minX) and (
                        x <= mainProject.compartmentDict[compartmentID].maxX):
                    if (y >= mainProject.compartmentDict[compartmentID].minY) and (
                            y <= mainProject.compartmentDict[compartmentID].maxY):
                        commandDict[(x, y)] = compartmentID
    commandList = [[list(key)[0], list(key)[1], value] for key, value in commandDict.items()]
    #time5b = time.time()
    #print("First Step of the compartments--- %s seconds ---" % (time5b - time5))
    n.command("setCompartmentAll " + re.sub(",", "", str(commandList)))
    #time5a = time.time()
    #print("Set up the compartments--- %s seconds ---" % (time5a - time5b))
    #addindividualtime = 0
    #delindividualtime = 0
    #changeTokenIntaketime = 0
    #PNSimsTime = 0
    #changePatchValueTime = 0
    #BacteriaSetterTimes = 0
    #goCommandTime = 0
    #resultswritetime = 0
    #inflowTime = 0
    #getdataandevalTimeIntake = 0
    #purereporttime = 0
    #jsontime = 0
    for i in range(0, int(parentProject.ticks)):
        newcsvline = [i]
        #time6 = time.time()
        newIndividualsRaw = n.report("newIndiv")
        #newIndividuals = ast.literal_eval(newIndividuals)
        newIndividuals = json.loads(newIndividualsRaw)
        for j in newIndividuals:
            mainProject.bacteriaIDDict[int(j[0])].addIndividual(int(j[1]), False)
        #time7 = time.time()
        #print("Add new Individuals--- %s seconds ---" % (time7 - time6))
        #addindividualtime += (time7 - time6)
        deadIndividualsRaw = n.report("deadIndiv")
        #deadIndividuals = ast.literal_eval(deadIndividuals)
        deadIndividuals = json.loads(deadIndividualsRaw)
        for j in deadIndividuals:
            mainProject.bacteriaIDDict[int(j[0])].delIndividual(int(j[1]))
        #time8 = time.time()
        #print("Delete dead individuals--- %s seconds ---" % (time8 - time7))
        #delindividualtime += (time8 - time7)
        tempCommandList = []
        for singleflow in allflows[i]:
            tempCommandList.append(singleflow)
        commandList = re.sub("'", "", str(tempCommandList))
        n.command("doinflowAll " + re.sub(",", "", str(commandList)))
        #time8b = time.time()
        #inflowTime += (time8b - time8)
        intakeReportRaw = n.report("intake")
        #time8bb = time.time()
        #purereporttime += (time8bb - time8b)
        intakeReport = json.loads(intakeReportRaw)
        #time8bc = time.time()
        #jsontime += (time8bc - time8bb)
        #intakeReport = ast.literal_eval(intakeReportRaw)
        #time8c = time.time()
        #getdataandevalTimeIntake += (time8c - time8bc)
        for j in intakeReport:
            mainProject.bacteriaIDDict[int(j[0])].dictOfIndividuals[int(j[1])].petriNet.getPlaceByName(
                "Env_" + j[2]).changeTokens(j[3])
        #time9 = time.time()
        #print("Change Tokens for intakes--- %s seconds ---" % (time9 - time8c))
        #changeTokenIntaketime += (time9 - time8c)
        for k in mainProject.listOfBacteriaIDs:
            for j in mainProject.bacteriaIDDict[k].listOfIndividuals:
                mainProject.bacteriaIDDict[k].dictOfIndividuals[j].petriNet.simulateStep()
        #time10 = time.time()
        #print("PetriNet Simulations --- %s seconds ---" % (time10 - time9))
        #PNSimsTime += (time10 - time9)
        for k in mainProject.listOfBacteriaIDs:
            totalCommandList = []
            for j in mainProject.bacteriaIDDict[k].listOfIndividuals:
                singleCommand = []
                singleCommand.append(j)
                for m in mainProject.bacteriaIDDict[k].listOfEnvPlaceIDs:
                    singleCommand.append(str(mainProject.bacteriaIDDict[k].dictOfIndividuals[j].petriNet.placeDict[m].tokens))
                totalCommandList.append(singleCommand)
            commandString = re.sub("'", "", str(totalCommandList))
            n.command("setBacteria" + str(k) + "PatchAll " + re.sub(",", "", commandString))
        #time11 = time.time()
        #print("Change patch values for outputs--- %s seconds ---" % (time11 - time10))
        #changePatchValueTime += (time11 - time10)
        for k in mainProject.listOfBacteriaIDs:
            totalCommandList = []
            for j in mainProject.bacteriaIDDict[k].listOfIndividuals:
                singleCommand = []
                singleCommand.append(j)
                for m in mainProject.bacteriaIDDict[k].listOfBehPlaceIDs:
                    if mainProject.bacteriaIDDict[k].dictOfBehPlaces[m] != "None":
                        singleCommand.append(str(mainProject.bacteriaIDDict[k].dictOfIndividuals[j].petriNet.placeDict[m].tokens))
                totalCommandList.append(singleCommand)
            commandString = re.sub("'", "", str(totalCommandList))
            n.command("setBacteria" + str(k) + "BehAll " + re.sub(",", "", commandString))
        #time13 = time.time()
        #print("Total for Commands for Bacteria Setters--- %s seconds ---" % (time13 - time11))
        #BacteriaSetterTimes += (time13 - time11)
        n.command("go")
        #time14 = time.time()
        #print("go command(including diffusion)--- %s seconds ---" % (time14 - time13))
        #goCommandTime += (time14 - time13)
        if i % 100 == 0:
            print("Runnumber: " + str(currRun) + " reached tick (mod 100): " + str(i))
        # write results
        for k in mainProject.listOfBacteriaIDs:
            newcsvline.append(str(len(mainProject.bacteriaIDDict[k].listOfIndividuals)))
            for behplace in mainProject.bacteriaIDDict[k].listOfBehPlaceIDs:
                counter = 0
                for bac in mainProject.bacteriaIDDict[k].listOfIndividuals:
                    if mainProject.bacteriaIDDict[k].dictOfIndividuals[bac].petriNet.placeDict[behplace].tokens >= 1:
                        counter += 1
                newcsvline.append(counter)
        patchreportraw = n.report("patchvalues")
        #patchreporteval = ast.literal_eval(patchreport)
        patchreporteval = json.loads(patchreportraw)
        for k in patchreporteval:
            newcsvline.append(int(k))
        csvwriter.writerow(newcsvline)
        #time15 = time.time()
        #print("writing tickresults--- %s seconds ---" % (time15 - time14))
        #resultswritetime += (time15 - time14)
    csvfile.close()
    n.close_model()
    print("Finished run number: " + str(currRun))
    currRun += 1
    #print("addindiv--- %s seconds ---" % addindividualtime)
    #print("deleteindiv--- %s seconds ---" % delindividualtime)
    #print("changeintaketokens--- %s seconds ---" % changeTokenIntaketime)
    #print("inflowTime--- %s seconds ---" % inflowTime)
    #print("purereporttime--- %s seconds ---" % purereporttime)
    #print("jsontime--- %s seconds ---" % jsontime)
    #print("evalTimeIntake--- %s seconds ---" % getdataandevalTimeIntake)
    #print("pnsimstime--- %s seconds ---" % PNSimsTime)
    #print("Changepatchvalues--- %s seconds ---" % changePatchValueTime)
    #print("bacteriasetters--- %s seconds ---" % BacteriaSetterTimes)
    #print("gocommandtime--- %s seconds ---" % goCommandTime)
    #print("resultwrite--- %s seconds ---" % resultswritetime)

    n.deleteWorkspace()
    # n.server_starter.shutdown_server()
def test(n):
    print("Test")
    return "Test"
