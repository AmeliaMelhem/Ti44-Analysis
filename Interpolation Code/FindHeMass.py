#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 15:22:20 2022

@authors: Amelia Melhem and Alexis Petty
"""

### Finds estimated He mass in WD given total mass using
### https://articles.adsabs.harvard.edu/pdf/2006MNRAS.371..263L

## Assumes Z = 0.01 and that WD core mass is equal to total mass
## Also assumes that the buffer mass of the He is equal to the total He mass

## 2/9: MBuff function altered to remove mass limits on WD -AM

import numpy as np
import pandas as pd

file = 0 # 0 for first file(aa), 1 for second(ag)

if file == 0:
    dataset = np.loadtxt("../Input Data/SeBa_aa_020418_production_run_wdwd_bob.data")
    fileName = 'Full_SeBa_aa_with_He.txt'
else: 
    dataset = dataset = np.loadtxt("../Input Data/SeBa_ag_020418_production_run_wdwd_bob.data")
    fileName = 'Full_SeBa_ag_with_He.txt'



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
                                             'Mwd2(Msun)', 'type_wd1', 'type_wd2' ])
# Initalize new columns for calculated data
pdDataset['He_min_wd1(Msun)'] = 0
pdDataset['He_min_wd2(Msun)'] = 0
pdDataset['He_max_wd1(Msun)'] = 0
pdDataset['He_max_wd2(Msun)'] = 0


## Function to find the buffer mass given WD mass and variables from Table 6
## Mass assumed to be given in solar masses


def MBuff(mass, a, b, c, d, e): # Too specific to be generalized -AM
    """
    Uses Equation 9 to estimate He Mass given the WD mass and parameters
    
    Parameters
    ----------
    mass : Core Mass of the WD
    a, b, c : Given by the table
    d, e : Min and Max allowed input WD masses. returns '-' if the input is 
    outside this range

    Returns
    -------
    MBuff : The estimated He Mass

    """
    
    #if mass < d or mass > e: #Writes '-' if the mass is not within the acccepted range
    #    MBuff = '-'   
    #    
    #else:
    #    MBuff = 10**(a + b*np.log10(mass) + c*(np.log10(mass)**2)) # Equation 9

    MBuff = 10**(a + b*np.log10(mass) + c*(np.log10(mass)**2))
            
    return MBuff


## Uses MBuff to assign buffer mass values in pdDataset 
## Assumes Z = 0.01

def assignMass(df): # Planned to be generalized at some point
    
    for x in range(len(df)):
        row = x
        
        ## MBuff min 
        a = -3.3243
        b = -6.7603
        c = -3.0043
        d = 0.52
        e = 0.94
        mass = df.iat[row, 3] #WD 1
        df.iat[row, 7] = MBuff(mass, a, b, c, d, e)
    
        mass = df.iat[row, 4] #WD 2
        df.iat[row, 8] = MBuff(mass, a, b, c, d, e)
    
        ## MBuff max 
        a = -2.9129
        b = -6.1056
        c = -5.0948
        d = 0.52
        e = 0.93 
    
        mass = df.iat[row, 3] #WD 1
        df.iat[row, 9] = MBuff(mass, a, b, c, d, e)
    
        mass = df.iat[row, 4] #WD 2
        df.iat[row, 10] = MBuff(mass, a, b, c, d, e)

    return df


## Remove entries that have no He mass attributed

def removeNull(df): # Could be generalized if useful but probably not -AM
    xList = []
    for x in range(len(df)):
        row = x
        if (df.iat[row, 7] == '-' and # change all 'and' to 'or' to only
            df.iat[row, 8] == '-' and # store information when all 4 buffer
            df.iat[row, 9] == '-' and # masses can be found
            df.iat[row, 10] == '-'):
                xList.append(x)
                
    df = df.drop(xList)
    
    return df

pdDataset = assignMass(pdDataset)
pdDataset = removeNull(pdDataset)

# Save as new txt file. Change header to False to be numpy compatible or add
# '#' to the front of the first line of txt.

with open('./' + fileName, 'w') as f:
    dfAsString = pdDataset.to_string(header=True, index=False)
    f.write(dfAsString)
