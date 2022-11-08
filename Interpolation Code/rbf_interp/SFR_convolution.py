"""
JG
Using the fits for the Ti/CO mass function
In addition to the mass fraction x (i.e. prod CO mass / total formed mass)
And an SFR which will for now be held constant at 10Msun per year 
To find the total rate of Ti44 produced due to SN 1A 
""" 

from rbf_interp_fits import * 

from scipy.integrate import quad
import matplotlib.pyplot as plt

# gives access to functions of form a*_TImax/min_fn
# (at+b)e^(-ct) + d
# which outputs Ti produced per CO mass 
# serving as our 'DTD' 

# Pos per Ti44 mass rate: 2.7e55 per solar mass of Ti44
x = 0.1488 # fraction of binary CO WD mass per total init. mass

def const_SFR(t): 
    return 10

def DTD(t, tp = 0.3, a = 4, s = -1): 
    # delay time distribution
    # default values are those chosen by Crocker et al for SN Ia 
    # with tp in Gyrs
    return ((t/tp)**a)/((t/tp)**(a-s)+1)

def TOTAL_TI_RATE(t, Ti_fn, SFR_fn): 
    def integrand(tp): 
        if t >= tp: 
            return Ti_fn(t-tp)*SFR_fn(tp)
        else: 
            return 0
    return quad(integrand, 0, 13.6*(10**9))[0]

time_arr = np.linspace(0, 13.6*(10**9), 100) 
ti_rate_arr = [TOTAL_TI_RATE(time, DTD, const_SFR) for time in time_arr] 

#plt.plot(time_arr, ti_rate_arr)
plt.plot(time_arr, DTD(time_arr))
plt.show()