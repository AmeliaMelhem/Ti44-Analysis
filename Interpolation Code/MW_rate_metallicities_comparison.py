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
import pandas as pd
import matplotlib.pyplot as plt

rate_data = np.loadtxt("Output Data/MW_Rates.csv", delimiter=',')

time_data = pd.read_csv("Output Data/Full_He_ag_with_Zenati.txt", sep='\s+', index_col=False) 
time_data = time_data.shift(periods=1, axis=1) 
time_data = time_data.sort_values(by='time_of_merger(Myr)') 
times = np.array(time_data.loc[:,'time_of_merger(Myr)'])

MW_0002_Rate = rate_data[0]
MW_01_Rate   = rate_data[1]
MW_02_Rate   = rate_data[2]
N = 15000
M = 3000

Relative_difference_0002 = (MW_0002_Rate-MW_01_Rate)/MW_01_Rate
Relative_difference_02   = (MW_02_Rate - MW_01_Rate)/MW_01_Rate
Relative_difference_01   = (MW_01_Rate - MW_01_Rate)/MW_01_Rate


#13871 is the zero-pt index


plt.rc('axes', labelsize=18)

# Relative Differences
# plt.figure(figsize=(12,   6))
# plt.subplot(1, 2, 1)

plt.plot(times, Relative_difference_0002,    label='Relative Difference Z = 0.0002')
plt.plot(times, Relative_difference_01, 'k', label='Relative Difference Z = 0.01 (baseline)')
plt.plot(times, Relative_difference_02,      label='Relative Difference Z = 0.02')

plt.ylabel("Relative Difference")
plt.xlabel("Time (Myr)")
plt.legend()
# plt.title("Percent difference of $^{44}$Ti production over time")

# plt.savefig("./Plots/Metallicity/Fulla.png")

plt.xlim(364,368)
plt.savefig("./Plots/Metallicity/ZoomIna.png")


# plt.xlim(1000,3000)
# plt.ylim(-0.002,0.002)
# plt.savefig("./Plots/Metallicity/Typical.png")

#==============================================================================================#

# Ti44 Rates

# plt.subplot(1, 2, 2)

plt.clf()
plt.yscale("log")
plt.plot(times, MW_0002_Rate,    label = 'Z = 0.0002')
plt.plot(times, MW_01_Rate, 'k', label = 'Z = 0.01')
plt.plot(times, MW_02_Rate,      label = 'Z = 0.02')

plt.ylabel("Specific $^{44}$Ti Rate")
plt.xlabel("Time (Myr)")
# plt.title("$^{44}$Ti production vs time")
plt.legend()
# plt.show()  


plt.xlim(366,366.4)
plt.ylim(4*10**-8, 9*10**-8)
plt.tight_layout(h_pad=1)
plt.savefig("./Plots/Metallicity/ZoomInb.png")


# plt.xlim(0,M)
# # plt.tight_layout(h_pad=2)
# plt.savefig("./Plots/Metallicity/Fullb.png")

