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
newxaxis = True
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):
        templist = []
        csvfile = open(filepath, newline="")
        inputfile = csv.reader(csvfile, delimiter=",")
        style = next(inputfile)
        header = next(inputfile)
        for i in range(1, len(header)):
            templist.append([])
        for row in inputfile:
            if newxaxis:
                xaxis.append(int(row[0]))
            for i in range(1, len(header)):
                templist[i - 1].append(int(row[i]))
        newxaxis = False
        numberOfSims += 1
        listOfData.append(templist)


xnew = np.linspace(min(xaxis), max(xaxis), 300)
counter = 0
print(listOfData)
for x in range(0, len(listOfData[0])):
    maxplot = []
    minplot = []
    avgplot = []
    print(len(listOfData[0][x]))
    for currx in range(0, len(listOfData[0][x])):
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
        print(tempmin)
        print(tempmax)
        print(tempavg)
    tempsmoothavg = make_interp_spline(xaxis, avgplot, k=3)
    smoothavg = tempsmoothavg(xnew)
    tempsmoothmin = make_interp_spline(xaxis, minplot, k=3)
    smoothmin = tempsmoothmin(xnew)
    tempsmoothmax = make_interp_spline(xaxis, maxplot, k=3)
    smoothmax = tempsmoothmax(xnew)
    print("done interpolating")
    plt.plot(xnew, smoothavg)
    plt.fill_between(xnew, smoothmin, smoothmax)
    plt.savefig(header[counter+1] + ".png", bbox_inches="tight")
    print("done")
    counter += 1
    plt.clf()
#csvfile = open("C:\\Users\\mariu\\PycharmProjects\\PetriAgentsPublic\\results.csv", newline="")
'''csvfile = open("C:\\Users\\Marius MainPC\\Desktop\\ToBeSorted\\PetriAgentsPublic\\results.csv", newline="")
inputfile = csv.reader(csvfile, delimiter=",")
xaxis = []
plots = []
style = next(inputfile)
header = next(inputfile)
print(header)
numberofPlots = len(header)
for i in range(1, numberofPlots):
    plots.append([])
for row in inputfile:
    xaxis.append(int(row[0]))
    for i in range(1, numberofPlots):
        plots[i-1].append(int(row[i]))
xnew = np.linspace(min(xaxis), max(xaxis), 300)
counter = 0
for x in plots:
    tempsmooth = make_interp_spline(xaxis, x, k=3)
    smooth = tempsmooth(xnew)
    print("done interpolating")
    plt.plot(xnew, smooth)
    plt.savefig(header[counter+1] + ".png", bbox_inches="tight")
    print("done")
    counter += 1
    plt.clf()'''


