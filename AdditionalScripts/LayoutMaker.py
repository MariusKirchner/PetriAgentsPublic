import tkinter.filedialog

filetypes = (("sbml files", "*.xml"), ("All files", "*.*"))
filename = tkinter.filedialog.askopenfilename(title="Open a SBML File", filetypes=filetypes)
file1 = open(filename, "r")
file2 = open("newfile.xml", "w")
lines = file1.readlines()
i = 0
for line in lines:
    if "layout:position" in line:
        file2.write("\t \t <layout:position layout:x=\""+str(i * 5)+"\" layout:y=\""+str(i * 5)+"\" layout:z=\"0\" >\n")
        i += 1
    else:
        file2.write(line)
file2.close()

