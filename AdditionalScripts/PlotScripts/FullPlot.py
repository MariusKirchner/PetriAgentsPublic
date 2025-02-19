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
print(listOfData[0][0])
minticks = len(listOfData[0][0])
print(minticks)
for x in range(0, numberOfSims):
    if len(listOfData[x][0]) < minticks:
        minticks = len(listOfData[x][0])
print(minticks)
for i in range(0, minticks):
    xaxis.append(i)
xnew = np.linspace(min(xaxis), max(xaxis), 300)
counter = 0
print(listOfData)
for x in range(0, len(listOfData[0])):
    maxplot = []
    minplot = []
    avgplot = []
    print(len(listOfData[0][x]))
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
    plt.plot(xnew, smoothavg, color="b")
    plt.fill_between(xnew, smoothmin, smoothmax, color="cornflowerblue")
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
    print(len(listOfData[0][x]))
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
        print(tempavg)
    tempsmoothavg = make_interp_spline(xaxis, avgplot, k=3)
    smoothavg = tempsmoothavg(xnew)
    tempsmoothmin = make_interp_spline(xaxis, minplot, k=3)
    smoothmin = tempsmoothmin(xnew)
    tempsmoothmax = make_interp_spline(xaxis, maxplot, k=3)
    smoothmax = tempsmoothmax(xnew)
    print("done interpolating")
    plt.plot(xnew, smoothavg, color="b")
    plt.fill_between(xnew, smoothmin, smoothmax, color="cornflowerblue")
    print(newfolderdir)
    plt.savefig(newfolderdir + "\\" + "StandardDeviation" + header[counter+1] + ".png", bbox_inches="tight")
    plt.savefig(newfolderdir + "\\" + "StandardDeviation" + header[counter + 1] + ".svg", bbox_inches="tight")
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


