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

plt.scatter(hd_ti, hd_he, color = 'red', label = 'Helium Detonation Data') 
plt.scatter(cd_ti, cd_he, color = 'blue', label = 'Core Detonation Data')

hd_fit = np.polyfit(hd_ti, hd_he, 1)
hd_ti_model = np.linspace(-4, -2.5, 10) 
hd_he_model = hd_fit[1] + hd_fit[0]*hd_ti_model

cd_fit = np.polyfit(cd_ti, cd_he, 1)
cd_ti_model = np.linspace(-5, -4.7, 10)
cd_he_model = cd_fit[1] + cd_fit[0]*cd_ti_model

plt.plot(hd_ti_model, hd_he_model, color = 'red', label = 'He Detonation Model')
plt.plot(cd_ti_model, cd_he_model, color = 'blue', label = 'Core Detonation Model')


plt.title('Final Abundances of Ti against He for Various Core and Shell Masses')
plt.xlabel('Log M_Ti^44 / M_Solar')
plt.ylabel('Log M_He / M_Solar')
plt.legend() 

plt.savefig("ti_interpolation")
plt.show() 
