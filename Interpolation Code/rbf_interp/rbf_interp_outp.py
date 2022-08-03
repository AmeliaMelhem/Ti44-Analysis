
"""
JG 
Utilizing the most sensible RBF interpolation to output Ti/e+ data from the SeBa sample 
Using the shortened sample that arose from NANs in finding He mass 

Here, I have plots: 
e+ produced at each time (summing over which would yield total e+) 
and, total e+ produced at some time 

I got # of positrons from Ti44 mass with Amy's positronFromTi function 

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
""" 
Updates from Aug 3: 
Attempts to make relationship intensive by outputting Ti^44 mass...
In units of Ti^44 mass per stellar mass that produced said Ti^44 
Then, 
Plotting said data over time to potentially yield some fit 

Also, commenting out some extraneous blocks to make the relevant bits run faster 
""" 
####################


# includes ...
import sys
sys.path.append('../')
from groupFunctions import positronFromTi
from rbf_interp import * 
#import numpy as np (within rbf_interp) 
import pandas as pd 
import matplotlib.pyplot as plt


######### Importing Data ############

# Data from Gronow and Leung papers 
ti_data = np.loadtxt("../../Input Data/he_co_ti_dat.txt") 
pts = ti_data[:,0:2] # Helium and Core masses 
vals = ti_data[:,2] # Ti44 masses 

# Interpolating Ti mass function based on above data 
ti_interp = RBF_interp(pts, vals, func = "multiquadric", scale = 0, norm = True) 

# SeBa data 
aa_df = pd.read_csv("../../Output Data/noDashSeBa_aa_with_He.txt", delim_whitespace=True, index_col=False)
aa_df = aa_df.shift(periods=1, axis=1) 
ag_df = pd.read_csv("../../Output Data/noDashSeBa_ag_with_He.txt", delim_whitespace=True, index_col=False) 
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
""" 
Quick update Aug 3
Divided entrywise by mass that produced Ti44
in this case, (WD1_m + WD2_m)
Consider adding Helium masses to denominator? 

def mass_normalization(ti_arr, wd1_pts_arr, wd2_pts_arr): 
    # Takes in numpy arrays (from data above) 
    # assuming wd*_pts_arr is indexed like [He_mass, WD*_mass] 
    # and performs the following calculation entrywise: 
    Ti_mass = Ti_mass / (WD1_mass + WD2_mass) 
    wd_mass_sum = wd1_pts_arr[:,1] + wd2_pts_arr[:,1] 
    return ti_arr / wd_mass_sum

aa_ti_max = mass_normalization(aa_ti_max, aa_wd1max_pts, aa_wd2max_pts) 
aa_ti_min = mass_normalization(aa_ti_min, aa_wd1min_pts, aa_wd2min_pts) 
ag_ti_max = mass_normalization(ag_ti_max, ag_wd1max_pts, ag_wd2max_pts) 
ag_ti_min = mass_normalization(ag_ti_min, ag_wd1min_pts, ag_wd2min_pts) 

This appears to get a better picture for the plots that show Ti44 produced at each moment in time 
But doesn't serve to get the total Ti44 plots intensive
"""
#################

# Function to sum over values of an array
# Returning an array with entries as sum up to that point 
# Update Aug 3: Normalized to total CO mass at each point 
def total_arr(ti_arr, wd1_pts_arr, wd2_pts_arr): 
    # inputs are numpy arrays for entrywise addition to work correctly 
    wd_mass_sum_arr = wd1_pts_arr[:,1] + wd2_pts_arr[:,1] 
    sum_ti = 0
    sum_co = 0 
    total = np.zeros(np.shape(ti_arr)[0]) 
    for i in range(np.shape(ti_arr)[0]): 
        sum_ti += ti_arr[i]
        sum_co += wd_mass_sum_arr[i]
        total[i] = sum_ti / sum_co
    return total

# Finding total Ti44 produced over time 
aa_totalTi_max = total_arr(aa_ti_max, aa_wd1max_pts, aa_wd2max_pts) 
aa_totalTi_min = total_arr(aa_ti_min, aa_wd1min_pts, aa_wd2min_pts) 
ag_totalTi_max = total_arr(ag_ti_max, ag_wd1max_pts, ag_wd2max_pts) 
ag_totalTi_min = total_arr(ag_ti_min, ag_wd1min_pts, ag_wd2min_pts) 

# Finding positrons from Ti mass arrays 
aa_pos_max = np.array(positronFromTi(aa_ti_max)) 
aa_pos_min = np.array(positronFromTi(aa_ti_min)) 
ag_pos_max = np.array(positronFromTi(ag_ti_max))
ag_pos_min = np.array(positronFromTi(ag_ti_min)) 

# Finding total positrons produced over time 
aa_totalPos_max = total_arr(aa_pos_max, aa_wd1max_pts, aa_wd2max_pts) 
aa_totalPos_min = total_arr(aa_pos_min, aa_wd1min_pts, aa_wd2min_pts) 
ag_totalPos_max = total_arr(ag_pos_max, ag_wd1max_pts, ag_wd2max_pts) 
ag_totalPos_min = total_arr(ag_pos_min, ag_wd1min_pts, ag_wd2min_pts) 

