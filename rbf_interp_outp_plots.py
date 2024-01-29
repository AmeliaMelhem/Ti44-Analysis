from rbf_interp_outp import * 
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots (1)

############ Plots ############


############ Plotting Specific Ti44 Rate Over Time##############

####ag#######
ax.plot(ag_times, ag_totalTi_max, 'k-', alpha = 1, label = 'max $^{44}$Ti')
ax.plot(ag_times, ag_totalTi_min, 'k--', alpha = 1, label = 'min $^{44}$Ti')
plt.xlabel("Time (Myr)", fontsize = 16) 
plt.ylabel("Specific $^{44}$Ti Rate", fontsize = 16) 
plt.xlim(0,13499)
plt.tight_layout()
plt.legend(loc = 'lower right') 
plt.savefig("ti_produced_ag") 
plt.close("all") 

