"""
JG
This calculation intends to find the total initial stellar mass
involved in the production of the Ti44, as calculated in rbf_interp_outp.py

This includes not only binary WD systems, but all other stellar masses
Which is represented by 
Total Stellar Mass = (1 + x)*binary_WD_mass 
where x is a mass fraction of: "other stars mass" / binary_WD_mass 

for the BPS models, 
the SeBa folks used the Salpeter (1955) initial mass function (IMF) 
for the range of 0.1 to 100 Msun
but that excludes brown dwarfs and higher mass stars and such 
moreover, the Salpeter IMF is inaccurate for the range of < 0.5 Msun 

to calculate total mass, 
you can integrate over [m*IMF(m)]dm for some range of masses
here, I'll use 0.1 to 126 Msun for the Milky Way 
but this is off by some constant relating to stellar density which I must find 

UPDATE: 
I can find the constant xi_0 by knowing that, 
stars with initial masses in range 0.08 -> 12 are expected to form WDs 
and stars with initial masses in range 0.8 -> 8 form CO WDs specifically
ie, for a system with N CO WDs
we have N = \int_{0.8Msun}^{8Msun} IMF(m)dm

Also, found: websites.pmc.ucsc.edu/~glatz/astr_112/lectures/notes19.pdf
which has helped my understanding
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


# Splicing dataframes between those with/without non-CO WDs 
# type 12 -> CO, type 13 -> He, type 14 -> ONe
df_co = df[df['type_wd1'] == 12.0] 
df_co = df[df['type_wd2'] == 12.0] 

# Calculating mass sums of both dataframes 
sum_binary_wd = pd.to_numeric(df['Mwd1(Msun)']).sum() 
sum_binary_wd += pd.to_numeric(df['Mwd2(Msun)']).sum() 

sum_binary_co_wd = pd.to_numeric(df_co['Mwd1(Msun)']).sum()  
sum_binary_co_wd += pd.to_numeric(df_co['Mwd2(Msun)']).sum() 


# Calculating constant xi_0
N_wd = 2*len(df) # twice ~120,000
N_CO_wd = 2*len(df_co) # twice ~40,000
# I added factor of two as is in binary systems 

xi_0_CO = N_CO_wd / ((8**(-1.35))/(-1.35) - (0.5**(-1.35))/(-1.35))
print(f"xi_0 from CO WD estimate: {xi_0_CO}")  
xi_0 = N_wd / ((12**(-1.35))/(-1.35) - (0.1**(-1.35))/(-1.35))
print(f"xi_0 from total WD estimate: {xi_0}")  
"""
Values for xi_0 are slightly contradictory when considering: 
    m in range (0.1, 12) become WDs
        associated mass-fraction: 0.567
    m in range (0.8, 8) become CO WDs
        associated mass-fraction: 8.276
I have been hung up on this weird discrepancy for a while,
but for now I'll take the value of 0.567 to be more "reasonable"????
"""

# calculating mass fraction 
def total_init_mass(m_lo, m_hi, xi): 
    # integrand is m*IMF(m) 
    # ie xi_0*m^(-1.35) 
    return (xi/(-0.35))*(m_hi**(-0.35) - m_lo**(-0.35)) 

x_CO = (total_init_mass(0.1, 100, xi_0_CO) / sum_binary_co_wd) - 1
print(f"x from CO WD estimate: {x_CO}") 
x = (total_init_mass(0.1, 100, xi_0) / sum_binary_co_wd) - 1
print(f"x from total WD estimate: {x}") 

"""
Next steps: 
normalize truncated sample to mass fraction 
to achieve Ti44 / mass / time 
then, 
using approx. constant SFR of 10 Msun / year 
to estimate net Ti44 produced per time 
""" 
