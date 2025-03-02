import math
import os
import sys

import matplotlib.pyplot as plt
import matplotlib
import csv
from scipy.interpolate import make_interp_spline
import numpy as np
import tkinter.filedialog
#todo: continue writing this, make it viable for any start setup (multiple bacteria in same graph)
#todo: add legends
#todo: add explanation to parameters

matplotlib.use("TkAgg")
directory = tkinter.filedialog.askdirectory()
listOfData = []
xaxis = []
numberOfSims = 0
tabledir = os.path.join(directory, 'tables')
for filename in os.listdir(tabledir):
    filepath = os.path.join(tabledir, filename)
    if os.path.isfile(filepath):
        templist = []
        csvfile = open(filepath, newline="")
        inputfile = csv.reader(csvfile, delimiter=",")
        style = next(inputfile)
        header = next(inputfile)
        for i in range(1, len(header)):
            templist.append([])
        for row in inputfile:
            for i in range(1, len(header)):
                templist[i - 1].append(int(row[i]))
        numberOfSims += 1
        listOfData.append(templist)

newfolderdir = os.path.join(directory, r'plots')
if not os.path.isdir(newfolderdir):
    os.makedirs(newfolderdir)
#print(listOfData[0][0])
minticks = len(listOfData[0][0])
#print(minticks)
for x in range(0, numberOfSims):
    if len(listOfData[x][0]) < minticks:
        minticks = len(listOfData[x][0])
print(minticks)
for i in range(0, minticks):
    xaxis.append(i)
xnew = np.linspace(min(xaxis), max(xaxis), 300)
'''counter = 0
#print(listOfData)
for x in range(0, len(listOfData[0])):
    maxplot = []
    minplot = []
    avgplot = []
    #print(len(listOfData[0][x]))
    for currx in range(0, minticks):
        tempmin = sys.float_info.max
        tempmax = 0
        tempcounter = 0
        avgsum = 0
        for currsim in range(0, numberOfSims):
            if listOfData[currsim][x][currx] < tempmin:
                tempmin = listOfData[currsim][x][currx]
            if listOfData[currsim][x][currx] > tempmax:
                tempmax = listOfData[currsim][x][currx]
            avgsum += listOfData[currsim][x][currx]
            tempcounter += 1
        tempavg = avgsum / tempcounter
        maxplot.append(tempmax)
        minplot.append(tempmin)
        avgplot.append(tempavg)
        #print(tempmin)
        #print(tempmax)
        #print(tempavg)
    tempsmoothavg = make_interp_spline(xaxis, avgplot, k=3)
    smoothavg = tempsmoothavg(xnew)
    tempsmoothmin = make_interp_spline(xaxis, minplot, k=3)
    smoothmin = tempsmoothmin(xnew)
    tempsmoothmax = make_interp_spline(xaxis, maxplot, k=3)
    smoothmax = tempsmoothmax(xnew)
    print("done interpolating")
    plt.plot(xnew, smoothavg, color="b")
    plt.fill_between(xnew, smoothmin, smoothmax, color="cornflowerblue")
    plt.ylim(bottom=0)
    print(newfolderdir)
    plt.savefig(newfolderdir + "\\" + "Total" + header[counter+1] + ".png", bbox_inches="tight")
    plt.savefig(newfolderdir + "\\" + "Total" + header[counter + 1] + ".svg", bbox_inches="tight")
    print("done")
    counter += 1
    plt.clf()
counter = 0
for x in range(0, len(listOfData[0])):
    maxplot = []
    minplot = []
    avgplot = []
    #print(len(listOfData[0][x]))
    for currx in range(0, minticks):
        tempcounter = 0
        avgsum = 0
        for currsim in range(0, numberOfSims):
            avgsum += listOfData[currsim][x][currx]
            tempcounter += 1
        tempavg = avgsum / tempcounter
        totaldev = 0
        for currsim in range(0, numberOfSims):
            totaldev += (listOfData[currsim][x][currx] - tempavg)**2
        variance = totaldev / tempcounter
        standarddev = math.sqrt(variance)
        maxplot.append(tempavg+standarddev)
        minplot.append(tempavg-standarddev)
        avgplot.append(tempavg)
        #print(tempavg)
    tempsmoothavg = make_interp_spline(xaxis, avgplot, k=3)
    smoothavg = tempsmoothavg(xnew)
    tempsmoothmin = make_interp_spline(xaxis, minplot, k=3)
    smoothmin = tempsmoothmin(xnew)
    tempsmoothmax = make_interp_spline(xaxis, maxplot, k=3)
    smoothmax = tempsmoothmax(xnew)
    print("done interpolating")
    plt.plot(xnew, smoothavg, color="b")
    plt.fill_between(xnew, smoothmin, smoothmax, color="cornflowerblue")
    plt.ylim(bottom=0)
    print(newfolderdir)
    plt.savefig(newfolderdir + "\\" + "StandardDeviation" + header[counter+1] + ".png", bbox_inches="tight")
    plt.savefig(newfolderdir + "\\" + "StandardDeviation" + header[counter + 1] + ".svg", bbox_inches="tight")
    print("done")
    counter += 1
    plt.clf()'''
counter = 0
for x in range(0, len(listOfData[0])):
    maxplot = []
    minplot = []
    avgplot = []
    #print(len(listOfData[0][x]))
    for currx in range(0, minticks):
        tempcounter = 0
        avgsum = 0
        for currsim in range(0, numberOfSims):
            avgsum += listOfData[currsim][x][currx]
            tempcounter += 1
        tempavg = avgsum / tempcounter
        totaldev = 0
        for currsim in range(0, numberOfSims):
            totaldev += (listOfData[currsim][x][currx] - tempavg)**2
        variance = totaldev / tempcounter
        standarddev = math.sqrt(variance)
        maxplot.append(tempavg+(0.95*(standarddev/math.sqrt(numberOfSims))))
        minplot.append(tempavg-(0.95*(standarddev/math.sqrt(numberOfSims))))
        avgplot.append(tempavg)
        #print(tempavg)
    tempsmoothavg = make_interp_spline(xaxis, avgplot, k=3)
    smoothavg = tempsmoothavg(xnew)
    tempsmoothmin = make_interp_spline(xaxis, minplot, k=3)
    smoothmin = tempsmoothmin(xnew)
    tempsmoothmax = make_interp_spline(xaxis, maxplot, k=3)
    smoothmax = tempsmoothmax(xnew)
    print("done interpolating")
    plt.plot(xnew, smoothavg, color="b")
    plt.fill_between(xnew, smoothmin, smoothmax, color="cornflowerblue")
    plt.ylim(bottom=0)
    print(newfolderdir)
    plt.savefig(newfolderdir + "\\" + "ConInt" + header[counter+1] + ".png", bbox_inches="tight")
    plt.savefig(newfolderdir + "\\" + "ConInt" + header[counter + 1] + ".svg", bbox_inches="tight")
    print("done")
    counter += 1
    plt.clf()
combinedPlots = [1, 5]
for x in combinedPlots:
    maxplot = []
    minplot = []
    avgplot = []
    #print(len(listOfData[0][x]))
    for currx in range(0, minticks):
        tempcounter = 0
        avgsum = 0
        for currsim in range(0, numberOfSims):
            avgsum += listOfData[currsim][x][currx]
            tempcounter += 1
        tempavg = avgsum / tempcounter
        totaldev = 0
        for currsim in range(0, numberOfSims):
            totaldev += (listOfData[currsim][x][currx] - tempavg)**2
        variance = totaldev / tempcounter
        #print("Variance")
        #print(variance)
        standarddev = math.sqrt(variance)
        maxplot.append(tempavg+(0.95*(standarddev/math.sqrt(numberOfSims))))
        minplot.append(tempavg-(0.95*(standarddev/math.sqrt(numberOfSims))))
        avgplot.append(tempavg)
        #print(tempavg)
    tempsmoothavg = make_interp_spline(xaxis, avgplot, k=3)
    smoothavg = tempsmoothavg(xnew)
    tempsmoothmin = make_interp_spline(xaxis, minplot, k=3)
    smoothmin = tempsmoothmin(xnew)
    tempsmoothmax = make_interp_spline(xaxis, maxplot, k=3)
    smoothmax = tempsmoothmax(xnew)
    print("done interpolating")
    if x == 1:
        plt.plot(xnew, smoothavg, color="b")
        plt.fill_between(xnew, smoothmin, smoothmax, facecolor="cornflowerblue", alpha=0.7)
    else:
        plt.plot(xnew, smoothavg, color="r")
        plt.fill_between(xnew, smoothmin, smoothmax, facecolor="indianred", alpha=0.7)
        print(newfolderdir)
        plt.xlabel("Simulation time (ticks)")
        plt.ylabel("Number of bacteria")
        plt.savefig(newfolderdir + "\\" + "Combine.png", bbox_inches="tight")
        plt.savefig(newfolderdir + "\\" + "Combine.svg", bbox_inches="tight")
        # plt.ylim(bottom=20, top=200)
        plt.ylim(bottom=32, top=38)
        plt.savefig(newfolderdir + "\\" + "CombineLimit.png", bbox_inches="tight")
        plt.savefig(newfolderdir + "\\" + "CombineLimit.svg", bbox_inches="tight")
        print("done")
    #plt.clf()
plt.clf()


