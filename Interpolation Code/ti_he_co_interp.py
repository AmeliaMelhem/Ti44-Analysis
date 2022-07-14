
"""
JG

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d 


gronow_data = np.loadtxt('../Input Data/Ti_He_Gronow.txt', skiprows=1, usecols= (1,2,5)) 
leung_data = np.loadtxt('../Input Data/Ti_He_Leung_T13.txt', usecols = (1,2,3,4,5,6,7))


he_data = gronow_data[:,0] 
he_data = np.append(he_data, leung_data[1,:]) 

co_data = gronow_data[:,2]
co_data = np.append(co_data, leung_data[0,:]) 

ti_data = gronow_data[:,1] 
ti_data = np.append(ti_data, leung_data[2,:]) 

fit = interp2d(he_data, co_data, ti_data, kind='linear') 

he_arr = np.linspace(np.amin(he_data), np.amax(he_data), 150) 
co_arr = np.linspace(np.amin(co_data), np.amax(co_data), 150) 



inp = input("Choose He or CO: ") 
if inp == "He": 
   plt.scatter(he_data, ti_data, color = 'Red', label = 'Data') 
   plt.plot(he_arr, fit(he_arr, co_arr)[0,:], color = 'Blue', label = 'Model') 
elif inp == "CO": 
   plt.scatter(co_data, ti_data, color = 'Red', label = 'Data') 
   plt.plot(co_arr, fit(he_arr, co_arr)[:,0], color = 'Blue', label = 'Model') 


plt.show() 
