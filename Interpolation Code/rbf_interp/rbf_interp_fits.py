"""
JG 
The purpose of this file is to isolate the core results from rbf_interp_outp.py 
So that they can be called upon later, 
without the extraneous, time-intensive computation required getting to this point 

It includes five functions, 
One generic model, 
And four fit to each sample

The functions resemble the form: 
    Ti/CO(t) ~ (a*x + b)*exp(-c*x) + d
And represent the impulse response of Ti produced (Ti mass per stellar mass) 
from a single burst of star formation 

Concerns: 
There is a point, near the end of the sample's domain (at about 14000 Myr) 
where the model begins to flatten, while the data continues a linear descent 
so this might produce an overestimate after folding in the SFR 
However, 
This occurs just near the current age of the Milky Way 
So we won't be considering times beyond this domain, thus it shouldn't matter too much 
""" 

import numpy as np
import matplotlib.pyplot as plt

params = np.loadtxt('rbf_interp_outp_params.txt', skiprows=1, usecols=(1,2,3,4)) 

aa_max = params[:,0] 
aa_min = params[:,1] 
ag_max = params[:,2] 
ag_min = params[:,3] 

def model(x, a, b, c, d): 
    return (a*x + b)*np.exp(-c*x) + d

def aa_TImax_fn(t): 
    return model(t, aa_max[0], aa_max[1], aa_max[2], aa_max[3]) 
def aa_TImin_fn(t): 
    return model(t, aa_min[0], aa_min[1], aa_min[2], aa_min[3]) 
def ag_TImax_fn(t): 
    return model(t, ag_max[0], ag_max[1], ag_max[2], ag_max[3]) 
def ag_TImin_fn(t): 
    return model(t, ag_min[0], ag_min[1], ag_min[2], ag_min[3]) 
