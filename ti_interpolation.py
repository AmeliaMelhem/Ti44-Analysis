"""
Created on Thursday June 30
@authors: John Gallagher
Using data from the Gronow et al paper located at tables 3, 4, 5, 6 to interpolate a relation between final abundances of He and Ti^44
Found at https://doi.org/10.1051/0004-6361/202039954
""" 

import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('./Ti_from_He.txt', skiprows = 1, usecols=(1, 2, 3, 4))

hd_he = np.log10(data[:,0])
hd_ti = np.log10(data[:,1])

cd_he = np.log10(data[:,2])
cd_ti = np.log10(data[:,3])

plt.scatter(hd_ti, hd_he, label = 'Core Detonation') 
plt.scatter(cd_ti, cd_he, label = 'Helium Detonation')

plt.title('Final Abundances of Ti against He for Various Core and Shell Masses')
plt.xlabel('Log M_Ti^44 / M_Solar')
plt.ylabel('Log M_He / M_Solar')
plt.legend() 

plt.savefig("ti_interpolation")
plt.show() 
