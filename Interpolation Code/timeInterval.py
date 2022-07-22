#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 18:43:02 2022

@author: amelia
"""

import numpy as np
import matplotlib.pyplot as plt

# pulls merger times and changes units to years, then sorts them
aaDataset = np.sort( (10**6) * np.loadtxt("../Input Data/SeBa_aa_020418_production_run_wdwd_bob.data", usecols=2) )
agDataset = np.sort( (10**6) * np.loadtxt("../Input Data/SeBa_ag_020418_production_run_wdwd_bob.data", usecols=2) )



def findInterval(dataset):
    intervals = []
    for x in range(len(dataset)-1):
        intervals.append( dataset[x+1]-dataset[x] ) 
    
    return intervals


aaIntervals = findInterval(aaDataset)
agIntervals = findInterval(agDataset)


plt.xlim(0,0.6e6)
plt.hist(aaIntervals, bins=1000)


# xSpace = np.linspace(0, np.max(agIntervals), len(agIntervals))
# plt.plot(xSpace, agIntervals)

plt.ylabel("Frequency")
plt.xlabel("Interval Length (years)")
plt.title("Interval Lengths Histogram (aa Dataset)")


plt.show()
#plt.savefig("../Output Data/" + "IntervalHisto_aa")