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
off by some constant relating to stellar density 

So, 
As far as I know, 
I can find this fraction by comparing the total binary WD mass in the sample
to the integral of the IMF over the entire range of masses 
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

# defining Salpeter initial mass function 
def IMF(m): 
    return m**(-2.35)
# defining integrand as m*IMF(m) for total mass
# and taking the antiderivative of such, 
def antiderivative(m): 
    return (-1/0.35)*(m**(-0.35)) 

# approximating total mass by integrating IMF (from 0.08Msun to, say, 150Msun) 
# this is supposed to represent the lower and upper limits of star masses 
# alternatively, the SeBa folks used bounds of between 0.8 to 126 Msun
# but that excludes the lower range of brown dwarfs and such
total = antiderivative(126) - antiderivative(0.8) 

# calculating constant off-set 
# essential, if we know N(m) for some m
# where N(m) is TOTAL number of stars with some mass m
# we find the constant p such that N(m) = p*(m**-2.35) 

# Excluding systems where at least one WD is not Carbon-Oxygen
# type 12 -> CO, type 13 -> He, type 14 -> ONe
df_co = df[df['type_wd1'] == 12.0] 
df_co = df[df['type_wd2'] == 12.0] 

sum_wdm = pd.to_numeric(df_co['Mwd1(Msun)']).sum()  
sum_wdm += pd.to_numeric(df_co['Mwd2(Msun)']).sum() 

# calculating mass fraction 
# total_stellar_mass = (1 + x)*binaryCO-WD_mass
x = (total/sum_wdm)
print(x) 
