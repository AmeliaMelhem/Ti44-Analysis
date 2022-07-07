"""
Created on Thursday June 30
@authors: John Gallagher
Using data from the Gronow et al paper located at tables 3, 4, 5, 6 to 
interpolate a relation between final abundances of He and Ti^44
Found at https://doi.org/10.1051/0004-6361/202039954
""" 

# R-Squared values for the various fits:
# Gronow not logged:
# HD: 0.389223216, CD: 0.595582972
# Gronow logged:
# HD: 0.4173998675, CD: 0.638657051
# Leung not logged: 0.469021872
# Leung logged: 0.350830245


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Idea for future Amy: have both files be found at once instead of needing to run the code twice
file = 0 # 0 for first file(aa), 1 for second(ag)


LeungData = np.loadtxt('Ti_He_Leung_T13.txt', usecols=(1, 2, 3, 4, 5, 6, 7))
GronowData = np.loadtxt('./Ti_He_Gronow.txt', skiprows = 1, usecols=(1, 2, 3, 4))
# I changed the filename to be more descriptive - JG

if file == 0:
    df = pd.read_csv('./SeBa_aa_with_He.txt', delim_whitespace=True, index_col=False)
    fileName = 'SeBa_aa_Ti_interp.txt'
else: 
    df = pd.read_csv('./SeBa_ag_with_He.txt', delim_whitespace=True, index_col=False)
    fileName = 'SeBa_ag_Ti_interp.txt'



#Pulls He and Ti masses for det type. Also, I removed the np.log10 -AM
hd_he = np.log10(GronowData[:,0])
hd_ti = np.log10(GronowData[:,1])

cd_he = np.log10(GronowData[:,2])
cd_ti = np.log10(GronowData[:,3])

leung_he = np.log10(LeungData[1,:])
leung_ti = np.log10(LeungData[2,:])


#Creates a least squares fit 
#I swapped Ti and He since we are looking for Ti - AM
#Also note: the values for the linspace should be changed to be automatically found from the file -AM
# Good point! I changed the values for linspace to be automatically found from the file by using amin/amax -JG

hd_fit = np.polyfit(hd_he, hd_ti, 1)
hd_he_model = np.linspace(np.amin(hd_he+hd_he*0.15), np.amax(hd_he-hd_he*0.15), 10) 
hd_ti_model = hd_fit[1] + hd_fit[0]*hd_he_model

cd_fit = np.polyfit(cd_he, cd_ti, 1)
cd_he_model = np.linspace(np.amin(cd_he+cd_he*0.15), np.amax(cd_he-cd_he*0.15), 10)
cd_ti_model = cd_fit[1] + cd_fit[0]*cd_he_model

leung_fit = np.polyfit(leung_he, leung_ti, 1)
leung_he_model = np.linspace(np.amin(leung_he+leung_he*0.15), np.amax(leung_he-leung_he*0.15), 10)
leung_ti_model = leung_fit[1] + leung_fit[0]*leung_he_model




#Plots data from paper
plt.scatter(hd_he, hd_ti, color = 'red', label = 'Gronow He Detonation Data') 
plt.scatter(cd_he, cd_ti, color = 'blue', label = 'Gronow Core Detonation Data')
plt.scatter(leung_he, leung_ti, color = 'green', label = 'Leung Data')


#Plots least squares fit
plt.plot(hd_he_model, hd_ti_model, color = 'red', label = 'He Detonation Model') 
plt.plot(cd_he_model, cd_ti_model, color = 'blue', label = 'Core Detonation Model')
plt.plot(leung_he_model, leung_ti_model, color = 'green', label = 'Leung Model')


plt.title('Mass of He vs Ti at detonation')
plt.ylabel('Mass Ti-44 (Log10 Msun)')
plt.xlabel('Mass He (Log10 Msun)')
plt.legend() 

#plt.savefig("Ti_linear_interp_model")
plt.show() 





#Initialize new columns for new data
df['He_Det_Ti_min_wd1(Log10 Msun)'] = 0
df['He_Det_Ti_min_wd2(Log10 Msun)'] = 0
df['He_Det_Ti_max_wd1(Log10 Msun)'] = 0
df['He_Det_Ti_max_wd2(Log10 Msun)'] = 0

df['Core_Det_Ti_min_wd1(Log10 Msun)'] = 0
df['Core_Det_Ti_min_wd2(Log10 Msun)'] = 0
df['Core_Det_Ti_max_wd1(Log10 Msun)'] = 0
df['Core_Det_Ti_max_wd2(Log10 Msun)'] = 0

df['Leung_Ti_min_wd1(Log10 Msun)'] = 0
df['Leung_Ti_min_wd2(Log10 Msun)'] = 0
df['Leung_Ti_max_wd1(Log10 Msun)'] = 0
df['Leung_Ti_max_wd2(Log10 Msun)'] = 0



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
        
        
        ## Leung data
        a = leung_fit[0]
        b = leung_fit[1]

        HeMass = df.iat[row, 7] #WD 1 min
        df.iat[row, 19] = TiMass(HeMass, a, b)
    
        HeMass = df.iat[row, 8] #WD 2 min
        df.iat[row, 20] = TiMass(HeMass, a, b)

        HeMass = df.iat[row, 9] #WD 1 max
        df.iat[row, 21] = TiMass(HeMass, a, b)
    
        HeMass = df.iat[row, 10] #WD 2 max
        df.iat[row, 22] = TiMass(HeMass, a, b)        
        
        
    return df


# df = assignMass(df)

# Save as new txt file. Change header to False to be numpy compatible or add
# '#' to the front of the first line of txt.

# with open('./' + fileName, 'w') as f:
#     dfAsString = df.to_string(header=True, index=False)
#     f.write(dfAsString)




