import os
def createNetLogoProject(mainProject):
    #TODO: General idea: Modularize, maybe write in external files and load in? Only if fast, opening a bunch of files all the time might be meh, but easier to write and easier to maintain
    if os.path.isfile("./NetLogoModels/temporary.nlogo"):
        os.remove("./NetLogoModels/temporary.nlogo")
    tempnetlogoFile = open("./NetLogoModels/temporary.nlogo", "w+")
    defaultnetlogoFile = open("./NetLogoModels/DefaultNetLogo.nlogo", "r")
    for i in mainProject.listOfBacteriaIDs:
        tempnetlogoFile.write("breed [bacteria" + str(i) + " bacterium" + str(i) + "] \n")
    tempnetlogoFile.write("breed [flagella flagellum] \n")
    tempnetlogoFile.write(" \n")
    #bacteria own attributes
    for i in mainProject.listOfBacteriaIDs:
        tempnetlogoFile.write("bacteria" + str(i) + "-own [ \n")
        for j in mainProject.bacteriaIDDict[i].listOfBehPlaceIDs:
            if mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] != "None":
                tempnetlogoFile.write("\t Beh_" + mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] + " \n")
        tempnetlogoFile.write("\t dxy \n")
        tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write(" \n")
    #patches own attributes
    tempnetlogoFile.write("patches-own [ \n")
    for i in mainProject.listOfEnvironmentMolecules:
        tempnetlogoFile.write("\t patch_" + i + "\n")
    tempnetlogoFile.write("\t compartmentID \n")
    tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write("\n")
    #connectors
    tempnetlogoFile.write("directed-link-breed [connectors connector] \n")
    tempnetlogoFile.write(" \n")
    #globals
    tempnetlogoFile.write("globals [\n")
    tempnetlogoFile.write("\t local-color \n")
    tempnetlogoFile.write("\t flagella-size \n")
    tempnetlogoFile.write("\t local-time \n")
    tempnetlogoFile.write("\t timeinterval-per-tick \n")
    tempnetlogoFile.write("\t bacteria-velocity \n")
    tempnetlogoFile.write("\t flowspeed \n")
    tempnetlogoFile.write("\t newIndividuals \n")
    tempnetlogoFile.write("\t deadIndividuals \n")
    for item in mainProject.compartmentRelationDict.items():
        tempnetlogoFile.write("\t comp" + str(item[0][0]) + "Xcomp" + str(item[0][1]) + "Bac \n")
        tempnetlogoFile.write("\t comp" + str(item[0][0]) + "Xcomp" + str(item[0][1]) + "Mol \n")
    tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write(" \n")
    #setupprocedures
    tempnetlogoFile.write("to setup \n")
    #clear all values for safety reasons
    tempnetlogoFile.write("\t clear-globals \n")
    tempnetlogoFile.write("\t clear-ticks \n")
    tempnetlogoFile.write("\t clear-turtles \n")
    tempnetlogoFile.write("\t clear-patches \n")
    tempnetlogoFile.write("\t clear-drawing \n")
    tempnetlogoFile.write("\t clear-output \n")
    tempnetlogoFile.write("\t reset-ticks \n")
    #set globals
    tempnetlogoFile.write("\t set timeinterval-per-tick 1 \n")
    tempnetlogoFile.write("\t set bacteria-velocity 0.3 \n")
    tempnetlogoFile.write("\t set flowspeed 0.1 \n")
    tempnetlogoFile.write("\t set newIndividuals [] \n")
    tempnetlogoFile.write("\t set deadIndividuals [] \n")
    #create bacteria
    for i in mainProject.listOfBacteriaIDs:
        tempnetlogoFile.write("\t create-bacteria" + str(i) + " " + str(mainProject.bacteriaIDDict[i].MOI) + "[ \n")
        tempnetlogoFile.write("\t \t setxy random-xcor random-ycor \n")
        tempnetlogoFile.write("\t \t set size 1 \n")
        for j in mainProject.bacteriaIDDict[i].listOfBehPlaceIDs:
            if mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] != "None":
                tempnetlogoFile.write("\t \t set Beh_" + mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] + " 0 \n")
        if mainProject.bacteriaIDDict[i].flagella:
            tempnetlogoFile.write("\t \t make-flagella \n")
        tempnetlogoFile.write("\t ] \n")
    for i in mainProject.listOfBacteriaIDs:
        tempnetlogoFile.write("\t set-default-shape bacteria" + str(i) + " \"" + mainProject.bacteriaIDDict[i].shapeRepresentation + "\" \n")
    tempnetlogoFile.write("\t set-default-shape flagella \"flagella\" \n")
    for i in mainProject.listOfBacteriaIDs:
        tempnetlogoFile.write("\t ask bacteria" + str(i) + " [ \n")
        tempnetlogoFile.write("\t \t set dxy ( bacteria-velocity * timeinterval-per-tick ) \n")
        print(mainProject.bacteriaIDDict[i].colorRepresentation)
        tempnetlogoFile.write("\t \t set color [" + str(mainProject.bacteriaIDDict[i].colorRepresentation[0]) + " " + str(mainProject.bacteriaIDDict[i].colorRepresentation[1]) + " " + str(mainProject.bacteriaIDDict[i].colorRepresentation[2]) + " ] \n")
        tempnetlogoFile.write("\t \t set local-color color \n")
        tempnetlogoFile.write("\t \t ask out-link-neighbors [set color local-color] \n")
        tempnetlogoFile.write("\t ] \n")
    #set patchvalues, these are examples
    for i in mainProject.listOfEnvironmentMolecules:
        currMol = mainProject.dictOfEnvironmentMolecules[i]
        tempnetlogoFile.write("\t ask patches with [pxcor >= " + str(currMol.distArea[0][0]) + " and pxcor <= " + str(currMol.distArea[1][0]) + " and pycor >= " + str(currMol.distArea[0][1]) + " and pycor <= " + str(currMol.distArea[1][1]) + "][ \n")
        tempnetlogoFile.write("\t \t set patch_" + i + " random " + str(currMol.distAmount) + " \n")
        tempnetlogoFile.write("\t ]")
    #for scarce food: with [pxcor < 50 and pycor < 50]
    #tempnetlogoFile.write("\t ask patches[ \n")
    # exemplary distributions!
    #for i in mainProject.listOfEnvironmentMolecules:
    #    tempnetlogoFile.write("\t \t set patch_" + i + " random 200 \n")
    #tempnetlogoFile.write("\t ] \n")
    #tempnetlogoFile.write("\t \t set patch_Nut random 6 \n")
    #tempnetlogoFile.write("\t \t set patch_Repl_Inhib random 2 \n")
    #tempnetlogoFile.write("\t \t set patch_Poison random 2 \n")
    #tempnetlogoFile.write("\t ] \n")
    #tempnetlogoFile.write("\t ask patch 5 10 [ \n")
    #tempnetlogoFile.write("\t \t set patch_Nut 1000 \n")
    #tempnetlogoFile.write("\t ] \n")
    #tempnetlogoFile.write("\t ask patch 5 40 [ \n")
    #tempnetlogoFile.write("\t \t set patch_Nut 1000 \n")
    #tempnetlogoFile.write("\t ] \n")
    #until here
    for item in mainProject.compartmentRelationDict.items():
        tempnetlogoFile.write("\t set comp" + str(item[0][0]) + "Xcomp" + str(item[0][1]) + "Bac " + str(item[1][0]) + " \n")
        tempnetlogoFile.write("\t set comp" + str(item[0][0]) + "Xcomp" + str(item[0][1]) + "Mol " + str(item[1][1]) + " \n")
    tempnetlogoFile.write("\t set flagella-size 1 \n")
    tempnetlogoFile.write("\t updateView \n")
    tempnetlogoFile.write("end \n")
    tempnetlogoFile.write("\n")
    #set patch compartment function
    tempnetlogoFile.write("to setCompartment [x y newCompartmentID] \n")
    tempnetlogoFile.write("\t ask patch x y [ \n")
    tempnetlogoFile.write("\t \t set compartmentID newCompartmentID \n")
    tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write("end \n")
    #set patch compartment all
    tempnetlogoFile.write("to setCompartmentAll [listOfCommands] \n")
    tempnetlogoFile.write("\t foreach listOfCommands [ \n")
    tempnetlogoFile.write("\t \t [content] -> \n")
    tempnetlogoFile.write("\t \t setCompartment (item 0 content) (item 1 content) (item 2 content) \n")
    tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write("end \n")
    #make flagella function
    tempnetlogoFile.write("to make-flagella \n")
    tempnetlogoFile.write("\t let flagella-shape (word \"flagella\" 1) \n")
    tempnetlogoFile.write("\t hatch 1 [ \n")
    tempnetlogoFile.write("\t \t set breed flagella \n")
    tempnetlogoFile.write("\t \t set color blue \n")
    tempnetlogoFile.write("\t \t set label \"\" \n")
    tempnetlogoFile.write("\t \t set shape \"flagella-4\" \n")
    tempnetlogoFile.write("\t \t bk 0.5 \n")
    tempnetlogoFile.write("\t \t set size 1 \n")
    tempnetlogoFile.write("\t \t create-connector-from myself [ \n")
    tempnetlogoFile.write("\t \t \t set hidden? true \n")
    tempnetlogoFile.write("\t \t \t tie \n")
    tempnetlogoFile.write("\t \t ] \n")
    tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write("end \n")
    tempnetlogoFile.write(" \n")
    #runtime procedures
    #standard go
    tempnetlogoFile.write("to go \n")
    #tempnetlogoFile.write("\t patch-intakes \n")
    for i in mainProject.listOfBacteriaIDs:
        tempnetlogoFile.write("\t ask bacteria" + str(i) + " [ \n")
        for j in mainProject.bacteriaIDDict[i].listOfBehPlaceIDs:
            if mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] != "None":
                tempnetlogoFile.write("\t \t if (Beh_" + mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] + " != 0) [ \n")
                #tempnetlogoFile.write("\t \t \t let tempList [] \n")
                #tempnetlogoFile.write("\t \t \t set tempList lput who tempList \n")
                tempnetlogoFile.write("\t \t \t bacteria" + str(i) + "_" + mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] + " who \n")
                tempnetlogoFile.write("\t \t ] \n")
        tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write("\t ask flagella with [not any? my-links][die] \n")
    if mainProject.diffBool or mainProject.flowBool:
        tempnetlogoFile.write("\t patchdiffusion \n")
    tempnetlogoFile.write("\t tick \n")
    tempnetlogoFile.write("\t set local-time ticks * timeinterval-per-tick \n")
    tempnetlogoFile.write("\t updateView \n")
    tempnetlogoFile.write("end \n")
    tempnetlogoFile.write("\n")

    if mainProject.diffBool or mainProject.flowBool:
        #diffusion and flow function
        #TODO: include flow and diffusion rates
        #TODO: single tokens get moved multiple times if netlogo opens them multiple times patch after patch! => save them to a list or similar and add them after everything happened
        if mainProject.diffBool and mainProject.flowBool:
            directionalList = [3, 7, 15, 25, 15, 7, 3, 5]
            stayProb = 20
        elif mainProject.diffBool:
            useList = [5, 10, 5, 10, 10, 5, 10, 5]
            stayProb = 40
        elif mainProject.flowBool:
            directionalList = [0, 0, 0, 75, 0, 0, 0, 0]
            stayProb = 25
        if mainProject.flowBool:
            if mainProject.flowDir == "S":
                useList = [directionalList[0], directionalList[1], directionalList[2], directionalList[7], directionalList[3], directionalList[6], directionalList[5], directionalList[4]]
            elif mainProject.flowDir == "SW":
                useList = [directionalList[1], directionalList[2], directionalList[3], directionalList[0], directionalList[4], directionalList[7], directionalList[6], directionalList[5]]
            elif mainProject.flowDir == "W":
                useList = [directionalList[2], directionalList[3], directionalList[4], directionalList[1], directionalList[5], directionalList[0], directionalList[7], directionalList[6]]
            elif mainProject.flowDir == "NW":
                useList = [directionalList[3], directionalList[4], directionalList[5], directionalList[2], directionalList[6], directionalList[1], directionalList[0], directionalList[7]]
            elif mainProject.flowDir == "N":
                useList = [directionalList[4], directionalList[5], directionalList[6], directionalList[3], directionalList[7], directionalList[2], directionalList[1], directionalList[0]]
            elif mainProject.flowDir == "NE":
                useList = [directionalList[5], directionalList[6], directionalList[7], directionalList[4], directionalList[0], directionalList[3], directionalList[2], directionalList[1]]
            elif mainProject.flowDir == "E":
                useList = [directionalList[6], directionalList[7], directionalList[0], directionalList[5], directionalList[1], directionalList[4], directionalList[3], directionalList[2]]
            elif mainProject.flowDir == "SE":
                useList = [directionalList[7], directionalList[0], directionalList[1], directionalList[6], directionalList[2], directionalList[5], directionalList[4], directionalList[3]]

        tempnetlogoFile.write("to patchdiffusion \n")
        #TODO: SEPERATE DIFFUSION AND FLOW! IT IS NOT THE SAME!!!! RENAME EVERYTHING FLOW TO FLOW!
        tempnetlogoFile.write("\t let tempList [] \n")
        tempnetlogoFile.write("\t ask patches [ \n")
        for i in mainProject.listOfEnvironmentMolecules:
            tempnetlogoFile.write("\t \t set tempList range patch_" + i + " \n")
            tempnetlogoFile.write("\t \t foreach tempList [ \n")
            tempnetlogoFile.write("\t \t \t let randomDirection random 100 \n")
            tempnetlogoFile.write("\t \t \t (ifelse \n")
            counter = 0
            add = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0:
                        add += stayProb
                        tempnetlogoFile.write("\t \t \t (randomDirection < " + str(add) + ")[ \n")
                        tempnetlogoFile.write("\t \t \t ;nothing happens as the random decider decided to leave the molecule in place \n")
                        tempnetlogoFile.write("\t \t \t ] \n")
                    else:
                        add += useList[counter]
                        tempnetlogoFile.write("\t \t \t (randomDirection < " + str(add) + ")[ \n")
                        tempnetlogoFile.write("\t \t \t \t (ifelse (pxcor + " + str(x) + " <= max-pxcor and pxcor + " + str(x) + " >= min-pxcor and pycor + " + str(y) + " <= max-pycor and pycor + " + str(y) + " >= min-pycor) \n")
                        tempnetlogoFile.write("\t \t \t \t [ \n")
                        tempnetlogoFile.write("\t \t \t \t \t ifelse ([compartmentID] of patch (pxcor + " + str(x) + ") (pycor + " + str(y) + ") != compartmentID) \n")
                        tempnetlogoFile.write("\t \t \t \t \t [ \n")
                        tempnetlogoFile.write("\t \t \t \t \t \t ifelse ((runresult (word \"comp\" (compartmentID) \"Xcomp\" ([compartmentID] of patch (pxcor + " + str(x) + ") (pycor + " + str(y) + ")) \"Mol\" )) = 0) \n")
                        tempnetlogoFile.write("\t \t \t \t \t \t \t [ \n")
                        tempnetlogoFile.write("\t \t \t \t \t \t \t ;nothing happens as the molecule cant flow into target \n")
                        tempnetlogoFile.write("\t \t \t \t \t \t \t ] \n")
                        tempnetlogoFile.write("\t \t \t \t \t \t \t [ \n")
                        tempnetlogoFile.write("\t \t \t \t \t \t \t \t ;different compartments but flow allowed\n")
                        tempnetlogoFile.write("\t \t \t \t \t \t \t \t set patch_" + i + " (patch_" + i + " - 1) \n")
                        tempnetlogoFile.write("\t \t \t \t \t \t \t \t ask patch (pxcor + " + str(x) + ") (pycor + " + str(y) + ")[ \n")
                        tempnetlogoFile.write("\t \t \t \t \t \t \t \t \t  set patch_" + i + " (patch_" + i + " + 1) \n")
                        tempnetlogoFile.write("\t \t \t \t \t \t \t \t ] \n")
                        tempnetlogoFile.write("\t \t \t \t \t \t \t ] \n")
                        tempnetlogoFile.write("\t \t \t \t \t ] \n")
                        tempnetlogoFile.write("\t \t \t \t \t [ \n")
                        tempnetlogoFile.write("\t \t \t \t \t set patch_" + i + " (patch_" + i + " - 1) \n")
                        tempnetlogoFile.write("\t \t \t \t \t ask patch (pxcor + " + str(x) + ") (pycor + " + str(y) + ")[ \n")
                        tempnetlogoFile.write("\t \t \t \t \t \t set patch_" + i + " (patch_" + i + " + 1) \n")
                        tempnetlogoFile.write("\t \t \t \t \t ] \n")
                        tempnetlogoFile.write("\t \t \t \t \t ] \n")
                        tempnetlogoFile.write("\t \t \t \t ] \n")
                        tempnetlogoFile.write("\t \t \t \t (pxcor + " + str(x) + " > max-pxcor) [ \n")
                        tempnetlogoFile.write("\t \t \t \t set patch_" + i + " (patch_" + i + " - 1) \n")
                        tempnetlogoFile.write("\t \t \t \t ]) \n")
                        tempnetlogoFile.write("\t \t \t ] \n")
                        counter += 1
            tempnetlogoFile.write("\t \t \t ) \n")
            tempnetlogoFile.write("\t \t ] \n")
        tempnetlogoFile.write("\t ] \n")
        tempnetlogoFile.write("end \n")

    #update View function (TODO: EXTEND, make it user dependant)
    tempnetlogoFile.write("to updateView \n")
    tempnetlogoFile.write("\t ask patches [ \n")
    tempnetlogoFile.write("\t \t if (patch_" + mainProject.listOfEnvironmentMolecules[0] + " = 0) [set pcolor 5] \n")
    tempnetlogoFile.write("\t \t if (patch_" + mainProject.listOfEnvironmentMolecules[0] + " > 0) [set pcolor 19] \n")
    tempnetlogoFile.write("\t \t if (patch_" + mainProject.listOfEnvironmentMolecules[0] + " > 25) [set pcolor 18] \n")
    tempnetlogoFile.write("\t \t if (patch_" + mainProject.listOfEnvironmentMolecules[0] + " > 50) [set pcolor 17] \n")
    tempnetlogoFile.write("\t \t if (patch_" + mainProject.listOfEnvironmentMolecules[0] + " > 75) [set pcolor 16] \n")
    tempnetlogoFile.write("\t \t if (patch_" + mainProject.listOfEnvironmentMolecules[0] + " > 100) [set pcolor 15] \n")
    #tempnetlogoFile.write("\t \t \t set pcolor 5 \n ")
    tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write("end \n")
    tempnetlogoFile.write("\n")

    #behaviour functions
    #extend these for more behaviours
    #These are for now filled with placeholder behaviour for movement, replication and death
    #This should probably be changed by the user depending on the bacteria
    #things like movement speed, movement type (flagellar, linear etc.)
    #same for replication, change variables by user (timespan, where to spawn, size after etc.)

    for i in mainProject.listOfBacteriaIDs:
        if "Move" in mainProject.bacteriaIDDict[i].dictOfBehPlaces.values():
            if mainProject.lrCont and mainProject.tbCont:
                tempnetlogoFile.write("to bacteria" + str(i) + "_" + "Move" + " [ id ] \n")
                tempnetlogoFile.write("\t ask turtle id [ \n")
                tempnetlogoFile.write("\t \t forward dxy \n")
                tempnetlogoFile.write("\t \t right (5 - random-float 10) \n")
                tempnetlogoFile.write("\t \t set Beh_Move (Beh_Move - 1) \n")
                tempnetlogoFile.write("\t ] \n")
                tempnetlogoFile.write("end \n")
            else:
                #TODO: change the first ifelse with 0.5 difference to dxy difference and check if out of bounds?
                tempnetlogoFile.write("to bacteria" + str(i) + "_" + "Move" + " [ id ] \n")
                tempnetlogoFile.write("\t ask turtle id [ \n")
                tempnetlogoFile.write("\t \t (ifelse \n")
                tempnetlogoFile.write("\t \t \t (patch-at dx 0 = nobody) \n")
                tempnetlogoFile.write("\t \t \t [ \n")
                tempnetlogoFile.write("\t \t \t \t set heading (- heading) \n")
                tempnetlogoFile.write("\t \t \t \t forward dxy \n")
                tempnetlogoFile.write("\t \t \t \t ask out-link-neighbors \n")
                tempnetlogoFile.write("\t \t \t \t [ \n")
                tempnetlogoFile.write("\t \t \t \t \t setxy ([xcor] of myself) ([ycor] of myself) \n")
                tempnetlogoFile.write("\t \t \t \t \t set heading ([heading] of myself)\n")
                tempnetlogoFile.write("\t \t \t \t \t bk 2 \n")
                tempnetlogoFile.write("\t \t \t \t ] \n")
                tempnetlogoFile.write("\t \t \t ] \n")
                tempnetlogoFile.write("\t \t \t (patch-at 0 dy) = nobody \n")
                tempnetlogoFile.write("\t \t \t [ \n")
                tempnetlogoFile.write("\t \t \t \t set heading (180 - heading) \n")
                tempnetlogoFile.write("\t \t \t \t forward dxy \n")
                tempnetlogoFile.write("\t \t \t \t ask out-link-neighbors \n")
                tempnetlogoFile.write("\t \t \t \t [ \n")
                tempnetlogoFile.write("\t \t \t \t \t setxy ([xcor] of myself) ([ycor] of myself) \n")
                tempnetlogoFile.write("\t \t \t \t \t set heading ([heading] of myself)\n")
                tempnetlogoFile.write("\t \t \t \t \t bk 2 \n")
                tempnetlogoFile.write("\t \t \t \t ] \n")
                tempnetlogoFile.write("\t \t \t ] \n")
                tempnetlogoFile.write("\t \t \t ([compartmentID] of patch-here != [compartmentID] of patch-ahead dxy) \n")
                tempnetlogoFile.write("\t \t \t [ \n")
                tempnetlogoFile.write("\t \t \t \t ifelse (runresult (word \"comp\" ([compartmentID] of patch-here) \"Xcomp\" ([compartmentID] of patch-ahead dxy) \"Bac\")) = 0 \n")
                tempnetlogoFile.write("\t \t \t \t [ \n")
                tempnetlogoFile.write("\t \t \t \t \t set heading heading + 180 \n")
                tempnetlogoFile.write("\t \t \t \t \t forward dxy")
                tempnetlogoFile.write("\t \t \t \t \t ask out-link-neighbors \n")
                tempnetlogoFile.write("\t \t \t \t \t [ \n")
                tempnetlogoFile.write("\t \t \t \t \t \t setxy ([xcor] of myself) ([ycor] of myself) \n")
                tempnetlogoFile.write("\t \t \t \t \t \t set heading ([heading] of myself) \n")
                tempnetlogoFile.write("\t \t \t \t \t \t bk 2 \n")
                tempnetlogoFile.write("\t \t \t \t \t ] \n")
                tempnetlogoFile.write("\t \t \t \t ] \n")
                tempnetlogoFile.write("\t \t \t \t [ \n")
                tempnetlogoFile.write("\t \t \t \t \t forward dxy \n")
                tempnetlogoFile.write("\t \t \t \t \t right (5 - random-float 10) \n")
                tempnetlogoFile.write("\t \t \t \t \t set Beh_Move (Beh_Move - 1) \n")
                tempnetlogoFile.write("\t \t \t \t ] \n")
                tempnetlogoFile.write("\t \t \t ] \n")
                tempnetlogoFile.write("\t \t \t [ \n")
                tempnetlogoFile.write("\t \t \t \t forward dxy \n")
                tempnetlogoFile.write("\t \t \t \t right (5 - random-float 10) \n")
                tempnetlogoFile.write("\t \t \t \t set Beh_Move (Beh_Move - 1) \n")
                tempnetlogoFile.write("\t \t \t ] \n")
                tempnetlogoFile.write("\t \t ) \n")
                tempnetlogoFile.write("\t ] \n")
                tempnetlogoFile.write("end \n")
        #Does this work for noncontinuos regions? How to handle compartments?
        #rfvbgedTODO: for now bacteria spawn new bacteria at the same place to handle this - maybe try below at some point
        #maybe check positions if in compartment, if not => closer repr => check again, rinse and repeat
        if "Tumble" in mainProject.bacteriaIDDict[i].dictOfBehPlaces.values():
            tempnetlogoFile.write("to bacteria" + str(i) + "_" + "Tumble" + " [ id ] \n")
            tempnetlogoFile.write("\t ask turtle id [ \n")
            tempnetlogoFile.write("\t \t set heading (heading + random-float 360) \n")
            tempnetlogoFile.write("\t ] \n")
            tempnetlogoFile.write("end \n")
        if "Replication" in mainProject.bacteriaIDDict[i].dictOfBehPlaces.values():
            tempnetlogoFile.write("to bacteria" + str(i) + "_" + "Replication" + " [ id ] \n")
            tempnetlogoFile.write("\t ask turtle id [ \n")
            tempnetlogoFile.write("\t \t hatch-bacteria" + str(i) + " 1 [ \n")
            tempnetlogoFile.write("\t \t \t setxy xcor ycor \n")
            tempnetlogoFile.write("\t \t \t set heading (heading + random-float 360) \n")
            tempnetlogoFile.write("\t \t \t set size 1 \n")
            for j in mainProject.bacteriaIDDict[i].listOfBehPlaceIDs:
                if mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] != "None":
                    tempnetlogoFile.write("\t \t \t set Beh_" + mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] + " 0 \n")
            # TODO:make check for flagella and enable with it
            #tempnetlogoFile.write("\t \t \t make-flagella \n")
            tempnetlogoFile.write("\t \t \t set color [" + str(mainProject.bacteriaIDDict[i].colorRepresentation[0]) + " " + str(mainProject.bacteriaIDDict[i].colorRepresentation[1]) + " " + str(mainProject.bacteriaIDDict[i].colorRepresentation[2]) + " ] \n")
            tempnetlogoFile.write("\t \t \t set local-color color \n")
            tempnetlogoFile.write("\t \t \t ask out-link-neighbors [set color local-color] \n")
            tempnetlogoFile.write("\t \t \t let tempList [] \n")
            tempnetlogoFile.write("\t \t \t set tempList lput " + str(i) + " tempList \n")
            tempnetlogoFile.write("\t \t \t set tempList lput who tempList \n")
            tempnetlogoFile.write("\t \t \t set newIndividuals lput tempList newIndividuals \n")
            tempnetlogoFile.write("\t \t ] \n")
            tempnetlogoFile.write("\t \t set size 1 \n")
            tempnetlogoFile.write("\t ] \n")
            tempnetlogoFile.write("end \n")
        if "Size" in mainProject.bacteriaIDDict[i].dictOfBehPlaces.values():
            tempnetlogoFile.write("to bacteria" + str(i) + "_" + "Size" + " [ id ]  \n")
            tempnetlogoFile.write("\t ask turtle id [ \n")
            tempnetlogoFile.write("\t \t if (Beh_Size > 5) [ \n")
            tempnetlogoFile.write("\t \t \t set size 2 \n")
            tempnetlogoFile.write("\t \t ] \n")
            tempnetlogoFile.write("\t \t if (Beh_Size > 10) [ \n")
            tempnetlogoFile.write("\t \t \t set size 3 \n")
            tempnetlogoFile.write("\t \t ] \n")
            tempnetlogoFile.write("\t ] \n")
            tempnetlogoFile.write("end \n")
        if "Death" in mainProject.bacteriaIDDict[i].dictOfBehPlaces.values():
            tempnetlogoFile.write("to bacteria" + str(i) + "_" + "Death" + " [ id ] \n")
            tempnetlogoFile.write("\t ask turtle id [ \n")
            tempnetlogoFile.write("\t \t let tempList [] \n")
            tempnetlogoFile.write("\t \t set tempList lput " + str(i) + " tempList \n")
            tempnetlogoFile.write("\t \t set tempList lput who tempList \n")
            tempnetlogoFile.write("\t \t set deadIndividuals lput tempList deadIndividuals \n")
            tempnetlogoFile.write("\t \t ask my-links [ die ] \n")
            tempnetlogoFile.write("\t \t die \n")
            tempnetlogoFile.write("\t ] \n")
            tempnetlogoFile.write("end \n")

    #patchintakefunction
    tempnetlogoFile.write("to patch-intakes \n")
    for i in mainProject.listOfBacteriaIDs:
        tempnetlogoFile.write("\t ask bacteria" + str(i) + " [ \n")
        tempnetlogoFile.write("\t \t ask patch-here [ \n")
        for j in mainProject.bacteriaIDDict[i].listOfEnvPlaces:
            tempnetlogoFile.write("\t \t \t if (patch_" + j + " > 0) [ \n")
            tempnetlogoFile.write("\t \t \t \t set patch_" + j + " (patch_" + j + " - 1) \n")
            tempnetlogoFile.write("\t \t \t ] \n")
        tempnetlogoFile.write("\t \t ] \n")
        tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write("end \n")
    #setBehaviour functions
    for i in mainProject.listOfBacteriaIDs:
        tempString = "[ id "
        for j in mainProject.bacteriaIDDict[i].listOfBehPlaceIDs:
            if mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] != "None":
                tempString += ("Beh" + mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] + " ") #maybe parenthesis gone
        tempString += "]"
        tempnetlogoFile.write("to setBacteria" + str(i) + "Beh " + tempString + " \n")
        tempnetlogoFile.write("\t ask turtle id [ \n")
        for j in mainProject.bacteriaIDDict[i].listOfBehPlaceIDs:
            if mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] != "None":
                tempnetlogoFile.write("\t \t set Beh_" + mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] + " Beh" + mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] + " \n")
        tempnetlogoFile.write("\t ] \n")
        tempnetlogoFile.write("end \n")
    #new setAllBehaviour functions
    for i in mainProject.listOfBacteriaIDs:
        tempString = ""
        x = 0
        for j in mainProject.bacteriaIDDict[i].listOfBehPlaceIDs:
            if mainProject.bacteriaIDDict[i].dictOfBehPlaces[j] != "None":
                tempString += "(item " + str(x) + " content) "
                x += 1
        tempString += "(item " + str(x) + " content) "
        tempnetlogoFile.write("to setBacteria" + str(i) + "BehAll " + "[ listOfCommands ]" + " \n")
        tempnetlogoFile.write("\t foreach listOfCommands [ \n")
        tempnetlogoFile.write("\t \t [content] -> \n")
        tempnetlogoFile.write("\t \t setBacteria" + str(i) + "Beh " + tempString + " \n")
        tempnetlogoFile.write("\t ] \n")
        tempnetlogoFile.write("end \n")
    #setPatch function
    #TODO: Fix for different intake numbers than 1
    for i in mainProject.listOfBacteriaIDs:
        tempString = "[ id "
        for j in mainProject.bacteriaIDDict[i].listOfEnvPlaceIDs:
            if mainProject.bacteriaIDDict[i].dictOfEnvPlaces[j] != "None":
                tempString += (mainProject.bacteriaIDDict[i].dictOfEnvPlaces[j] + " ") #maybe parenthesis gone
        tempString += "]"
        tempnetlogoFile.write("to setBacteria" + str(i) + "Patch " + tempString + " \n")
        tempnetlogoFile.write("\t ask turtle id [ \n")
        tempnetlogoFile.write("\t \t ask patch-here [ \n")
        for j in mainProject.bacteriaIDDict[i].listOfEnvPlaceIDs:
            tempnetlogoFile.write("\t \t \t set patch_" + mainProject.bacteriaIDDict[i].dictOfEnvPlaces[j] + " " + mainProject.bacteriaIDDict[i].dictOfEnvPlaces[j] + " \n")
        tempnetlogoFile.write("\t \t ] \n")
        tempnetlogoFile.write("\t ] \n")
        tempnetlogoFile.write("end \n")
    #setAllPatches function
    for i in mainProject.listOfBacteriaIDs:
        tempString = ""
        x = 0
        for j in mainProject.bacteriaIDDict[i].listOfEnvPlaceIDs:
            if mainProject.bacteriaIDDict[i].dictOfEnvPlaces[j] != "None":
                tempString += "(item " + str(x) + " content) "
                x += 1
        tempString += "(item " + str(x) + " content) "
        tempnetlogoFile.write("to setBacteria" + str(i) + "PatchAll " + "[ listOfCommands ]" + " \n")
        tempnetlogoFile.write("\t foreach listOfCommands [ \n")
        tempnetlogoFile.write("\t \t [content] -> \n")
        tempnetlogoFile.write("\t \t setBacteria" + str(i) + "Patch " + tempString + " \n")
        tempnetlogoFile.write("\t ] \n")
        tempnetlogoFile.write("end \n")
    #single inflow function
    tempnetlogoFile.write("to doinflow [ molecule amount starty endy ] \n")
    tempnetlogoFile.write("\t while [starty <= endy] [ \n")
    tempnetlogoFile.write("\t \t ask patch 0 starty [ \n")
    tempnetlogoFile.write("\t \t \t (run (word \"set patch_\" molecule \" patch_\" molecule \" + \" amount)) \n")
    tempnetlogoFile.write("\t \t \t set starty (starty + 1) \n")
    tempnetlogoFile.write("\t \t ] \n")
    tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write("end \n")
    #allinflow function
    tempnetlogoFile.write("to doinflowAll " + "[ listOfCommands ]" + " \n")
    tempnetlogoFile.write("\t foreach listOfCommands [ \n")
    tempnetlogoFile.write("\t \t [content] -> \n")
    tempnetlogoFile.write("\t \t doinflow (item 0 content) (item 1 content) (item 2 content) (item 3 content) \n")
    tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write("end \n")

    #pushfunction
    #TODO make it custom in GUI
    #TODO: add compartment detection for these spawns (and probably the normal repl as well) (for some reason normal repl seems to work)
    tempnetlogoFile.write("to pushfunction [ currBacID ] \n")
    tempnetlogoFile.write("\t ask turtle currBacID [ \n")
    tempnetlogoFile.write("\t \t let push-dir heading \n")
    tempnetlogoFile.write("\t \t ask other turtles-on patch-here [ \n")
    tempnetlogoFile.write("\t \t \t let olddir heading \n")
    tempnetlogoFile.write("\t \t \t set heading push-dir \n")
    tempnetlogoFile.write("\t \t \t fd 2 \n")
    tempnetlogoFile.write("\t \t \t pushfunction who \n")
    tempnetlogoFile.write("\t \t \t set heading olddir \n")
    tempnetlogoFile.write("\t \t ] \n")
    tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write("end \n")


    #reportfunctions
    #tempList each individual
    #bacList each bacteriatype
    #wholeList all of them
    tempnetlogoFile.write("to-report bacteriaReport \n")
    tempnetlogoFile.write("\t let tempList [] \n")
    tempnetlogoFile.write("\t let bacList [] \n")
    tempnetlogoFile.write("\t let wholeList [] \n")
    for i in mainProject.listOfBacteriaIDs:
        tempnetlogoFile.write("\t ask bacteria" + str(i) + " [ \n")
        tempnetlogoFile.write("\t \t set tempList lput " + str(i) + " tempList \n")
        tempnetlogoFile.write("\t \t set tempList lput who tempList \n")
        tempnetlogoFile.write("\t \t set bacList lput tempList bacList \n")
        tempnetlogoFile.write("\t \t set tempList [] \n")
        tempnetlogoFile.write("\t ] \n")
        tempnetlogoFile.write("\t set wholeList lput bacList wholeList \n")
        tempnetlogoFile.write("\t set bacList [] \n")
    tempnetlogoFile.write("\t report wholeList \n")
    tempnetlogoFile.write("end \n")
    tempnetlogoFile.write("\n")

    #newIndividuals
    tempnetlogoFile.write("to-report newIndiv \n")
    tempnetlogoFile.write("\t let tempList newIndividuals \n")
    tempnetlogoFile.write("\t set newIndividuals [] \n")
    tempnetlogoFile.write("\t report tempList \n")
    tempnetlogoFile.write("end \n")

    # deadIndividuals
    tempnetlogoFile.write("to-report deadIndiv \n")
    tempnetlogoFile.write("\t let tempList deadIndividuals \n")
    tempnetlogoFile.write("\t set deadIndividuals [] \n")
    tempnetlogoFile.write("\t report tempList \n")
    tempnetlogoFile.write("end \n")

    tempnetlogoFile.write("to-report intake \n")
    tempnetlogoFile.write("\t let tempList [] \n")
    tempnetlogoFile.write("\t let wholeList [] \n")
    tempnetlogoFile.write("\t let bacType 0 \n")
    for i in mainProject.listOfBacteriaIDs:
        tempnetlogoFile.write("\t set bacType " + str(i) + " \n")
        tempnetlogoFile.write("\t ask bacteria" + str(i) + " [ \n")
        tempnetlogoFile.write("\t \t let tempID who \n")
        tempnetlogoFile.write("\t \t ask patch-here [ \n")
        for j in mainProject.bacteriaIDDict[i].listOfEnvPlaces:
            tempnetlogoFile.write(" \t \t \t set tempList lput bacType tempList \n")
            tempnetlogoFile.write(" \t \t \t set tempList lput tempID tempList\n")
            tempnetlogoFile.write(" \t \t \t set tempList lput \"\\\"" + j + "\\\"\" templist \n")
            tempnetlogoFile.write(" \t \t \t set tempList lput patch_" + j + " templist \n")
            tempnetlogoFile.write(" \t \t \t set wholeList lput tempList wholeList \n")
            tempnetlogoFile.write(" \t \t \t set tempList [] \n")
        tempnetlogoFile.write("\t \t ] \n")
        tempnetlogoFile.write("\t ] \n")
    tempnetlogoFile.write("\t report wholeList \n")
    tempnetlogoFile.write("end \n")

    tempnetlogoFile.write("to-report patchvalues \n")
    tempnetlogoFile.write("\t let templist [] \n")
    for j in mainProject.listOfEnvironmentMolecules:
        tempnetlogoFile.write("\t let tempvalue" + j + " 0 \n")
    tempnetlogoFile.write("\t ask patches [ \n")
    for j in mainProject.listOfEnvironmentMolecules:
        tempnetlogoFile.write("\t \t set tempvalue" + j + " tempvalue" + j + " + patch_" + j + " \n")
    tempnetlogoFile.write("\t ] \n ")
    for j in mainProject.listOfEnvironmentMolecules:
        tempnetlogoFile.write("\t set templist lput tempvalue" + j + " templist \n")
    tempnetlogoFile.write("\t report templist \n")
    tempnetlogoFile.write("end \n")
    lines = defaultnetlogoFile.readlines()
    for i in range(0, len(lines)):
        if i == 16:
            tempnetlogoFile.write(str(mainProject.lrCont) + "\n")
        elif i == 17:
            tempnetlogoFile.write(str(mainProject.tbCont) + "\n")
        elif i == 20:
            tempnetlogoFile.write(mainProject.maxXCor + "\n")
        elif i == 22:
            tempnetlogoFile.write(mainProject.maxYCor + "\n")
        else:
            tempnetlogoFile.write(lines[i])
    tempnetlogoFile.close()
    projectPath = os.path.abspath("./NetLogoModels/temporary.nlogo")
    return projectPath