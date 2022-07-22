
from rbf_interp import * 
import matplotlib.pyplot as plt

data = np.loadtxt("../../Input Data/he_co_ti_dat.txt") 
pts = data[:,0:2] # Helium and Core masses
vals = data[:,2] # Ti44 masses

ti_interp = RBF_interp(pts, vals, func = "multiquadric", norm = False)


print(ti_interp.err()) 
print(ti_interp.scale) 

ti_interp.optimize() 

print(ti_interp.err()) 
print(ti_interp.scale) 
