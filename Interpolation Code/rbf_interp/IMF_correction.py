"""
JG
This calculation intends to find the total initial stellar mass
involved in the production of the Ti44, as calculated in rbf_interp_outp.py

This includes not only binary WD systems, but all other stellar masses
Which is represented by 
Total Stellar Mass = (1 + x)*binary_WD_mass 
where x is a mass fraction of: "other stars mass" / binary_WD_mass 

the SeBa folks used the Salpeter (1955) initial mass function (IMF) 
which is a power law of -2.35
ie 
N(m)dm ~ m^(-2.35) * Delta_m
for the number stars with masses in range (m , m + Delta_m) 

alternatively cast in terms of Xi (which is stellar mass density??) 

So, 
As far as I know, 
I can find this fraction by comparing the total binary WD mass in the sample
to the integral of the IMF over the entire range of masses 
but what range of masses to use?

""" 

# includes ...
import pandas as pd
import numpy as np

# Importing data 
df = pd.read_csv("../../Input Data/SeBa_aa_020418_production_run_wdwd_bob.data", delim_whitespace=True, index_col=False)  
# Gives extraneous error due to second header row that I discard in the following lines
df = df.shift(periods=1, axis=1) 
df = df.drop(['#'], axis=1) 
df = df.drop([0], axis=0) 
# Data is organized with the following column labels: 
# id
# DWD_formation_time(Myr) 
# time_of_merger(Myr) 
# Mwd1(Msun) 
# Mwd2(Msun) 
# type_wd1
# type_wd2

# Defining Salpeter initial mass function 
def IMF(m): 
    return m**(-2.35)
def IMF_antiderivative(m): 
    return -2.35*m**(-3.35) 

# Finding maximum and minimum WD masses for integration bounds 
# Probably should change this later but it's a start 
max_m = pd.to_numeric(df['Mwd1(Msun)']).max() 
if max_m < pd.to_numeric(df['Mwd2(Msun)']).max(): 
    max_m = pd.to_numeric(df['Mwd2(Msun)']).max() 
min_m = pd.to_numeric(df['Mwd1(Msun)']).min() 
if min_m > pd.to_numeric(df['Mwd2(Msun)']).min(): 
    min_m = pd.to_numeric(df['Mwd2(Msun)']).min() 

# Excluding systems where at least one WD is not Carbon-Oxygen
# type 12 -> CO, type 13 -> He, type 14 -> ONe
df_co = df[df['type_wd1'] == 12.0] 
df_co = df[df['type_wd2'] == 12.0] 

sum_wdm = pd.to_numeric(df_co['Mwd1(Msun)']).sum()  
sum_wdm += pd.to_numeric(df_co['Mwd2(Msun)']).sum() 

# calculating approximate mass fraction 
total = IMF_antiderivative(max_m) - IMF_antiderivative(min_m) 
mass_frac = (total/sum_wdm)
print(mass_frac) 
