#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 00:12:10 2022

@author: amelia
"""

import numpy as np
import matplotlib.pyplot as plt
import groupFunctions as gf


# pulls merger times and changes units to years, then sorts them
aaDataset = (10**6) * np.loadtxt("../Input Data/SeBa_aa_020418_production_run_wdwd_bob.data", usecols=2) 
agDataset = (10**6) * np.loadtxt("../Input Data/SeBa_ag_020418_production_run_wdwd_bob.data", usecols=2)



percent = 0.5


totalNumber = int( percent*len(aaDataset) )
aaSample = np.random.choice(aaDataset, totalNumber)

totalNumber = int( percent*len(agDataset) )
agSample = np.random.choice(agDataset, totalNumber)


aaIntervals = gf.findInterval(aaSample)
agIntervals = gf.findInterval(agSample)


# Can be made shorter, written out for clarity's sake
def samplePoints(dataset):
    allNumbers = []
    allSampleMedians = []
    for x in range(100): 
        percent = 0.01*x + 0.01
        
        totalNumber = int( percent*len(dataset) )
        sample = np.random.choice(dataset, totalNumber)
        
        allNumbers.append(totalNumber)
        
        allSampleMedians.append(np.median(gf.findInterval(sample)))
        
        
        
    return allNumbers, allSampleMedians

aaNumbers, aaSample = samplePoints(aaDataset)
agNumbers, agSample = samplePoints(agDataset)



plt.plot(aaNumbers, aaSample, label = "aa Dataset Medians")
plt.plot(agNumbers, agSample, label = "ag Dataset Medians")
plt.plot( xValues, oneOverX, label = "Test Fit")



plt.title("Random Sampling Medians")
plt.xlabel("Number of Points Sampled")
plt.ylabel("Median of the Random Sample")
plt.legend()
plt.show()


