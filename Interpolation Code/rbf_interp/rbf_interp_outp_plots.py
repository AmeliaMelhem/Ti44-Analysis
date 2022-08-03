""" 
JG 
Associated plots with rbf_interp_outp.py file 
In attempt to find intensive relationship for M_Ti/M_CO/time
In the limit of a single burst of start formation at t=0
After which, we'll try folding in the SFR to get the total rate 
""" 

from rbf_interp_outp import * 

############ Plots ############
"""
# Plotting Ti44 produced at each moment in time 
# aa
plt.scatter(aa_times, aa_ti_max, color = 'Red', label = 'He max') 
plt.scatter(aa_times, aa_ti_min, color = 'Blue', label = 'He min') 
plt.title("Ti44 produced at each time (aa sample)") 
plt.xlabel("Time (Myr)") 
plt.ylabel("Ti44 mass (Msun)") 
plt.legend() 
plt.savefig("../../Plots/rbf_interp_plots/results/aaTi") 
plt.close("all") 
# ag 
plt.scatter(ag_times, ag_ti_max, color = 'Red', label = 'He max') 
plt.scatter(ag_times, ag_ti_min, color = 'Blue', label = 'He min') 
plt.title("Ti44 produced at each time (ag sample)") 
plt.xlabel("Time (Myr)") 
plt.ylabel("Ti44 mass (Msun)") 
plt.legend() 
plt.savefig("../../Plots/rbf_interp_plots/results/agTi") 
plt.close("all") 
"""

# Plotting total Ti44 produced over time
# aa 
plt.scatter(aa_times, aa_totalTi_max, color = 'Red', label = 'He max') 
plt.scatter(aa_times, aa_totalTi_min, color = 'Blue', label = 'He min') 
plt.title("Total Ti44 produced per total CO (aa sample)") 
plt.xlabel("Time (Myr)") 
plt.ylabel("Ti44 mass (Msun)") 
plt.legend() 
plt.savefig("../../Plots/rbf_interp_plots/results/aaTi_total") 
plt.close("all") 
# ag
plt.scatter(ag_times, ag_totalTi_max, color = 'Red', label = 'He max') 
plt.scatter(ag_times, ag_totalTi_min, color = 'Blue', label = 'He min') 
plt.title("Total Ti44 produced per total CO (ag sample)") 
plt.xlabel("Time (Myr)") 
plt.ylabel("Ti44 mass (Msun)") 
plt.legend() 
plt.savefig("../../Plots/rbf_interp_plots/results/agTi_total") 
plt.close("all") 

"""
# Plotting positrons produced at each moment in time 
# aa
plt.scatter(aa_times, aa_pos_max, color = 'Red', label = 'He max') 
plt.scatter(aa_times, aa_pos_min, color = 'Blue', label = 'He min') 
plt.title("e+ produced at each time (aa sample)") 
plt.xlabel("Time (Myr)") 
plt.ylabel("Number of positrons") 
plt.legend() 
plt.savefig("../../Plots/rbf_interp_plots/results/aaPos") 
plt.close("all") 
# ag 
plt.scatter(ag_times, ag_pos_max, color = 'Red', label = 'He max') 
plt.scatter(ag_times, ag_pos_min, color = 'Blue', label = 'He min') 
plt.title("e+ produced at each time (ag sample)") 
plt.xlabel("Time (Myr)") 
plt.ylabel("Number of positrons") 
plt.legend() 
plt.savefig("../../Plots/rbf_interp_plots/results/agPos") 
plt.close("all") 
"""

# Plotting total postitrons produced over time 
# aa 
plt.scatter(aa_times, aa_totalPos_max, color = 'Red', label = 'He max') 
plt.scatter(aa_times, aa_totalPos_min, color = 'Blue', label = 'He min')
plt.title("Total positrons produced per total CO (aa sample)") 
plt.xlabel("Time (Myr)") 
plt.ylabel("Number of positrons") 
plt.legend() 
plt.savefig("../../Plots/rbf_interp_plots/results/aaPos_total") 
plt.close("all") 
# ag
plt.scatter(ag_times, ag_totalPos_max, color = 'Red', label = 'He max') 
plt.scatter(ag_times, ag_totalPos_min, color = 'Blue', label = 'He min')
plt.title("Total positrons produced per total CO (ag sample)") 
plt.xlabel("Time (Myr)") 
plt.ylabel("Number of positrons") 
plt.legend() 
plt.savefig("../../Plots/rbf_interp_plots/results/agPos_total") 
plt.close("all")
