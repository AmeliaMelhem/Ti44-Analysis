#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Alexis Petty & Amelia Melhem

Creates plots to compare to figure 9 in 
https://articles.adsabs.harvard.edu/pdf/2006MNRAS.371..263L 
to verify FindHeMass.py is working correctly
"""


import matplotlib.pyplot as plt
import numpy as np


file = 0 # 0 for first file(aa), 1 for second(ag)

if file == 0:
    data = np.loadtxt("../Output Data/Extended Range WD He Mass/Full_He_aa_with_Zenati.txt")    
    fileName = 'Combined_Mass_Comparison'
else: 
    data = np.loadtxt("../Output Data/Extended Range WD He Mass/Full_He_ag_with_Zenati.txt")
    fileName = 'Combined_Mass_Comparison'



Mwd1=np.log10(data[:,3])
He_min_wd1=np.log10(data[:,7])
He_max_wd1=np.log10(data[:,9])

sorted_pairs = sorted(zip(Mwd1, He_min_wd1, He_max_wd1))
Mwd1, He_min_wd1, He_max_wd1 = [list(i) for i in zip(*sorted_pairs)]

plt.plot(Mwd1, He_min_wd1,"k-", label="He Mass min")
plt.plot(Mwd1, He_max_wd1,"k--", label="He Mass max")


Mwd2=np.log10(data[:,4])
He_min_wd2=np.log10(data[:,8])
He_max_wd2=np.log10(data[:,10])

sorted_pairs = sorted(zip(Mwd2, He_min_wd2, He_max_wd2))
Mwd2, He_min_wd2, He_max_wd2 = [list(i) for i in zip(*sorted_pairs)]

plt.plot(Mwd2, He_min_wd2,"k-")
plt.plot(Mwd2, He_max_wd2,"k--")
#plt.plot(-0.31852,-1.498498, "bo")


plt.legend()
plt.ylabel('Log He Mass ($M_{\odot}$)')
plt.xlabel('Log WD Mass ($M_{\odot}$)')

#plt.savefig(fileName)

plt.show()