import sys
import socket
import pandas as pd
import datetime as dt
import numpy as np
from math import pi
import csv

# Filedata
processfilepath = '/Users/kieran/develop/PythonTools/Face Tracking/out/'
processfilename = 'KIERAN_05-03-2020 17:03:19.txt'
fullfile = processfilepath + processfilename
savepath = '/Users/kieran/develop/PythonTools/Face Tracking/processed/'
savefilename = 'KIERAN_processed.csv'
fullsavepath = savepath + savefilename

print("Processing: " + processfilename)

# Read data file
row = []
rows = list()

col_headers = list()
vertex_headers = list()

for s in range(1220):
    x = "v"+str(s) + "_x"
    y = "v"+str(s) + "_y"
    z = "v"+str(s) + "_z"

    col_headers.append(x)
    col_headers.append(y)
    col_headers.append(z)

col_headers.append("TimeStamp")

# Read data file
with open(fullfile, mode='r') as face_data:
    print("Loading... " + processfilename)
    data = face_data.readline()
    data = data.split(">")
    index = 0
    print("Parising... " + processfilename)
    for mesh in data:
        mesh = mesh.replace(":",",")
        mesh = mesh.replace("~",",")
        mesh = mesh.replace("<","")
        mesh = mesh.replace("t,","")
        mesh = mesh.split(",")

        vindex = 0
        for v in mesh:
            if (len(row) <= 3661):
                row.append(v)
                if (len(row) != 3661 and len(mesh) == vindex):  
                    row = []    
                if (len(row) == 3661):
                    rows.append(row)
                    row = []
            vindex = vindex + 1

print("Creating df... " + processfilename)

# Add data to df
df = pd.DataFrame(rows,columns=col_headers)

df[col_headers] = df[col_headers].astype(float)

print("Coverting df to pickle... ")
# Save as pickle for post processing
df.to_pickle(fullsavepath + '.pickle')

print("Coverting df to csv... ")

# Write csv 
df.to_csv(fullsavepath)

print("COMPLETE!!!")