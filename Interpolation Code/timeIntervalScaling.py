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
aaDataset = np.loadtxt("../Input Data/SeBa_aa_020418_production_run_wdwd_bob.data", usecols=(2,3,4))
agDataset = np.loadtxt("../Input Data/SeBa_ag_020418_production_run_wdwd_bob.data", usecols=(2,3,4))

aaDataset[:,0] = (10**6) * aaDataset[:,0] # time unit from Myr to yr
agDataset[:,0] = (10**6) * agDataset[:,0] # time unit from Myr to yr


# Takes numSamples number of samples for the given dataset, and creates 3 lists
# First is number of mergers in each sample, second is the total sample mass,
# third is the median interval lengths in each sample
def samplePoints(dataset, numSamples):
    allNumbers = []
    allSampleMedians = []
    allSampleMasses = []
    for x in range(numSamples): 
        totalNumber = int( (x+1)/numSamples*len(dataset) )
        
        sample = np.random.permutation(dataset)
        sample = sample[0:totalNumber]        

        allNumbers.append(totalNumber)
        allSampleMedians.append( np.median( gf.findInterval( sample[:,0] ) ) )
        allSampleMasses.append( np.sum(sample[:,(1,2)] ) ) #adds both masses
        
        
    return allNumbers, allSampleMasses, allSampleMedians 


aaNumbers, aaMasses, aaMedian = samplePoints(aaDataset, 100)
agNumbers, agMasses, agMedian = samplePoints(agDataset, 100)

# x = number of mergers
plt.plot(np.log(aaNumbers), np.log(aaMedian), label = "aa Dataset Interval Medians")
plt.plot(np.log(agNumbers), np.log(agMedian), label = "ag Dataset Interval Medians")
plt.title("Logged Random Sample Merger Number vs Interval Medians")
plt.xlabel("Logged Random Sample Merger Number")


# x = total system mass
# plt.plot(np.log(aaMasses), np.log(aaMedian), label = "aa Dataset Interval Medians")
# plt.plot(np.log(agMasses), np.log(agMedian), label = "ag Dataset Interval Medians")
# plt.title("Logged Random Sample Mass vs Interval Medians")
# plt.xlabel("Logged Random Sample Masses")



plt.ylabel("Logged Random Sample Interval Medians")
plt.legend()
plt.show()


