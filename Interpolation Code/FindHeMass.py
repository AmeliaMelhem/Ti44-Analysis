#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 15:22:20 2022

@authors: Amelia Melhem and Alexis Petty
"""

### Finds estimated He mass in WD given total mass using
### https://articles.adsabs.harvard.edu/pdf/2006MNRAS.371..263L and
### https://academic.oup.com/mnras/article/482/1/1135/5124388 (table 1)

## Assumes Z = 0.01 and that WD core mass is equal to total mass
## Also assumes that the buffer mass of the He is equal to the total He mass

## 2/9: MBuff function altered to remove mass limits on WD -AM

## 2/4/24: Looked at change in He buffer mass for varying metalicty assumptions -AM

import numpy as np
import pandas as pd

file = 1 # 0 for first file(aa), 1 for second(ag)

if file == 0:
    dataset = np.loadtxt("../Input Data/SeBa_aa_020418_production_run_wdwd_bob.data")
    fileName = '../Output Data/Full_He_aa_with_Zenati.txt'
else: 
    dataset = np.loadtxt("../Input Data/SeBa_ag_020418_production_run_wdwd_bob.data")
    fileName = '../Output Data/Full_He_ag_with_Zenati.txt'



## Removes entries that are not CO-CO WD binaries

xList = [] #Index of entries to be removed

for x in range(len(dataset)):
    
    #Removes entry if first star is not CO-WD
    if dataset[(x,5)] != 12:
        xList.append(x)        
        
    #Removes entry if second star is not CO-WD
    elif dataset[(x,6)] != 12:
        xList.append(x)


dataset = np.delete(dataset, xList, axis = 0)




## Conversion to Pandas DataFrames, done to allow '-' to be inputed where a system has a min buffer mass but no max buffer mass

pdDataset = pd.DataFrame(dataset, columns = ['id', 'DWD_formation_time(Myr)', 
                                             'time_of_merger(Myr)', 'Mwd1(Msun)', 
                                             'Mwd2(Msun)', 'type_wd1', 'type_wd2' ], 
                                             dtype=np.single)

# Initalize new columns for calculated data
pdDataset['He_min_wd1(Msun)_0002'] = 0.
pdDataset['He_min_wd2(Msun)_0002'] = 0.
pdDataset['He_max_wd1(Msun)_0002'] = 0.
pdDataset['He_max_wd2(Msun)_0002'] = 0.

pdDataset['He_min_wd1(Msun)_01'] = 0.
pdDataset['He_min_wd2(Msun)_01'] = 0.
pdDataset['He_max_wd1(Msun)_01'] = 0.
pdDataset['He_max_wd2(Msun)_01'] = 0.

pdDataset['He_min_wd1(Msun)_02'] = 0.
pdDataset['He_min_wd2(Msun)_02'] = 0.
pdDataset['He_max_wd1(Msun)_02'] = 0.
pdDataset['He_max_wd2(Msun)_02'] = 0.

## Function to find the buffer mass given WD mass and variables from Table 6
## Mass assumed to be given in solar masses


def MBuff(mass, LM_T6_vars):
    """
    First uses Zenati et al. to estimate He buffer mass given WD mass. 
    If out of range, then uses equation 9 and table 6 from Lawlor and MacDonald (2006)
    
    Parameters
    ----------
    mass : Core Mass of the WD
    a, b, c : Given by table 6
    d, e : Min and Max allowed input WD masses. returns '-' if the input is 
    outside this range

    Returns
    -------
    MBuff : The estimated He Mass

    """
    
    if mass < 0.52 and mass > 0.4: # Figure 1 Zenati et al
       MBuff =  0.28 - 0.39*mass

    elif mass < 0.4 and mass > 0.3: #second check is somewhat irrelevent as mass is never below 0.3
        MBuff = mass - 0.3    
    
    else:
        MBuff = 10**(LM_T6_vars[0] + LM_T6_vars[1]*np.log10(mass) + LM_T6_vars[2]*(np.log10(mass)**2)) # Equation 9 Lawlor and MacDonald

    return MBuff


## Uses MBuff to assign buffer mass values in pdDataset 

def assignMass(df): 

    # Z = 0.0002    
    z0_0002_min =   [-3.4083, -8.0814, -7.4303,  0.58, 1.22]
    z0_0002_max =   [-2.9816, -8.0142, -10.9891, 0.57, 1.23]

    # Z = 0.01    
    z0_01_min =     [-3.3243, -6.7603, -3.0043,  0.52, 0.94]
    z0_01_max =     [-2.9129, -6.1056, -5.0948,  0.52, 0.93]

    # Z = 0.02    
    z0_02_min =     [-3.3106, -7.1480, -4.4195,  0.51, 0.97]
    z0_02_max =     [-3.0248, -7.5528, -10.5975, 0.57, 0.97]


    # All Table 6 variables, to be easily iterable
    zList = [z0_0002_min, z0_0002_max, 
             z0_01_min  , z0_01_max, 
             z0_02_min  , z0_02_max]
    
    for row in range(len(df)):
        for i in range(3):

            ## MBuff min 
            mass = df.iat[row, 3] #WD 1
            df.iat[row, 4*i+7] = MBuff(mass, zList[i*2])
        
            mass = df.iat[row, 4] #WD 2
            df.iat[row, 4*i+8] = MBuff(mass, zList[i*2])
        
            ## MBuff max     
            mass = df.iat[row, 3] #WD 1
            df.iat[row, 4*i+9] = MBuff(mass, zList[i*2+1])
        
            mass = df.iat[row, 4] #WD 2
            df.iat[row, 4*i+10] = MBuff(mass, zList[i*2+1])

    return df


## Remove entries that have no He mass attributed

def removeNull(df): # Could be generalized if useful but probably not -AM
    xList = []
    for row in range(len(df)):
        for i in range(3):
            if (df.iat[row, 4*i+7] == '-' and # change all 'and' to 'or' to only
                df.iat[row, 4*i+8] == '-' and # store information when all 4 buffer
                df.iat[row, 4*i+9] == '-' and # masses can be found
                df.iat[row, 4*i+10] == '-'):
                    xList.append(x)
                
    df = df.drop(xList)
    
    return df

pdDataset = assignMass(pdDataset)
pdDataset = removeNull(pdDataset)

# Save as new txt file. Change header to False to be numpy compatible or add
# '#' to the front of the first line of txt.

with open(fileName, 'w') as f:
    dfAsString = pdDataset.to_string(header=True, index=False)
    f.write(dfAsString)
