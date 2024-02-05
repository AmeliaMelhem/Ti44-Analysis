#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 15:22:20 2022

@authors: Amelia Melhem

Altered form of FindHeMass.py to include a linear iterpolation to prevent
unphysical results at log(WDmass) ~ -0.3
"""

#TODO:
# fix sort order
# Done!


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

file = 0 # 1 for first file(aa), 0 for second(ag)
plotname = "HeLinMassComparison"

if file == 1:
    data = np.loadtxt("../Output Data/Extended Range WD He Mass/Full_SeBa_aa_with_He.txt")
    fileName = 'Full_SeBa_aa_with_He_Interp.txt'
    index = 1919
else:
    data = np.loadtxt("../Output Data/Extended Range WD He Mass/Full_SeBa_ag_with_He.txt")
    fileName = 'Full_SeBa_ag_with_He_Interp.txt'
    index = 3172

# Setting and sorting mass values
Mwd1=np.log10(data[:,3])
He_min_wd1=np.log10(data[:,7])
He_max_wd1=np.log10(data[:,9])


Mwd2=np.log10(data[:,4])
He_min_wd2=np.log10(data[:,8])
He_max_wd2=np.log10(data[:,10])

i1 = data[:,0]
i2 = i1

# sorted_pairs1 = sorted(zip(Mwd1, He_min_wd1, He_max_wd1, i1))
# sorted_pairs2 = sorted(zip(Mwd2, He_min_wd2, He_max_wd2, i2))

# Mwd1, He_min_wd1, He_max_wd1, i1 = [list(i) for i in zip(*sorted_pairs1)]
# Mwd2, He_min_wd2, He_max_wd2, i2 = [list(i) for i in zip(*sorted_pairs2)]

plt.plot(Mwd1, He_min_wd1,"k-", label="He Mass min")
plt.plot(Mwd1, He_max_wd1,"k--", label="He Mass max")
plt.plot(Mwd2, He_min_wd2,"k-")
plt.plot(Mwd2, He_max_wd2,"k--")


"""
Last two pts (wdMass, HeMass, i):
    aa:
        -0.31384475923938915 -1.4985162409270554 1919
        -0.31384297004234674 -1.4985299278995878 1920
    ag:
        -0.31384386463994657 -1.4985162409270554 3172
        -0.3138322350148824 -1.4985573031387727 3173
"""
        
# for i in range(len(Mwd1)):
#     if Mwd1[i] > -0.3138522091:
#         if Mwd1[i] < -0.3138:
#             print(Mwd1[i], He_min_wd1[i], i)

# if file == 1:
#     x1 = -0.31384475923938915
#     y1 = -1.4985162409270554
#     x2 = -0.31384297004234674
#     y2 = -1.4985299278995878
# else:
#     x1 = -0.31384386463994657
#     y1 = -1.4985162409270554
#     x2 = -0.3138322350148824
#     y2 = -1.4985573031387727


# m = (y2-y1)/(x2-x1)
# b = y1 - m*x1

# x1 = -0.31384386463994657
# y1 = -1.4985436153034843
# x2 = -0.3138322350148824
# y2 = -1.4985573031387727
# b = y1 - m*x1
# print(b)

m = -3.5308285082865614
bMin = -2.6066724797250362
bMax = -2.6066451053486075

#x = np.linspace(-0.5,-0.3138522091,100)
#y = [m*x[i]+bMin for i in range(len(x)) ]
#plt.plot(x,y,"b--")
#plt.plot(-0.31852,-1.498498, "bo")

for i in range(len(Mwd1)):
    if Mwd1[i] < -0.3138522091:
        He_max_wd1[i] = m*Mwd1[i]+bMax
        He_min_wd1[i] = m*Mwd1[i]+bMin
    if Mwd2[i] < -0.3138522091:
        He_max_wd2[i] = m*Mwd2[i]+bMax
        He_min_wd2[i] = m*Mwd2[i]+bMin



Mwd1Altered = []
He_min_wd1_Alterd = []
He_max_wd1_Alterd = []

for i in range(index):
    Mwd1Altered.append(Mwd1[i])
    He_min_wd1_Alterd.append(He_min_wd1[i])
    He_max_wd1_Alterd.append(He_max_wd1[i])


plt.plot(Mwd1Altered, He_max_wd1_Alterd,"r--")
plt.plot(Mwd1Altered, He_min_wd1_Alterd,"r-")


# store new interped data:
    
# sorted_pairs1 = sorted(zip(i1, Mwd1, He_min_wd1, He_max_wd1))
# sorted_pairs2 = sorted(zip(i2, Mwd2, He_min_wd2, He_max_wd2))
# i1, Mwd1, He_min_wd1, He_max_wd1 = [list(i) for i in zip(*sorted_pairs1)]
# i2, Mwd2, He_min_wd2, He_max_wd2 = [list(i) for i in zip(*sorted_pairs2)]


data[:,7] = [10**He_min_wd1[i] for i in range(len(data))]
data[:,9] = [10**He_max_wd1[i] for i in range(len(data))]

data[:,8] = [10**He_min_wd2[i] for i in range(len(data))]
data[:,10] = [10**He_max_wd2[i] for i in range(len(data))]


# check interp functions: it works!!

# for i in range(len(Mwd1)):
#     diff = He_max_wd1[i] - He_min_wd1[i]
#     if diff < 0:
#         print(diff)



# Save as new txt file. Change header to False to be numpy compatible or add
# '#' to the front of the first line of txt.

pdDataset = pd.DataFrame(data, columns = 
     ['id', 'DWD_formation_time(Myr)', 'time_of_merger(Myr)', 'Mwd1(Msun)', 
      'Mwd2(Msun)', 'type_wd1', 'type_wd2', 'He_min_wd1(Msun)',  'He_min_wd2(Msun)',
      'He_max_wd1(Msun) ', 'He_max_wd2(Msun)']
     )


with open('./' + fileName, 'w') as f:
    dfAsString = pdDataset.to_string(header=True, index=False)
    f.write(dfAsString)
