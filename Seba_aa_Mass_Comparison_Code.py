import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("C:\\Users\\Alexis Petty\\Desktop\\He-Abundance-Model\\noDashSeBa_aa_with_He.txt")
Mwd1=np.log10(data[:,3])
He_min_wd1=np.log10(data[:,7])
plt.plot(Mwd1, He_min_wd1,"ro")

He_max_wd1=np.log10(data[:,9])
plt.plot(Mwd1, He_max_wd1,"b*")

Mwd2=np.log10(data[:,4])
He_min_wd2=np.log10(data[:,8])
plt.plot(Mwd2, He_min_wd2,"ro")

He_max_wd2=np.log10(data[:,10])
plt.plot(Mwd2, He_max_wd2,"b*")



plt.title('WD-Mass VS He-Mass')
plt.legend(['W1min','W1max', 'W2min', 'W2max'])
plt.ylabel('He-Mass')
plt.xlabel('WD-Mass')
plt.savefig("Mass_Comparison_aa")

plt.show()