#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 15:22:20 2022

@author: amymelhem
"""


## Assumes Z = 0.01 and that WD core mass is equal to total mass

## Mass range is different for buffer mass max and min, this assume they are the same


import numpy as np

x = 0 # 0 for first file, 1 for second

if x == 0:
    dataset = np.loadtxt("./SeBa_aa_020418_production_run_wdwd_bob.data")
else: 
    dataset = dataset = np.loadtxt("./SeBa_ag_020418_production_run_wdwd_bob.data")




## Removes enties that are not CO-CO WD binaries or fit Z = 0.01 conditions



xList = [] #Index of entries to be removed

for x in range(len(dataset)):
    
    #Removes entry if first star is not CO-WD
    if dataset[(x,5)] != 12:
        xList.append(x)        
        
    #Removes entry if second star is not CO-WD
    elif dataset[(x,6)] != 12:
        xList.append(x)


dataset = np.delete(dataset, xList, axis = 0)

datasetMin, datasetMax = dataset




xList = [] 
for x in range(len(datasetMin)):    
    #Removes entry if first or second WD is not in 0.52 - 0.93 mass range
    
    if datasetMin[(x,3)] < 0.52 or datasetMin[(x,3)] > 0.94:
        xList.append(x)
        
    elif datasetMin[(x,4)] < 0.52 or datasetMin[(x,3)] > 0.94:
        xList.append(x)

datasetMin = np.delete(datasetMin, xList, axis = 0)


xList = [] 
for x in range(len(datasetMax)):    
    #Removes entry if first or second WD is not in 0.52 - 0.93 mass range
    
    if datasetMax[(x,3)] < 0.52 or datasetMax[(x,3)] > 0.93:
        xList.append(x)
        
    elif datasetMax[(x,4)] < 0.52 or datasetMax[(x,3)] > 0.93:
        xList.append(x)


datasetMax = np.delete(datasetMax, xList, axis = 0)



#tie to IDs


M_buff_Min = []

for x in Range(len(dataset)):
    a = -3.3243
    b = -6.7603
    c = -3.0043
    
    M_buff_Min = ()
    




M_buff_Max










