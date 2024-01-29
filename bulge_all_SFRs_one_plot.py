from rbf_interp_outp import *
import matplotlib.pyplot as plt
import numpy as np
from numpy import exp

###################################################Nature_paper_BULGE_SFR##########
integrand = []
for i in range (len(ag_ti_max)):                                                 
    time = 1e-3*ag_times[i]                                                        #convert time from megayear to gigayear
    A = -2.62*10**(-2)
    B = 0.384
    C = 8.4*10**(-2)
    D = 3.254
    z = (np.sqrt(-(time-28)*time)-time)/time                                #convert from time to redshift z using formula from Carmel et al https://arxiv.org/pdf/gr-qc/0506079.pdf 
    integrand.append(ag_ti_min[i]*((10**(A*(z**2)+(B*z)+C))-D))        #store ti44 value produced at z value, use ag_ti_max[i] for max ti44 rate


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


##########convert the current ti44 rate of sample to the current ti44 rate of milky way bulge#############################
mass_ratio = 1.6e+10/38499996   
milky_way_rate = rate*mass_ratio
print("The ti44 production rate for the milky way bulge  = ", milky_way_rate, "solarmass/yr")


###################plot the ti44 rate for history of milky way########################################
milky_way_timed_rate = timed_rate*mass_ratio
plt.plot(ag_times, milky_way_timed_rate, 'm-', label = 'Crocker et al (bulge)')




###################################################K06_BULGE_SFR#########################

file = open('K06timesandrates.csv', 'r')  #open data file for K06
data_in = file.readlines()[:]  #read in data
file.close
sfrtime = []
rate = []
for line in data_in:     #store time and rate from data in lists
  sp = line.split()

  rate.append(float(sp[1]))
  sfrtime.append(float(sp[0]))



###########lists to store times that match with ag_times#############################
realtime = []
realrate = []
integrand = []





###########find times that match with ag_times##########################
count = 0
for i in range (len(ag_ti_max)):
    time = 1e-3*ag_times[i]                                 #convert time from megayear to gigayear
    for j in range(i, len(sfrtime)):
      diff = (ag_times[i]/1000) - sfrtime[j]
      if diff < 0.001:
        count = count + 1
        realtime.append(sfrtime[j])
        realrate.append(10**(4*rate[j])) #using 2kpc as distance
        break


##########store ti44 value per time step##############################
for i in range (len(ag_ti_max)):
    integrand.append(ag_ti_min[i]*realrate[i]) #use ag_ti_max[i] for max ti44 rate


timed_rate = [None]*len(integrand)
timed_time = [None]*len(integrand)
for i in range(len(integrand)):
   timed_rate[i]= 0
   timed_time[i] = 1e+6*(ag_times[i])
   for j in range(i):
      timed_rate[i] += integrand[j]           ##store ti44 production per year


#####convert lists to numpy arrays
timed_rate = np.array(timed_rate)
timed_time = np.array(timed_time)
timed_rate = timed_rate/timed_time

sum = np.sum(integrand)                       #find total ti44 produced by summing over all time steps
max_time = 1e+6*np.max(ag_times)     #find the max time of mergers and convert to mega years
finalrate = sum/(max_time)                    #find the current ti44 rate of sample


##########convert the current ti44 rate of sample to the current ti44 rate of milky way bulge#############################
mass_ratio = 1.6e+10/38499996
milky_way_rate = finalrate*mass_ratio
print("The ti44 production rate for the milky way bulge  = ", milky_way_rate, "solarmass/yr")



###################plot the ti44 rate for history of milky way########################################
milky_way_timed_rate = timed_rate*mass_ratio
plt.plot(ag_times, milky_way_timed_rate, 'y-', label = 'K06')



################################################CL04_BULGE_SFR#################

file = open('CL04timesandrates.csv', 'r')  #open data file for CL04
data_in = file.readlines()[:]  #read in data
file.close
sfrtime = []
rate = []
for line in data_in:     #store time and rate from data in lists
  sp = line.split()

  rate.append(float(sp[1]))
  sfrtime.append(float(sp[0]))


###########lists to store times that match with ag_times#############################
realtime = []
realrate = []
integrand = []


###########find times that match with ag_times##########################
count = 0
for i in range (len(ag_ti_max)):
    time = 1e-3*ag_times[i]                                    #convert time from megayear to gigayear
    for j in range(i, len(sfrtime)):
      diff = (ag_times[i]/1000) - sfrtime[j]
      if diff < 0.001:
        count = count + 1
        realtime.append(sfrtime[j])
        realrate.append(4*rate[j])       #using 2kpc as distance
        break


##########store ti44 value per time step##########################
for i in range (len(ag_ti_max)):
    integrand.append(ag_ti_min[i]*realrate[i])       #use ag_ti_max[i] for max ti44 rate


timed_rate = [None]*len(integrand)
timed_time = [None]*len(integrand)
for i in range(len(integrand)):
   timed_rate[i]= 0
   timed_time[i] = 1e+6*(ag_times[i])
   for j in range(i):
      timed_rate[i] += integrand[j]           #store ti44 production per year


#####convert lists to numpy arrays
timed_rate = np.array(timed_rate)
timed_time = np.array(timed_time)
timed_rate = timed_rate/timed_time

sum = np.sum(integrand)                         #find total ti44 produced by summing over all time steps
max_time = 1e+6*np.max(ag_times)       #find the max time of mergers and convert to mega years
finalrate = sum/(max_time)                       #find the current ti44 rate of sample


##########convert the current ti44 rate of sample to the current ti44 rate of milky way bulge#############################
mass_ratio = 1.6e+10/38499996
milky_way_rate = finalrate*mass_ratio
print("The ti44 production rate for the milky way bulge  = ", milky_way_rate, "solarmass/yr")

###################plot the ti44 rate for history of milky way########################################
milky_way_timed_rate = timed_rate*mass_ratio
plt.plot(ag_times, milky_way_timed_rate, 'k-', label = 'CL04')


######################################Bernardetal_BULGE_SFR###############
time = 13.4
z =np.sqrt((28/time)-1)-1
g_prime = (0.282)*exp(0.283*z)          #SFR 


integrand = []
for i in range (len(ag_ti_max)):                                                
    time = 1e-3*ag_times[i]
    #z =np.sqrt((28/time)-1)-1
    z = (np.sqrt(-(time-28)*time)-time)/time                               #convert from time to redshift z using formula from Carmel et al https://arxiv.org/pdf/gr-qc/0506079.pdf 
    integrand.append(ag_ti_min[i]*0.282*exp(0.283*z))           #store ti44 value produced at z value, use ag_ti_max[i] for max ti44 rate



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

sum = np.sum(integrand)                       #find total ti44 produced by summing over all time steps
max_time = 1e+6*np.max(ag_times)     #find the max time of mergers and convert to mega years
rate = sum/(max_time)                           #find the current ti44 rate of sample


##########convert the current ti44 rate of sample to the current ti44 rate of milky way bulge#############################
mass_ratio = 1.6e+10/38499996   
milky_way_rate = rate*mass_ratio
print("The ti44 production rate for the milky way bulge  = ", milky_way_rate, "solarmass/yr")


###################plot the ti44 rate for history of milky way########################################
milky_way_timed_rate = timed_rate*mass_ratio
plt.plot(ag_times, milky_way_timed_rate, 'b-', label = 'Bernard et al')



#####################final settings for plot################################################################
plt.ylim(1e-9, 3e-4)
plt.xlim(0, 13499)
plt.xlabel("Time (Myr)", fontsize = 16)
plt.ylabel("$^{44}$Ti Rate ($\mathrm{M}_{\odot}/yr$)", fontsize = 16)
plt.yscale("log")
plt.legend()
plt.savefig("allSFRsbulge",bbox_inches='tight')
plt.close("all")

