
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
dset = 3
match dset: 
    case 1: 
        a = None
        b = 13
    case 2: 
        a = 13
        b = None
    case 3: 
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

def fetch_ind(val, arr): 
    # finds index of arr such that arr[i] ~ val 
    # assuming arr is sorted and ascending  
    for i in range(len(arr)): 
        if val > arr[i]: 
            continue 
        else: 
            return i

def fetch_err(): 
    """ 
    returns an array with the %error between data/model
    """
    err = [] 
    for i in range(len(he_data)): 
        temp_he = np.delete(he_data, i, 0) 
        temp_co = np.delete(co_data, i, 0) 
        temp_ti = np.delete(ti_data, i, 0) 
        temp_fit_fn = interp2d(temp_he, temp_co, temp_ti, kind='linear')
        err.append(100*np.abs((ti_data[i] - temp_fit_fn(he_data[i], co_data[i])) / ti_data[i])) 
    return np.mean(err) 

print(fetch_err()) 
