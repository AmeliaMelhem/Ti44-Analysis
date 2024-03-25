#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:43:20 2024

@authors: Amelia Melhem
"""

# Compares the Milky Way Ti44 production rates for varies levels of assumed metallicites. 
# It uses the assumed Z = 0.01 as a baseline since that was our original assumption, but
# only needs to demonstates how large of a difference the levels make.

import numpy as np
import matplotlib.pyplot as plt

dataset = np.loadtxt("Output Data/MW_Rates.csv", delimiter=',')

MW_0002_Rate = dataset[0]
MW_01_Rate   = dataset[1]
MW_02_Rate   = dataset[2]
N  = 15000

Relative_difference_0002 = (MW_0002_Rate-MW_01_Rate)/MW_01_Rate
Relative_difference_02   = (MW_02_Rate - MW_01_Rate)/MW_01_Rate
Relative_difference_01   = (MW_01_Rate - MW_01_Rate)/MW_01_Rate

high = [0,0]

#13871 is the zero-pt index
# plt.yscale("log")

# plt.plot(MW_01_Rate, label = '01')
# plt.plot(MW_02_Rate, label = '02')
# plt.plot(MW_0002_Rate, label = '0002')
plt.plot(Relative_difference_01[N:], 'k', label='Relative Difference Z = 0.01 (baseline)')
plt.plot(Relative_difference_0002[N:], label='Relative Difference Z = 0.0002')
plt.plot(Relative_difference_02[N:],   label='Relative Difference Z = 0.02')
plt.ylabel("Relative Difference")
plt.xlabel("\"Time\"")
plt.title("Percent difference of Ti44 production over time")
plt.legend()
plt.show()  



