
"""
JG 
continuation of rbf_interp.py 
for plotting and testing validity of the fits
""" 

from rbf_interp import * 
import matplotlib.pyplot as plt

data = np.loadtxt("../../Input Data/he_co_ti_dat.txt") 
pts = data[:,0:2] # Helium and Core masses
vals = data[:,2] # Ti44 masses

funcs = ("multiquadric", "inv_multiquadric", "thin_plate_spline", "gaussian") 
nrbf = (False, True) 
labels = np.array([["multiquadric", "norm_multiquad"], ["inv_multiquad", "norm_inv_multiquad"], ["spline", "norm_spline"], ["gaussian", "norm_gaussian"]])  

he_arr = pts[:,0] 
co_arr = pts[:,1] 
he_arr = np.linspace(np.amin(he_arr), np.amax(he_arr), 50) 
co_arr = np.linspace(np.amin(co_arr), np.amax(co_arr), 50) 


# Toggle the following for debugging 
"""
ti_interp = RBF_interp(pts, vals, func = funcs[3], norm = nrbf[1])

print(ti_interp.err()) 
print(ti_interp.scale) 

ti_interp.optimize() 
print(ti_interp.err()) 
print(ti_interp.scale) 
"""


# The following code plots each possible func/normalization 
# and includes error and optimal scale factor values 
i = 0 
j = 0
for i in range(len(funcs)): 
    for j in range(len(nrbf)): 
        # set-up interpolating function 
        ti_interp = RBF_interp(pts, vals, func = funcs[i], norm = nrbf[j]) 
        ti_interp.optimize() 
        label = labels[i][j] 
        error = ti_interp.err() 

        # here I have to populate a table of interpolated values 
        ti_interp_tab = np.zeros((len(he_arr), len(co_arr))) 
        for k in range(len(he_arr)): 
            for l in range(len(co_arr)): 
                temp_pt = (he_arr[k],co_arr[l]) 
                ti_interp_tab[k][l] = ti_interp.interp(temp_pt) 

        # plotting configuration 
        plt.pcolormesh(he_arr, co_arr, ti_interp_tab)
        plt.colorbar().set_label("Ti44 Mass", rotation=270) 
        plt.title(f"RBF: {label}\nError: {error}") 
        plt.xlabel("He mass") 
        plt.ylabel("Core mass") 
        plt.savefig("../../Plots/rbf_interp_plots/" + label)
