
"""
JG
Cross-referencing our fits from the data from Gronow paper to those of 
"Explosive nucleosynthesis in sub Ch-Mass WD models for type Ia supernova... by Leung and Nomoto 
specifically from table 13 which depicts abundances of radioactive isotopes after various detonations and abundances of Helium

Note: table13 evidently shows abundances following helium detonation as the Gronow data for the core detonation
was orders of magnitude different
"""


import numpy as np
import matplotlib.pyplot as plt

leung_data = np.loadtxt('../Input Data/Ti_He_Leung_T13.txt', usecols=(1, 2, 3, 4, 5, 6, 7)) 
gronow_data = np.loadtxt('../Input Data/Ti_He_Gronow.txt', skiprows = 1, usecols=(1, 2, 3, 4))


# row 2 is He mass and row 3 is Ti44 mass
leung_he = leung_data[1,:]
leung_ti = leung_data[2,:] 


# This is data from the helium detonation 
gronow_he_HD = gronow_data[:,0]
gronow_ti_HD = gronow_data[:,1]


# This is data from the core detonation 
gronow_he_CD = gronow_data[:,2]
gronow_ti_CD = gronow_data[:,3]




# I'm unsure whether Ti/He should be independent var but I think Ti44 is the 'observed' quantity so I'll let it be x-axis
# So our idea is to use the He masses to try to estimate the Ti masses. So since the Ti mass will depend on the He mass, the
# Ti should be on the y-axis. -AM
plt.scatter(gronow_he_HD, gronow_ti_HD, color = 'Green', label = "Gronow He-Det Data") 
#plt.scatter(gronow_he_CD, gronow_ti_CD, color = 'Blue', label = "Gronow Core-Det Data") #Ends up being too small to view
plt.scatter(leung_he, leung_ti, color = 'Magenta', label = "Lueng Data")

plt.title("Final abundances of Helium and Titanium-44 following detonation") 
plt.xlabel("He (Solar Masses)") 
plt.ylabel("Ti-44 (Solar Masses)") 

plt.legend() 
plt.show() 
