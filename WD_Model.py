#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 15:22:20 2022

@author: amymelhem
"""


## Assumes Z = 0.01 and that WD core mass is equal to total mass

## Mass range is different for buffer mass max and min, *

import numpy as np

x = 0 # 0 for first file, 1 for second

if x == 0:
    dataset = np.loadtxt("./SeBa_aa_020418_production_run_wdwd_bob.data")
else: 
    dataset = dataset = np.loadtxt("./SeBa_ag_020418_production_run_wdwd_bob.data")




## Next 3 for loops remove entries that are not CO-CO WD binaries or fit Z = 0.01 conditions


xList = [] #Index of entries to be removed

for x in range(len(dataset)):
    
    #Removes entry if first star is not CO-WD
    if dataset[(x,5)] != 12:
        xList.append(x)        
        
    #Removes entry if second star is not CO-WD
    elif dataset[(x,6)] != 12:
        xList.append(x)


dataset = np.delete(dataset, xList, axis = 0)

datasetMin, datasetMax = dataset, dataset # initialize the two differing datasets


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



# Finds buffer mass min, stores in list MBuffMin with system ID

MBuffMin = np.zeros((1,3))
for x in range(len(datasetMin)):
    a = -3.3243
    b = -6.7603
    c = -3.0043
    
    Mass1 = datasetMin[(x,3)]
    Mass2 = datasetMin[(x,4)]
    
    
    MBuffMin1 = 10**(a + b*np.log10(Mass1) + c*(np.log10(Mass1)**2))
    MBuffMin2 = 10**(a + b*np.log10(Mass2) + c*(np.log10(Mass2)**2))
    
    MBuffMin = np.concatenate((MBuffMin, [[datasetMin[(x,0)], MBuffMin1, MBuffMin2]]))
    
MBuffMin = np.delete(MBuffMin, 0, axis = 0)




# Finds buffer mass max, stores in list MBuffMax with system ID

MBuffMax = np.zeros((1,3))

for x in range(len(datasetMax)):
    a = -2.9129
    b = -6.1056
    c = -5.0948
    
    Mass1 = datasetMax[(x,3)]
    Mass2 = datasetMax[(x,4)]
    
    MBuffMax1 = 10**(a + b*np.log10(Mass1) + c*(np.log10(Mass1)**2))
    MBuffMax2 = 10**(a + b*np.log10(Mass2) + c*(np.log10(Mass2)**2))
    
    MBuffMax = np.concatenate((MBuffMax, [[datasetMax[(x,0)], MBuffMax1, MBuffMax2]]))
    
MBuffMax = np.delete(MBuffMax, 0, axis = 0)







