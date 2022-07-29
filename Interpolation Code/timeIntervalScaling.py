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



aaMasses = np.loadtxt("../Input Data/SeBa_aa_020418_production_run_wdwd_bob.data", usecols=3) + \
    np.loadtxt("../Input Data/SeBa_aa_020418_production_run_wdwd_bob.data", usecols=4)
agMasses = np.loadtxt("../Input Data/SeBa_ag_020418_production_run_wdwd_bob.data", usecols=3) + \
    np.loadtxt("../Input Data/SeBa_ag_020418_production_run_wdwd_bob.data", usecols=4)


# Can be made shorter, written out for clarity's sake
def samplePoints(dataset):
    allNumbers = []
    allSampleMedians = []
    allSampleMasses = []
    for x in range(100): 
        percent = 0.01*x + 0.01
        totalNumber = int( percent*len(dataset) )
        
        sample = np.random.permutation(dataset)
        sample = sample[0:totalNumber]        

        allNumbers.append(totalNumber)
        allSampleMedians.append( np.median( gf.findInterval( sample[:,0] ) ) )
        allSampleMasses.append( np.sum(sample[:,(1,2)] ) ) #adds both masses
        
        
    return allNumbers, allSampleMasses, allSampleMedians 


aaNumbers, aaMasses, aaMedian = samplePoints(aaDataset)
agNumbers, agMasses, agMedian = samplePoints(agDataset)



plt.plot(np.log(aaMasses), np.log(aaMedian), label = "aa Dataset Interval Medians")
plt.plot(np.log(agMasses), np.log(agMedian), label = "ag Dataset Interval Medians")
# plt.plot( xValues, oneOverX, label = "Test Fit")



plt.title("Random Sample Mass vs Interval Medians")
plt.xlabel("Random Sample Masses")
plt.ylabel("Random Sample Interval Medians")
plt.legend()
plt.show()


