#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 15:22:20 2022

@author: amymelhem
"""

import numpy as np

x = 0 # 0 for first file, 1 for second

if x == 0:
    dataset = np.loadtxt("./SeBa_aa_020418_production_run_wdwd_bob.data")
else: 
    dataset = dataset = np.loadtxt("./SeBa_ag_020418_production_run_wdwd_bob.data")




xList = []

for x in range(len(dataset)):
    
    #Removes entry if first star is not CO-WD
    if dataset[(x,5)] != 12:
        xList.append(x)        
        
    #Removes entry if second star is not CO-Wd
    elif dataset[(x,6)] != 12:
        xList.append(x)
    

dataset = np.delete(dataset, xList, axis = 0)
print(len(dataset))











