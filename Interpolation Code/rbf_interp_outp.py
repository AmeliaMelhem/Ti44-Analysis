
"""
JG 
Utilizing the most sensible RBF interpolation to output Ti/e+ data from the SeBa sample 
Using the shortened sample that arose from NANs in finding He mass 

Justification for Ti44 mass interpolation: 
Upon fixing the error calculation for the SciPy routine, 
I found it to be about twice that of any RBF interpolation (at around 230%) 

I chose the multiquadric basis function because, 
although the error was slightly higher for known points (at around 112%), 
the colormesh plot seemed much more sensible

ie the gaussian and inverse-multiquadric fits were 'more accurate' for the sampled points, 
but died almost immediately elsewhere
which assuredly would cause problems (greatly underestimating e+ produced from 1A events) 
also, they were optimized near the limit that scale-factor -> 0 
while having strange behavior at exactly zero 

the multiquadric fit showed no preference for known values, 
and was optimized precisely with scale-factor set to zero, with no strange behavior 
so we have, very simply, phi(r) = |r| 
and our fit is just a linear combination of |r| that spans dim(# of data points) 
""" 
####################


# includes ...
import sys
sys.path.append('../')
from rbf_interp import * 
#import numpy as np (within rbf_interp) 
import pandas as pd 
from scipy.optimize import curve_fit 
from scipy.integrate import quad
import matplotlib.pyplot as plt


######### Importing Data ############

# Data from Gronow and Leung papers 
ti_data = np.loadtxt('../Input Data/he_co_ti_dat.txt') 
pts = ti_data[:,0:2] # Helium and Core masses 
vals = ti_data[:,2] # Ti44 masses 

# Interpolating Ti mass function based on above data 
ti_interp = RBF_interp(pts, vals, func = "multiquadric", scale = 0, norm = True) 

# SeBa data 
aa_df = pd.read_csv("../Output Data/Extended Range WD He Mass/Full_He_aa_with_Zenati.txt", delim_whitespace=True, index_col=False)
aa_df = aa_df.shift(periods=1, axis=1) 
ag_df = pd.read_csv("../Output Data/Extended Range WD He Mass/Full_He_ag_with_Zenati.txt", delim_whitespace=True, index_col=False) 
ag_df = ag_df.shift(periods=1, axis=1) 
# a*_dat is organized as follows: 
# Column 0: # (nan) 
# Column 1: id
# Column 2: DWD_formation_time(Myr) 
# Column 3: time_of_merger(Myr) 
# Column 4: Mwd1(Msun) 
# Column 5: Mwd2(Msun) 
# Column 6: type_wd1
# Column 7: type_wd2 
# Column 8: He_min_wd1(Msun)
# Column 9: He_min_wd2(Msun)
# Column 10: He_max_wd1(Msun) 
# Column 11: He_max_wd2(Msun) 


############ Organizing data ############ 

# Sorting dataframes by time of merger 
aa_df = aa_df.sort_values(by='time_of_merger(Myr)') 
ag_df = ag_df.sort_values(by='time_of_merger(Myr)') 

# Time of merger NumPy arrays 
aa_times = np.array(aa_df.loc[:,'time_of_merger(Myr)']) 
ag_times = np.array(ag_df.loc[:,'time_of_merger(Myr)'])  

# Organizing input points (He,CO) into NumPy arrays 
aa_wd1min_pts = np.array(aa_df.loc[:,['He_min_wd1(Msun)','Mwd1(Msun)']])
aa_wd1max_pts = np.array(aa_df.loc[:,['He_max_wd1(Msun)','Mwd1(Msun)']])
aa_wd2min_pts = np.array(aa_df.loc[:,['He_min_wd2(Msun)','Mwd2(Msun)']])
aa_wd2max_pts = np.array(aa_df.loc[:,['He_max_wd2(Msun)','Mwd2(Msun)']])

ag_wd1min_pts = np.array(ag_df.loc[:,['He_min_wd1(Msun)','Mwd1(Msun)']])
ag_wd1max_pts = np.array(ag_df.loc[:,['He_max_wd1(Msun)','Mwd1(Msun)']])
ag_wd2min_pts = np.array(ag_df.loc[:,['He_min_wd2(Msun)','Mwd2(Msun)']])
ag_wd2max_pts = np.array(ag_df.loc[:,['He_max_wd2(Msun)','Mwd2(Msun)']])

# Interpolated Ti mass arrays 
""" 
Note: maxHe does not necessarily imply more Ti produced 
so it's best to think of ti_max vs ti_min as just two different samples 
but they do appear to be correlated as expected 
"""
aa_ti_max = np.array(ti_interp.arr_interp(aa_wd1max_pts)) 
aa_ti_max += np.array(ti_interp.arr_interp(aa_wd2max_pts)) 
aa_ti_min = np.array(ti_interp.arr_interp(aa_wd1min_pts)) 
aa_ti_min += np.array(ti_interp.arr_interp(aa_wd2min_pts)) 

ag_ti_max = np.array(ti_interp.arr_interp(ag_wd1max_pts)) 
ag_ti_max += np.array(ti_interp.arr_interp(ag_wd2max_pts)) 
ag_ti_min = np.array(ti_interp.arr_interp(ag_wd1min_pts)) 
ag_ti_min += np.array(ti_interp.arr_interp(ag_wd2min_pts)) 

#################

# 11/07
# instead of normalization method commented out below, I'll try using the DTD from Crocker et al paper
# which they had arbitrarily scaled
# and normalize it such that, when integrated over Milky Way's life, it equals the grand total Ti produced

sum_aa_Ti_max = np.sum(aa_ti_max)
sum_ag_Ti_max = np.sum(ag_ti_max)
sum_aa_Ti_min = np.sum(aa_ti_min)
sum_ag_Ti_min = np.sum(ag_ti_min)

def DTD_Ti(t, sum_Ti, tp = 0.3, a = 4, s = -1): 
    # default parameters are those used by Crocker et al for SN Ia
    # tp is in Gyrs
    def DTD_arbitrary(t): 
        return ((t/tp)**a)/((t/tp)**(a-s)+1)
    A = sum_Ti / quad(DTD_arbitrary, 0, 13.6)[0]
    return A*DTD_arbitrary(t)

def test_DTD(t):
    return DTD_Ti(t, sum_aa_Ti_max)
# print(sum_aa_Ti_max)
# returned 20 Msun Ti total

def const_SFR(t):
    return 10e-8

x = 0.15 # fraction of binary CO WD mass per total init. mass
total_mass = 38499996 # total mass used in SeBa sample

def TOTAL_TI_RATE(t, DTD_fn, SFR_fn):
    def integrand(tp):
        if t >= tp:
            return DTD_fn(t-tp) * SFR_fn(t)
        else:
            return 0
    return quad(integrand, 0, 13.6)[0]

time_arr = np.linspace(0, 13.6, 100)
# dtd_arr = [test_DTD(time) for time in time_arr]
ti_rate_arr = [TOTAL_TI_RATE(time, test_DTD, const_SFR) for time in time_arr]

#plt.plot(time_arr, ti_rate_arr)
#plt.show()

# Try using the DTD from the data itself
# Maybe normalize it to total Ti produced from the sample
# Then scale the SFR to adjust for the Milky Way mass discrepancy



#############################################
# Function to sum over values of an array
# Returning an array with entries as sum up to that point 
# Update Aug 3: Normalized to total CO mass at each point 
def total_ti(ti_arr, wd1_pts_arr, wd2_pts_arr, co_norm = True): 
    # inputs must be numpy arrays for entrywise addition to work 
    # optional parameter determines if normalized to CO mass in mergers
    wd_mass_sum_arr = wd1_pts_arr[:,1] + wd2_pts_arr[:,1] 
    sum_ti = 0
    sum_co = 0 
    total = np.zeros(np.shape(ti_arr)[0]) 
    for i in range(np.shape(ti_arr)[0]): 
        sum_ti += ti_arr[i]
        sum_co += wd_mass_sum_arr[i]
        if co_norm: 
            total[i] = sum_ti / sum_co
        else:
            total[i] = sum_ti
    return total

# Finding total Ti44 produced over time 
aa_totalTi_max = total_ti(aa_ti_max, aa_wd1max_pts, aa_wd2max_pts) 
aa_totalTi_min = total_ti(aa_ti_min, aa_wd1min_pts, aa_wd2min_pts) 
ag_totalTi_max = total_ti(ag_ti_max, ag_wd1max_pts, ag_wd2max_pts) 
ag_totalTi_min = total_ti(ag_ti_min, ag_wd1min_pts, ag_wd2min_pts) 

###### Fits ######

# Model function 
def model(x, a, b, c, d): 
    return (a*x + b)*np.exp(-c*x) + d

# Fitting to model with curve_fit
initial_guess = (7e-8, -1e-4, 5e-4, 9e-4) 
aa_Ti_max_fit, cov1 = curve_fit(model, aa_times, aa_totalTi_max, p0 = initial_guess, absolute_sigma = True) 
aa_Ti_min_fit, cov2 = curve_fit(model, aa_times, aa_totalTi_min, p0 = initial_guess, absolute_sigma = True)
ag_Ti_max_fit, cov3 = curve_fit(model, ag_times, ag_totalTi_max, p0 = initial_guess, absolute_sigma = True) 
ag_Ti_min_fit, cov4 = curve_fit(model, ag_times, ag_totalTi_min, p0 = initial_guess, absolute_sigma = True)

# Exporting fitting parameters to a file
params = { 
        'aa_max': aa_Ti_max_fit, 
        'aa_min': aa_Ti_min_fit, 
        'ag_max': ag_Ti_max_fit, 
        'ag_min': ag_Ti_min_fit,
        'param': ['a','b','c','d']
} 
params_df = pd.DataFrame(params) 
params_df.set_index('param', inplace=True) 
#params_df.to_csv('rbf_interp_outp_params.txt', sep = ' ') 

# Linspace arrays for plotting 
aa_times_lin = np.linspace(np.amin(aa_times), np.amax(aa_times), 150) 
ag_times_lin = np.linspace(np.amin(ag_times), np.amax(ag_times), 150) 

# Functions for plotting 
def aa_TImax_fn(t): 
    return model(t, aa_Ti_max_fit[0], aa_Ti_max_fit[1], aa_Ti_max_fit[2], aa_Ti_max_fit[3]) 
def aa_TImin_fn(t): 
    return model(t, aa_Ti_min_fit[0], aa_Ti_min_fit[1], aa_Ti_min_fit[2], aa_Ti_min_fit[3]) 
def ag_TImax_fn(t): 
    return model(t, ag_Ti_max_fit[0], ag_Ti_max_fit[1], ag_Ti_max_fit[2], ag_Ti_max_fit[3]) 
def ag_TImin_fn(t): 
    return model(t, ag_Ti_min_fit[0], ag_Ti_min_fit[1], ag_Ti_min_fit[2], ag_Ti_min_fit[3]) 


################ Plots
# Plotting total Ti44 produced over time
# aa 
#plt.scatter(aa_times, aa_totalTi_max, color = 'Red', alpha = 0.5, label = 'He max') 
#plt.scatter(aa_times, aa_totalTi_min, color = 'Blue', alpha = 0.5, label = 'He min') 
#plt.plot(aa_times_lin, aa_TImax_fn(aa_times_lin), color = 'Red') 
#plt.plot(aa_times_lin, aa_TImin_fn(aa_times_lin), color = 'Blue') 
#plt.title("Total Ti44 produced per total CO (aa sample)") 
#plt.xlabel("Time (Myr)") 
#plt.ylabel("Ti44 mass (Msun)") 
#plt.legend() 
#plt.show()
# plt.savefig("../../Plots/rbf_interp_plots/results/aaTi_total") 
# plt.close("all") 
# ag
#plt.scatter(ag_times, ag_totalTi_max, color = 'Red', alpha = 0.5, label = 'He max') 
#plt.scatter(ag_times, ag_totalTi_min, color = 'Blue', alpha = 0.5, label = 'He min') 
#plt.plot(ag_times_lin, ag_TImax_fn(ag_times_lin), color = 'Red') 
#plt.plot(ag_times_lin, ag_TImin_fn(ag_times_lin), color = 'Blue') 
#plt.title("Total Ti44 produced per total CO (ag sample)") 
#plt.xlabel("Time (Myr)") 
#plt.ylabel("Ti44 mass (Msun)") 
#plt.legend() 
#plt.show()
#plt.savefig("../../Plots/rbf_interp_plots/results/agTi_total") 
#plt.close("all") 

