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
    data = np.loadtxt("../Output Data/Full_He_aa_with_Zenati.txt")    
    fileName = 'Combined_Mass_Comparison'
else: 
    data = np.loadtxt("../Output Data/Full_He_ag_with_Zenati.txt")
    fileName = 'Combined_Mass_Comparison'




colorList = ["g-","g--",
             "b-","b--",
             "k-","k--"]
labelList = ["He Mass min Z=0.0002" ,"He Mass max Z=0.0002",
             "He Mass min Z=0.01"   ,"He Mass max Z=0.01",
             "He Mass min Z=0.02"   ,"He Mass max Z=0.02"]


for i in range(3):
    Mwd2=np.log10(data[:,4])
    Mwd1=np.log10(data[:,3])
    He_min_wd1=np.log10(data[:,4*i+7])
    He_min_wd2=np.log10(data[:,4*i+8])
    He_max_wd1=np.log10(data[:,4*i+9])
    He_max_wd2=np.log10(data[:,4*i+10])

    sorted_pairs_1 = sorted(zip(Mwd1, He_min_wd1, He_max_wd1))
    Mwd1, He_min_wd1, He_max_wd1 = [list(i) for i in zip(*sorted_pairs_1)]
    sorted_pairs_2 = sorted(zip(Mwd2, He_min_wd2, He_max_wd2))
    Mwd2, He_min_wd2, He_max_wd2 = [list(i) for i in zip(*sorted_pairs_2)]


    plt.plot(Mwd1, He_min_wd1,colorList[2*i],   label=labelList[2*i])
    plt.plot(Mwd1, He_max_wd1,colorList[2*i+1], label=labelList[2*i+1])
    plt.plot(Mwd2, He_min_wd2,colorList[2*i])
    plt.plot(Mwd2, He_max_wd2,colorList[2*i+1])

plt.legend()
plt.ylabel('Log He Mass ($M_{\odot}$)')
plt.xlabel('Log WD Mass ($M_{\odot}$)')

#plt.savefig(fileName)

plt.show()