from rbf_interp_outp import *
import matplotlib.pyplot as plt
import numpy as np

###################################################Nature_paper_DISK_SFR##########
integrand = []
for i in range (len(ag_ti_max)):
    time = 1e-3*ag_times[i]                            #convert time from megayear to gigayear
    A = -4.06*10**(-2)
    B = 0.331
    C = 0.338
    D = 0.771
    z = (np.sqrt(-(time-28)*time)-time)/time                           #convert from time to redshift z using formula from Carmel et al https://arxiv.org/pdf/gr-qc/0506079.pdf
    integrand.append(ag_ti_min[i]*((10**(A*(z**2)+(B*z)+C))-D))           #store ti44 value produced at z value, use ag_ti_max[i] for max ti44 rate


##########arrays to convert time from megayear to year#######################################################
timed_rate = [None]*len(integrand)
timed_time = [None]*len(integrand)
for i in range(len(integrand)):
   timed_rate[i]= 0
   timed_time[i] = 1e+6*(ag_times[i])
   for j in range(i):
      timed_rate[i] += integrand[j]      #store ti44 production per year

#####convert lists to numpy arrays
timed_rate = np.array(timed_rate) 
timed_time = np.array(timed_time)
timed_rate = timed_rate/timed_time          

sum = np.sum(integrand)                       #find total ti44 produced by summing over all time steps
max_time = 1e+6*np.max(ag_times)     #find the max time of mergers and convert to mega years
rate = sum/(max_time)                           #find the current ti44 rate of sample


##########convert the current ti44 rate of sample to the current ti44 rate of milky way disk############################
mass_ratio = 3.7e+10/38499996
milky_way_rate = rate*mass_ratio
print("The ti44 production rate for the milky way disk  = ", milky_way_rate, "solarmass/yr")


###################plot the ti44 rate for history of milky way########################################
milky_way_timed_rate = timed_rate*mass_ratio
plt.plot(ag_times, milky_way_timed_rate, color = 'r', label = 'Crocker et al (disk)')


###############################################################SFR_exp+0.12t###################################
integrand = []
for i in range (len(ag_ti_max)):
    time = 1e-3*ag_times[i]                            #convert time from megayear to gigayear
    integrand.append(ag_ti_min[i]*(np.exp(0.12*time)))     #store ti44 value produced at time value, use ag_ti_max[i] for max ti44 rate

######arrays to convert time from megayear to year#######################################################
timed_rate = [None]*len(integrand)
timed_time = [None]*len(integrand)
for i in range(len(integrand)):
   timed_rate[i]= 0
   timed_time[i] = 1e+6*(ag_times[i])
   for j in range(i):
      timed_rate[i] += integrand[j]      ##store ti44 production per year

#####convert lists to numpy arrays
timed_rate = np.array(timed_rate) 
timed_time = np.array(timed_time)
timed_rate = timed_rate/timed_time          

sum = 3.7e+10/(6.683e+9)*np.sum(integrand)    #find total ti44 produced by summing over all time steps and normalizing SFR
max_time = 1e+6*np.max(ag_times)     #find the max time of mergers and convert to mega years
rate = sum/(max_time)                           #find the current ti44 rate of sample



##########convert the current ti44 rate of sample to the current ti44 rate of milky way disk#############################
mass_ratio = 3.7e+10/38499996
milky_way_rate = rate*mass_ratio
print("The ti44 production rate for the milky way disk  = ", milky_way_rate, "solarmass/yr")


###################plot the ti44 rate for history of milky way########################################
milky_way_timed_rate = timed_rate*mass_ratio
plt.plot(ag_times, milky_way_timed_rate, color = 'green', label = 'exp(0.12t)')





##################################################Aexp+exp#################
integrand = []
for i in range (len(ag_ti_max)):
    time = 1e-3*ag_times[i]                 #convert time from megayear to gigayear
    A = 3*(10**(-9))
    lamb = 2
    gamma = 0.089
    integrand.append(ag_ti_min[i]*(A*np.exp(time*lamb)+np.exp(gamma*time)))     #store ti44 value produced at time value, use ag_ti_max[i] for max ti44 rate

######arrays to convert time from megayear to year#######################################################
timed_rate = [None]*len(integrand)
timed_time = [None]*len(integrand)
for i in range(len(integrand)):
   timed_rate[i]= 0
   timed_time[i] = 1e+6*(ag_times[i])
   for j in range(i):
      timed_rate[i] += integrand[j]      ##store ti44 production per year

#####convert lists to numpy arrays
timed_rate = np.array(timed_rate) 
timed_time = np.array(timed_time)
timed_rate = timed_rate/timed_time          

sum = 3.7e+10/(8.225e+11)*np.sum(integrand)    #find total ti44 produced by summing over all time steps and normalizing SFR
max_time = 1e+6*np.max(ag_times)                     #find the max time of mergers and convert to mega years
rate = sum/(max_time)                                           #ind the current ti44 rate of sample



##########convert the current ti44 rate of sample to the current ti44 rate of milky way disk#############################
mass_ratio = 3.7e+10/38499996
milky_way_rate = rate*mass_ratio
print("The ti44 production rate for the milky way disk  = ", milky_way_rate, "solarmass/yr")

###################plot the ti44 rate for history of milky way########################################
milky_way_timed_rate = timed_rate*mass_ratio
plt.plot(ag_times, milky_way_timed_rate, color = 'b', label = 'A exp('+str(chr(955))+str(chr(964))+')+exp('+str(chr(947))+str(chr(964))+')')



######################################################justandjahreiss########################
integrand = []
for i in range (len(ag_ti_max)):
    time = 1e-3*ag_times[i]                          #convert time from megayear to gigayear
    mean = 3.8
    t0 = 5.6
    t1 = 8.2
    tn = 9.9
    numerator = (time + t0)*tn**3
    denominator = (time**2+t1**2)**2
    integrand.append(ag_ti_min[i]*((mean*numerator)/denominator))               #store ti44 value produced at time value, use ag_ti_max[i] for max ti44 rate
    
######arrays to convert time from megayear to year#######################################################
timed_rate = [None]*len(integrand)
timed_time = [None]*len(integrand)
for i in range(len(integrand)):
   timed_rate[i]= 0
   timed_time[i] = 1e+6*(ag_times[i])
   for j in range(i):
      timed_rate[i] += integrand[j]      #store ti44 production per year


#####convert lists to numpy arrays
timed_rate = np.array(timed_rate) 
timed_time = np.array(timed_time)
timed_rate = timed_rate/timed_time          

sum = 3.7e+10/(4.823e+10)*np.sum(integrand)            #find total ti44 produced by summing over all time steps and normalizing SFR
max_time = 1e+6*np.max(ag_times)                             #find the max time of mergers and convert to mega years
rate = sum/(max_time)                                                   #find the current ti44 rate of sample



##########convert the current ti44 rate of sample to the current ti44 rate of milky way disk#############################
mass_ratio = 3.7e+10/38499996
milky_way_rate = rate*mass_ratio
print("The ti44 production rate for the milky way disk  = ", milky_way_rate, "solarmass/yr")


###################plot the ti44 rate for history of milky way########################################
milky_way_timed_rate = timed_rate*mass_ratio
plt.plot(ag_times, milky_way_timed_rate, color = 'purple', label = 'Just&Jahreiss')



#####################final settings for plot################################################################
plt.ylim(1e-9,3e-4)
plt.xlim(0,13499)
plt.xlabel("Time (Myr)", fontsize = 16)
plt.ylabel("$^{44}$Ti Rate ($\mathrm{M}_{\odot}/yr$)", fontsize = 16)
plt.yscale("log")
plt.legend()
plt.savefig("allSFRsdisk",bbox_inches='tight')
plt.close("all")


