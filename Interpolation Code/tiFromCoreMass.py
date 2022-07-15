#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 00:56:16 2022

@author: amelia
"""

from groupFunctions import steppedLinearInterp
import numpy as np
import matplotlib.pyplot as plt

## Input Data

LeungData = np.loadtxt('../Input Data/Ti_He_Leung_T13.txt', skiprows = 1, usecols=(1, 2, 3, 4, 5, 6, 7)) 
GronowData = np.loadtxt('../Input Data/Ti_He_Gronow.txt', usecols=(2, 5))

# Reformats data
GronowData[:,[1,0]] = GronowData[:,[0,1]] # Swaps coloumns
GronowData = GronowData.T

inputData = np.concatenate((GronowData, LeungData), axis = 1)

# WD Mass Data
Mass1aa = np.loadtxt('../Input Data/SeBa_aa_020418_production_run_wdwd_bob.data', usecols=(3), skiprows=(122000))
Mass2aa = np.loadtxt('../Input Data/SeBa_aa_020418_production_run_wdwd_bob.data', usecols=(4))
Mass1ag = np.loadtxt('../Input Data/SeBa_ag_020418_production_run_wdwd_bob.data', usecols=(3))
Mass2ag = np.loadtxt('../Input Data/SeBa_ag_020418_production_run_wdwd_bob.data', usecols=(4))

# Estimated Ti44 Mass
TiMass1aa = steppedLinearInterp(inputData, Mass1aa)
TiMass2aa = steppedLinearInterp(inputData, Mass2aa)
TiMass1ag = steppedLinearInterp(inputData, Mass1ag)
TiMass2ag = steppedLinearInterp(inputData, Mass2ag)


x = np.linspace(np.amin(Mass1aa), np.amax(Mass1aa), len(TiMass1aa))
y = TiMass1aa

plt.plot(x, y, 'b')
# plt.plot(inputData[0,:], inputData[1,:], "r+")
# plt.plot(GronowData[0,:], GronowData[1,:], "b+")
# plt.plot(LeungData[0,:], LeungData[1,:], "g+")


plt.show()