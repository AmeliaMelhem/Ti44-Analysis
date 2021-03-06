#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Alexis Petty

Creates plots to compare to figure 9 in https://articles.adsabs.harvard.edu/pdf/2006MNRAS.371..263L to verify FindHeMass.py
is working correctly
"""


import matplotlib.pyplot as plt
import numpy as np



file = 1 # 0 for first file(aa), 1 for second(ag)

if file == 1:
    data = np.loadtxt("./noDashSeBa_aa_with_He.txt")    
    fileName = 'Mass_Comparison_aa'
else: 
    data = np.loadtxt("./noDashSeBa_ag_with_He.txt")
    fileName = 'Mass_Comparison_ag'



Mwd1=np.log10(data[:,3])
He_min_wd1=np.log10(data[:,7])
plt.plot(Mwd1, He_min_wd1,"ro")

He_max_wd1=np.log10(data[:,9])
plt.plot(Mwd1, He_max_wd1,"b*")

Mwd2=np.log10(data[:,4])
He_min_wd2=np.log10(data[:,8])
plt.plot(Mwd2, He_min_wd2,"ro")

He_max_wd2=np.log10(data[:,10])
plt.plot(Mwd2, He_max_wd2,"b*")



plt.title('WD-Mass VS He-Mass')
plt.legend(['W1min','W1max', 'W2min', 'W2max'])
plt.ylabel('He-Mass')
plt.xlabel('WD-Mass')

plt.savefig(fileName)

plt.show()