
"""
JG
Cross-referencing our fits from the data from Gronow paper to those of "Explosive nucleosynthesis in sub Ch-Mass WD models for type Ia supernova... by Leung and Nomoto 
specifically from table 13 which depicts abundances of radioactive isotopes after various detonations and abundances of Helium

Note: table13 evidently shows abundances following helium detonation as the Gronow data for the core detonation was orders of magnitude different
"""

import numpy as np
import matplotlib.pyplot as plt

leung_data = np.loadtxt('Ti_He_Leung_T13.txt', usecols=(1, 2, 3, 4, 5, 6, 7)) 
# row 2 is He mass and row 3 is Ti44 mass
leung_he = leung_data[1,:]
leung_ti = leung_data[2,:] 

gronow_data = np.loadtxt('Ti_He_Gronow.txt', skiprows = 1, usecols=(1, 2, 3, 4)) 
gronow_he = gronow_data[:,0]
gronow_ti = gronow_data[:,1]
# This is data from the helium detonation 

# I'm unsure whether Ti/He should be independent var but I think Ti44 is the 'observed' quantity so I'll let it be x-axis
plt.scatter(gronow_ti, gronow_he, color = 'Green', label = "Gronow Data") 
plt.scatter(leung_ti, leung_he, color = 'Magenta', label = "Lueng Data")

plt.title("Final abundances of Helium and Titanium^44 following detonation") 
plt.xlabel("Ti44 (Solar Masses)") 
plt.ylabel("He (Solar Masses)") 

plt.legend() 
plt.show() 

