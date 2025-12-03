__author__ = "Marius Kirchner, Goethe University Frankfurt am Main"

from xml.dom import minidom
from Backend.BackendStorage import Config
def openConfig(filepath):
    file = open(filepath, 'r', encoding='utf8')
    doc = minidom.parse(file)
    netlogoPath = doc.getElementsByTagName("NetLogoPath")[0].childNodes[0].data
    newConfig = Config.PetriAgentConfig(netlogoPath)
    print("test")
    return newConfig