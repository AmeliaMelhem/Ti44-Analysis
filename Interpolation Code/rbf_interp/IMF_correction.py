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
from scipy.integrate import quad


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

print('\n\n\n') # Weird Pandas error so this makes more readable

###################################################

def Kroupa_IMF(m, xi): 
    if m < 0.08: 
        alpha = 0.3
    elif m >= 0.08 and m < 0.5: 
        alpha = 1.3
    elif m >= 0.5: 
        alpha = 2.3
    return xi*m**(-1 * alpha) 

def Salpeter_IMF(m, xi): 
    return xi*(m**(-2.35)) 

def IMF_integral(m_lo, m_hi, xi, fn, find_mass=True): 
    # Integrates IMF over range m_lo to m_hi
    # find_mass bool determines what integral will yield
    #   t: total mass over said range
    #   f: total number of stars in range
    def integrand(m, xi): 
        if find_mass: 
            return m*fn(m, xi)
        else: 
            return fn(m, xi)
    return quad(integrand, m_lo, m_hi, args=(xi))[0]

# Calculating constant xi_0
N_wd = 2*len(df) # twice ~120,000
N_CO_wd = 2*len(df_co) # twice ~40,000
# I added factor of two as it is a binary system 
# and we assume f_bin = N_b / (N_b + N_s) = 50% (effectively another 2x) 
xi_0_CO = N_CO_wd / (0.5 * IMF_integral(0.5, 8, 1, Kroupa_IMF, find_mass=False)) 
print(f"xi_0 from CO WD estimate: {xi_0_CO}")  
xi_0_tot = N_wd / (0.5 * IMF_integral(0.08, 12, 1, Kroupa_IMF, find_mass=False))
print(f"xi_0 from total WD estimate: {xi_0_tot}")  
# They are somewhat similar so let us average 
xi_0_avg = 0.5 * (xi_0_CO + xi_0_tot) 


# This dissented quite a bit from the prior method
# But, finding xi such that total mass is known
# According to SeBa people, for this simulation: 
total_mass = 38499996
xi_0_alt = total_mass / IMF_integral(0.1, 100, 1, Salpeter_IMF, find_mass=True) 
print(f"xi_0 from total mass: {xi_0_alt}") 
# Questions: 
# What mass range did SeBa use? They used Salpeter IMF? 


# Now calculating ~mass~ fraction as opposed to that by number of stars 
# x_co_bin = mass of binary CO white dwarfs / total initial mass formed ~ 0.14
# x_wd_bin = mass of all binary white dwards / total initial mass formed ~ 0.325
x_co_bin = sum_binary_co_wd / IMF_integral(0.1, 100, xi_0_avg, Kroupa_IMF, find_mass=True) 
print(f"mass fraction of binary CO WDs per total mass: {x_co_bin}") 
x_wd_bin = sum_binary_wd / IMF_integral(0.1, 100, xi_0_avg, Kroupa_IMF, find_mass=True) 
print(f"mass fraction of all binary WDs per total mass: {x_wd_bin}") 
