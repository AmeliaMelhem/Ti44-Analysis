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
for the range of 0.8 to 126 Msun
but that excludes brown dwarfs and such 
moreover, the Salpeter IMF is inaccurate for the range of < 0.5 Msun 
so here, I'll use the Kroupa IMF which is near-identical to Salpeter in the BPS ranges

to calculate total mass, 
you can integrate over [m*IMF(m)]dm for some range of masses
here, I'll use 0.08 to 150 Msun for the Milky Way 
but this is off by some constant relating to stellar density which I must find 
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


def total_mass(m_lo, m_hi, p=1): 
    # uses Kroupa IMF to calculate total stellar mass in some range 
    # off by stellar density constant 
    def antiderivative(m, alpha): 
        return p*((1/(2 - alpha))*m**(2 - alpha))
    if m_lo < 0.08 and m_hi > 0.5: 
        a = antiderivative(0.08, 0.3) - antiderivative(m_lo, 0.3) 
        b = antiderivative(0.5, 1.3) - antiderivative(0.08, 0.3)
        c = antiderivative(m_hi, 2.3) - antiderivative(0.5, 2.3) 
        return a + b + c
    elif (m_lo >= 0.08 and m_lo < 0.5) and m_hi > 0.5: 
        b = antiderivative(0.5, 1.3) - antiderivative(m_lo, 1.3) 
        c = antiderivative(m_hi, 2.3) - antiderivative(0.5, 2.3) 
        return b + c
    else: # ( if m_lo >= 0.5 and m_hi > 0.5: )
        c = antiderivative(m_hi, 2.3) - antiderivative(m_lo, 2.3) 
        return c


# need to calculate constant off-set 
# essential, if we know N(m) for some (or several) m
# where N(m) is TOTAL number of stars with some mass m
# we find the constant p such that N(m) = p*(m**alpha) 
# alpha may be piecewise in Kroupa IMF case 
# BUT! the SeBa people state they assume ALL stars are members of binary systems from their IMF 
# so, I can find the constant by:  Integral[m*IMF(m)dm] = total binary WD mass ???
sum_binary_wd = pd.to_numeric(df['Mwd1(Msun)']).sum() 
sum_binary_wd += pd.to_numeric(df['Mwd2(Msun)']).sum() 
p_SeBa = sum_binary_wd / total_mass(0.8, 126) 


# Now, excluding systems where at least one WD is not Carbon-Oxygen
# type 12 -> CO, type 13 -> He, type 14 -> ONe
df_co = df[df['type_wd1'] == 12.0] 
df_co = df[df['type_wd2'] == 12.0] 

sum_binary_co_wd = pd.to_numeric(df_co['Mwd1(Msun)']).sum()  
sum_binary_co_wd += pd.to_numeric(df_co['Mwd2(Msun)']).sum() 


# calculating mass fraction 
# total_stellar_mass = (1 + x)*binaryCO-WD_mass
x = sum_binary_wd/sum_binary_co_wd - 1
print(x) 
x = total_mass(0.8, 126, p_SeBa)/sum_binary_co_wd - 1
print(x) 
