# Ti44 Analysi

## Input Data
A directory for tables and data pulled from outside sources and papers.

## Output Data & Plots
Where our codes will send tables and Python plots of analysis data to.

## Interpolation Code
The codes we've made to anayze the data.

### groupFunctions.py
This where our group kept any functions we found ourselves using multiple times within seperate codes.


### FindHeMass.py
Estimates the helium shell mass of each white dwarf in the SeBa data using the total mass of the star. It first checks if the mass is within 0.4 to 0.52 solar masses. If so, it will assign a mass using Zenati et al. The equation used is: 

![](https://latex.codecogs.com/svg.image?M_{He}=0.28-0.39M_{WD})

However, if the WD mass is not within this range, then it will use equation 9 from Lawlor and MacDonald:
$$log_{10}(M_{He})=a+b\*log_{10}(M_{WD})+c\*log_{10}(M_{WD})^2$$

Where $a,b,$ and $c$ are definded based on the metalicity of the white dwarf. Currently, we have assumed the the metalicity of the stars are all $z=0.01$. However, we are looking into the effects of having different metalicity values. The He shell masses are appended to the original data file and sent to /Output\_data.

### HeMassLinearInterp.py (deprecated)

An older code that was used to deal with an older issue where some unphysical results were appearing when the $log(M_{WD})$ was about $-0.3$. This is unused now that Zenati et al. was added to the FindHeMass.py.


### tiFromCoreMass.py (deprecated)

This code used the data from the Gronow paper and the Leung paper to created a nearest neighbor linear interpolation to esitmate the Ti44 mass from the core mass. This has been replaced by Johnny's RBF interpolation that also includes the He shell mass in it's interpolation.


### timeIntervalScaling.py

Using 100 random samples of each dataset, we first sort and find the interval between the merger times. We take the median interval for each sample and save it into the array allSampleMedians. We also create another array called allSampleMasses that finds the total mass for each system in the sample. One more array, called allNumbers, takes in the total number of systems in the sample.

Using this data, the code creates two plots. The first is the logged number of systems vs the interval median values. The second is the logged sample mass vs the interval medians. These plots are saved in /Plots/LoggedRandomSample.png.

### timeInterval.py

This program grabs and sorts the merger times of each system in the aa and ag datasets. It creates a plot of the intervals over time saved into Plots/IntervalHisto.png

### MassCompasrisonCode.py

This code was to check if the FindHeMass.py was working correctly. It created multiple plots of the He shell mass against WD mass with differeing metallicities to compare them to figure 9 of Lawlor and MacDonald (2006).

### SFR.py

This creates an plot of the estimated star formation rate from equation 2 in Croker et al. Saved into Plots/MilkyWay\_SFR.png

### ti\_interpolation.py 

Using tables 3-6 of Gronow et al. to interpolation a relation between the final abundances of He and Ti44. Uses a linear interpolation and saves that data into Interpolation Data/SeBa\_aa\_Ti\_interp.txt

### rbf\_interp/ & ti\_interp2d/

These two directories were use RBF and scipy's interp2d to interpolate a function of Ti44 from the He and WD mass.



