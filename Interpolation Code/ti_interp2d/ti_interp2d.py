
"""
JG 
week of 7/11-15
using scipy to interpolate a 'function' from Ti, He, CO mass data
then porting said function to a large matrix of values 
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d 

# Gronow data occupies rows 0-12
# Leung data occupies rows 13-19
data = np.loadtxt("../../Input Data/he_co_ti_dat.txt") 

# 1 - Gronow
# 2 - Leung (produces warning with too small a sample) 
# 3 - Both
case = 3

if case == 1: 
    a = None 
    b = 13
elif case == 2: 
    a = 13
    b = None
elif case == 3: 
    a = None
    b = None

he_data = data[a:b,0] 
co_data = data[a:b,1] 
ti_data = data[a:b,2] 


fit_f = interp2d(he_data, co_data, ti_data, kind='linear') 
"""
scipy "interpolating function" object ~ non-portable
ie performs local interpolation at each point called
hence produces 0% error if known values are plugged in directly
"""

he_arr = np.linspace(np.amin(he_data), np.amax(he_data), 150) 
co_arr = np.linspace(np.amin(co_data), np.amax(co_data), 150) 
he, co = np.meshgrid(he_arr, co_arr) 

fit_t = fit_f(he_arr, co_arr) 
"""
matrix of approx. Ti mass values
evidently, columns are indexed by he_arr[col] 
and rows are indexed like co_arr[row] 
eg fit_t[3,6] == fit_f(he_arr[6], co_arr[3]) 
"""


def fetch_index(val, arr): 
    """
    finds index i of arr such that arr[i] ~ val
    assumes that arr is sorted and ascending
    which is true for the linspace arrays he_arr, co_arr
    """ 
    i = 0
    for i in range(len(arr)): 
        if arr[i] < val: 
            i += 1
        else: 
            return i 


"""
Now seek to populate an array, ti_model
with indices that allign with he_data, co_data
to both plot and test validity of the fit (ie find %error) 
ti_arr[i] = fit_t[fetch_index(co_data[i], co_arr), fetch_index(he_data[i], he_arr)] 
"""
ti_model = [] 
i = 0
for i in range(len(he_data)): 
    ti_model.append(fit_t[fetch_index(co_data[i], co_arr), fetch_index(he_data[i], he_arr)])


def fetch_err(dat_arr, mod_arr): 
    """ 
    returns an array with the %error between data/model
    """
    err = [] 
    i = 0
    for i in range(len(dat_arr)): 
        err.append(100*np.abs((mod_arr[i] - dat_arr[i]) / dat_arr[i])) 
    return err 

"""
print(fetch_err(ti_data, ti_model)) 
print("\n") 
print(np.mean(fetch_err(ti_data, ti_model))) 
"""

def ti_mass(he_mass, co_mass): 
    return fit_t[fetch_index(co_mass, co_arr), fetch_index(he_mass, he_arr)] 
