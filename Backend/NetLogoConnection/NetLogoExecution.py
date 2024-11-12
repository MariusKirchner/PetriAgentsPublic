__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

import ast
import platform
import time
import re
import csv
import nl4py


def executeNetLogoProject(mainProject, netLogoProjectFilepath):
    time1 = time.time()
    print("Executing NetLogoFile")
    print("Starting Netlogo from Python")

    # TODO: make user choose their NetLogoLocation
    # linux
    print(platform.platform()[0:7:])
    if platform.platform()[0:7:] == "Windows":
        #homepc
        nl4py.initialize(r"D:\UniversityPrograms\NetLogo6.3.0")
        #laptop
        #nl4py.initialize(r"C:\Program Files\NetLogo 6.3.0")
        #oldNLVersionTry
        #nl4py.initialize(r"C:\Program Files\NetLogo6.2.2")
    else:
        nl4py.initialize('/home/MariusKirchner/Desktop/Randomstuff/NetLogo-6.2.2-64/NetLogo 6.2.2/')


    n = nl4py.netlogo_app()
    time2 = time.time()
    #print("PreConfig--- %s seconds ---" % (time2 - time1))
    n.open_model(netLogoProjectFilepath)
    time3 = time.time()
    #print("Starting Netlogo--- %s seconds ---" % (time3 - time2))
    #setupstuff
    n.command("setup")
    n.command("setup")
    time4 = time.time()
    #print("double setup--- %s seconds ---" % (time4 - time3))
    csvfile = open("results.csv", "w", encoding="UTF8", newline="")
    csvwriter = csv.writer(csvfile)
    header = ["ticks"]
    for bacteria in mainProject.listOfBacteriaIDs:
        header.append(mainProject.bacteriaIDDict[bacteria].name)
        for behaviour in mainProject.bacteriaIDDict[bacteria].listOfBehPlaceIDs:
            header.append(mainProject.bacteriaIDDict[bacteria].name + mainProject.bacteriaIDDict[bacteria].dictOfBehPlaces[behaviour])
    for envmol in mainProject.listOfEnvironmentMolecules:
        header.append(envmol)
    seperatorline = ["sep=,"]
    csvwriter.writerow(seperatorline)
    csvwriter.writerow(header)
    currentBacteriaStatus = n.report("bacteriaReport")
    currentBacteriaStatus = ast.literal_eval(currentBacteriaStatus)
    for i in currentBacteriaStatus:
        #print(i)
        for j in i:
            mainProject.bacteriaIDDict[int(j[0])].addIndividual(int(j[1]))
    #runtime procedures
    time5 = time.time()
    #print("Setup the individuals--- %s seconds ---" % (time5 - time4))
    commandDict = {}
    for compartmentID in mainProject.listOfCompartmentIDs:
        for x in range(0, int(mainProject.maxXCor) + 1):
            for y in range(0, int(mainProject.maxYCor) + 1):
                if (x >= mainProject.compartmentDict[compartmentID].minX) and (x <= mainProject.compartmentDict[compartmentID].maxX):
                    if (y >= mainProject.compartmentDict[compartmentID].minY) and (y <= mainProject.compartmentDict[compartmentID].maxY):
                        commandDict[(x, y)] = compartmentID
    commandList = [[list(key)[0], list(key)[1], value] for key, value in commandDict.items()]
    time5b = time.time()
    #print("First Step of the compartments--- %s seconds ---" % (time5b - time5))
    n.command("setCompartmentAll " + re.sub(",", "", str(commandList)))
    time5a = time.time()
    #print("Setup the compartments--- %s seconds ---" % (time5a - time5b))

    for i in range(0, int(mainProject.ticks)):
        newcsvline = [i]
        time6 = time.time()
        newIndividuals = n.report("newIndiv")
        newIndividuals = ast.literal_eval(newIndividuals)
        for j in newIndividuals:
            mainProject.bacteriaIDDict[int(j[0])].addIndividual(int(j[1]))
        time7 = time.time()
        #print("Add new Individuals--- %s seconds ---" % (time7 - time6))
        deadIndividuals = n.report("deadIndiv")
        deadIndividuals = ast.literal_eval(deadIndividuals)
        for j in deadIndividuals:
            mainProject.bacteriaIDDict[int(j[0])].delIndividual(int(j[1]))
        time8 = time.time()
        #print("Delete dead individuals--- %s seconds ---" % (time8 - time7))
        intakeReport = n.report("intake")
        intakeReport = ast.literal_eval(intakeReport)
        for j in intakeReport:
            mainProject.bacteriaIDDict[int(j[0])].dictOfIndividuals[int(j[1])].petriNet.getPlaceByName("Env_" + j[2]).changeTokens(j[3])
        time9 = time.time()
        #print("Change Tokens for intakes--- %s seconds ---" % (time9 - time8))
        for k in mainProject.listOfBacteriaIDs:
            for j in mainProject.bacteriaIDDict[k].listOfIndividuals:
                mainProject.bacteriaIDDict[k].dictOfIndividuals[j].petriNet.simulateStep()
        time10 = time.time()
        #print("PetriNet Simulations --- %s seconds ---" % (time10 - time9))
        # todo: insert output functionality here, probably similar to the behaviour function below
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
        # here
        time11 = time.time()
        #print("Change patch values for outputs--- %s seconds ---" % (time11 - time10))
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
        #TODO: CHECK IF THIS REALLY WORKS!! ( looks good, but i just saw that flagella are different colors for multiple species)
        time13 = time.time()
        #print("Total for Commands for Bacteria Setters--- %s seconds ---" % (time13 - time11))
        n.command("go")
        time14 = time.time()
        #print("go command(including diffusion)--- %s seconds ---" % (time14 - time13))
        if i % 100 == 0:
            print(i)
        #write results
        for k in mainProject.listOfBacteriaIDs:
            newcsvline.append(str(len(mainProject.bacteriaIDDict[k].listOfIndividuals)))
            for behplace in mainProject.bacteriaIDDict[k].listOfBehPlaceIDs:
                counter = 0
                for bac in mainProject.bacteriaIDDict[k].listOfIndividuals:
                    if mainProject.bacteriaIDDict[k].dictOfIndividuals[bac].petriNet.placeDict[behplace].tokens >= 1:
                        counter += 1
                newcsvline.append(counter)
        patchreport = n.report("patchvalues")
        patchreporteval = ast.literal_eval(patchreport)
        for k in patchreporteval:
            newcsvline.append(int(k))
        csvwriter.writerow(newcsvline)