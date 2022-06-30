"""
Created on Thursday June 30
@authors: John Gallagher
Using data from the Gronow et al paper located at tables 3, 4, 5, 6 to interpolate a relation between final abundances of He and Ti^44
Found at https://doi.org/10.1051/0004-6361/202039954
""" 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


file = 1 # 0 for first file(aa), 1 for second(ag)

data = np.loadtxt('./Ti_from_He.txt', skiprows = 1, usecols=(1, 2, 3, 4))

if file == 0:
    df = pd.read_csv('./SeBa_aa_with_He.txt', delim_whitespace=True, index_col=False)
    fileName = 'SeBa_aa_Ti_interp.txt'
else: 
    df = pd.read_csv('./SeBa_ag_with_He.txt', delim_whitespace=True, index_col=False)
    fileName = 'SeBa_ag_Ti_interp.txt'



#Pulls He and Ti masses for det type [I removed the np.log10() -AM]
hd_he = (data[:,0])
hd_ti = (data[:,1])

cd_he = (data[:,2])
cd_ti = (data[:,3])



#Creates a least squares fit [I swapped Ti and He since we are looking for Ti - AM]
hd_fit = np.polyfit(hd_he, hd_ti, 1)
hd_he_model = np.linspace(-4, -2.5, 10) 
hd_ti_model = hd_fit[1] + hd_fit[0]*hd_he_model

cd_fit = np.polyfit(cd_he, cd_ti, 1)
cd_he_model = np.linspace(-5, -4.7, 10)
cd_ti_model = cd_fit[1] + cd_fit[0]*cd_he_model



#Plots data from paper
plt.scatter(hd_he, hd_ti, color = 'red', label = 'Helium Detonation Data') 
plt.scatter(cd_he, cd_ti, color = 'blue', label = 'Core Detonation Data')


#Plots least squares fit
# plt.plot(hd_ti_model, hd_he_model, color = 'red', label = 'He Detonation Model')
# plt.plot(cd_ti_model, cd_he_model, color = 'blue', label = 'Core Detonation Model')


plt.title('Final Abundances of Ti against He for Various Core and Shell Masses')
plt.xlabel('Log Ti-44 (Msun)')
plt.ylabel('Log He (Msun)')
plt.legend() 

# plt.savefig("HDti_interpolation")
# plt.show() 



#Initialize new columns for new data
df['He_Det_Ti_min_wd1(Msun)'] = 0
df['He_Det_Ti_min_wd2(Msun)'] = 0
df['He_Det_Ti_max_wd1(Msun)'] = 0
df['He_Det_Ti_max_wd2(Msun)'] = 0

df['Core_Det_Ti_min_wd1(Msun)'] = 0
df['Core_Det_Ti_min_wd2(Msun)'] = 0
df['Core_Det_Ti_max_wd1(Msun)'] = 0
df['Core_Det_Ti_max_wd2(Msun)'] = 0



def TiMass(HeMass, a, b):
    '''
    Parameters
    ----------
    HeMass : float
        Mass of the helium
    a : float
        First coeffient(for highest power term).
    b : float
        Last coeffient(for 0th power term).

    Returns
    -------
    TiMass: float or string
        Returns estimated mass for Ti. Assigned as '-' if no applicable mass.
    '''
    
    if HeMass == '-': #Writes '-' if the mass is not applicable
        TiMass = '-'   
        
    else:
        TiMass = a*float(HeMass) + b # Lin Interp
        
    return TiMass


def assignMass(df):
    
    for x in range(len(df)):
        row = x
        
        ## He det 
        a = hd_fit[0]
        b = hd_fit[1]

        HeMass = df.iat[row, 7] #WD 1 min
        df.iat[row, 11] = TiMass(HeMass, a, b)

        HeMass = df.iat[row, 8] #WD 2 min
        df.iat[row, 12] = TiMass(HeMass, a, b)

        HeMass = df.iat[row, 9] #WD 1 max
        df.iat[row, 13] = TiMass(HeMass, a, b)
    
        HeMass = df.iat[row, 10] #WD 2 max
        df.iat[row, 14] = TiMass(HeMass, a, b)


        ## Core det
        a = cd_fit[0]
        b = cd_fit[1]

        HeMass = df.iat[row, 7] #WD 1 min
        df.iat[row, 15] = TiMass(HeMass, a, b)
    
        HeMass = df.iat[row, 8] #WD 2 min
        df.iat[row, 16] = TiMass(HeMass, a, b)

        HeMass = df.iat[row, 9] #WD 1 max
        df.iat[row, 17] = TiMass(HeMass, a, b)
    
        HeMass = df.iat[row, 10] #WD 2 max
        df.iat[row, 18] = TiMass(HeMass, a, b)
    return df


df = assignMass(df)

# Save as new txt file. Change header to False to be numpy compatible or add
# '#' to the front of the first line of txt.

with open('./' + fileName, 'w') as f:
    dfAsString = df.to_string(header=True, index=False)
    f.write(dfAsString)




