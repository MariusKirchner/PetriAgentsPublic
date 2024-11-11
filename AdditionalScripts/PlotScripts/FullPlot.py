import matplotlib.pyplot as plt
import matplotlib
import csv
from scipy.interpolate import make_interp_spline
import numpy as np


#todo: continue writing this, make it viable for any start setup (multiple bacteria in same graph)
#todo: add legends
#todo: add explanation to parameters

matplotlib.use("TkAgg")
csvfile = open("C:\\Users\\mariu\\PycharmProjects\\PetriAgentsPublic\\results.csv", newline="")
inputfile = csv.reader(csvfile, delimiter=",")
xaxis= []
plots = []
style = next(inputfile)
header = next(inputfile)
print(header)
numberofPlots = len(header) - 1
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
    plt.clf()


