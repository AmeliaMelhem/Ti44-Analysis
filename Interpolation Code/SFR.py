#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 21:20:56 2022

@author: Amelia Melhem
"""

# Estimating SFR of the Milky Way using equation 2 from Crocker et al

import matplotlib.pyplot as plt

def findSFR(z, a, b, c, d):
    first = a * (z**2) + b*z + c
    if first < 0:
        first = 0

    SFR = 10**first - d    
    return SFR

BuldgeMass = []
BuldgeZ = []
for i in range(2501):    
    BuldgeMass.append(findSFR(i/100, -0.0406, 0.331, 0.338, 0.771))
    BuldgeZ.append(i/100)
    
DiscMass = []
DiscZ = []
for i in range(2501):    
    DiscMass.append(findSFR(i/100, -0.0262, 0.384, -0.0842, 3.254))
    DiscZ.append(i/100)

plt.show()
plt.plot(BuldgeZ, BuldgeMass, "orange", label = "Buldge SFR")
plt.plot(DiscZ, DiscMass, "blue", label = "Disc SFR")
plt.legend()
plt.ylabel("Star Formation Rate (Solar Masses/year)")
plt.xlabel("Redshit")
plt.title("Milky Way SFR with Variable Redshift")

#plt.savefig("../Plots/" + "MilkyWay_SFR")

"""
Next steps:
SFR/Star densisty in terms of time? 
How did Crocker et al. find it?
"""