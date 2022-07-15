"""
JG 
week of 7/11-15
Plotting interpolated function against He and core mass in various forms
more specifically, 
plotting the values closest to the He and CO mass values within fit_t
using arrays created in fits.py 
""" 

from ti_interp2d import * 

print("1 - Ti44 x He \n2 - Ti44 x CO \n3 - Ti(He,CO) \n4 - He x CO")
inp = input() 
if inp == "1": 
   plt.scatter(he_data, ti_data, color = 'Red', label = 'Data') 
   plt.scatter(he_data, ti_model, color = 'Blue', label = 'Model') 
   # plt.plot(he_arr, fit_t[0,:], color = 'Blue', label = 'Fit') 
   plt.plot(he_arr, np.zeros(len(he_arr),), 'k-') 
   plt.title("Ti44 related to initial He mass") 
   plt.xlabel("He Mass / Msun") 
   plt.ylabel("Ti44 mass / Msun") 
   plt.legend() 
   plt.savefig("../Plots/interp2d_1.png") 
elif inp == "2": 
   plt.scatter(co_data, ti_data, color = 'Red', label = 'Data') 
   plt.scatter(co_data, ti_model, color = 'Blue', label = 'Model')
   # plt.plot(co_arr, fit_t[:,0], color = 'Blue', label = 'Fit') 
   plt.plot(co_arr, np.zeros(len(co_arr),), 'k-') 
   plt.title("Ti44 related to initial core mass") 
   plt.xlabel("Core mass / Msun") 
   plt.ylabel("Ti44 mass / Msun") 
   plt.legend() 
   plt.savefig("../Plots/interp2d_2.png") 
elif inp == "3": 
    plt.pcolormesh(he_arr, co_arr, fit_f(he_arr, co_arr)) 
    plt.colorbar().set_label("Ti44 Mass", rotation=270)  
    plt.title("Ti44 mass as function of He and Core masses") 
    plt.xlabel("He mass / Msun") 
    plt.ylabel("Core mass / Msun") 
    plt.savefig("../Plots/interp2d_3.png") 
elif inp == "4": 
    plt.scatter(co_data, he_data) # mostly just for testing
plt.show()
