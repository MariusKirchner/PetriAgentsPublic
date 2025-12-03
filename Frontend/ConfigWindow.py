__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

import os
import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from Backend.BackendStorage import Config
from Backend.Input import OpenConfig
from xml.dom import minidom
def configWindow(config):
    configRoot = Tk()
    configRoot.title("Config MainWindow")
    #ttk.Label(master=configRoot, text="Current NetLogoPath: ").grid(row=0, column=0)
    #netLogoPathVar = StringVar(value=projectHolder.config.netLogoPath, master=configRoot)
    #ttk.Label(master=configRoot, textvariable=netLogoPathVar).grid(row=0, column=1)
    #ttk.Button(master=configRoot, text="Load new config file: ", command=lambda: configFilePicker()).grid(row=1, column=0)
    ttk.Label(master=configRoot, text="No config.xml detected, please choose a directory for your NetLogo installation.").grid(row=0, column=0)
    ttk.Button(master=configRoot, text="Choose new NetLogoPath: ", command=lambda: netLogoPathPicker()).grid(row=2, column=0)
    #ttk.Button(master=configRoot, text="Save these config settings: ", command=lambda: saveConfig(os.getcwd() + "/config.xml")).grid(row=3, column=0)

    def configFilePicker():
        filepath = tkinter.filedialog.askopenfilename(title="Loading config from...", filetypes=(("Config", ".xml"), ("All files", "*.*")))
        config = OpenConfig.openConfig(filepath)

    def netLogoPathPicker():
        filepath = tkinter.filedialog.askdirectory(title="NetLogo Path...")
        config.netLogoPath = filepath
        print(config.netLogoPath)
        doc = minidom.Document()
        doc.appendChild(doc.createComment(
            "PetriAgent Config created with PetriAgents Version 0.9.0, Release Date: 3rd of December 2025"))
        configEl = doc.createElement("Config")
        doc.appendChild(configEl)
        netlogopathEl = doc.createElement("NetLogoPath")
        configEl.appendChild(netlogopathEl)
        netlogopathEl.appendChild(doc.createTextNode(config.netLogoPath))
        doc = doc.toprettyxml()
        file = open(os.getcwd() + "/config.xml", mode="w")
        file.write(doc)
        file.close()
        print("Saving Config")
        configRoot.destroy()

    def saveConfig(filepath):
        doc = minidom.Document()
        doc.appendChild(doc.createComment("PetriAgent Config created with PetriAgents Version 0.9.0, Release Date: 3rd of December 2025"))
        configEl = doc.createElement("Config")
        doc.appendChild(configEl)
        netlogopath = doc.createElement("NetLogoPath")
        configEl.appendChild(netlogopath)
        netlogopath.appendChild(doc.createTextNode(config.netLogoPath))
        doc = doc.toprettyxml()
        file = open(filepath, mode="w")
        file.write(doc)
        file.close()
        print("Saving Config")
        configRoot.destroy()

    configRoot.mainloop()