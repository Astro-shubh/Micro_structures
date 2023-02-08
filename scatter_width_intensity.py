############## Used to plot height versus width of individual micropulses stored in a directory  ######################

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
dir=str(input("enter directory name: "))

widths1=[]
intensity=[]

############## Getting information of individual micropulses   ##########################

for fil in os.listdir(dir):
	I=[]
	for line in open(dir+"/"+fil,"r"):
		s=[float(r) for r in line.split()]
		I.append(s[1])
	mean=np.mean(I)
	energy=np.sum(I)

	base=np.ones(len(I))
	I_base=(I[-1]+I[-2]+I[0]+I[1])/4.0
	base=base*I_base
	I=I-base
	max1=np.amax(I)
	intensity.append(max1)
	a_i=np.correlate(I,I,'full')
	acf_min=np.ones(len(a_i))
	min_acf=np.amin(a_i)
	acf_min=acf_min*min_acf
	a_i=a_i-acf_min
	maximum=np.amax(a_i)
	k=np.where(a_i==maximum)
	for i in range(0,len(I)):
		if a_i[i+k[0]]<maximum/2.0:
			p=i+float((a_i[i+k[0]-1]-maximum/2.0)/(a_i[i+k[0]-1]-a_i[i+k[0]]))-1
			widths1.append(2.*p)
			break;
	
	
widths1=np.array(widths1)*5.12            #########  5.12 is resolution of the time series. Please use the resolution of your observations here
res = stats.pearsonr(widths1,intensity)
print(res)

###################  Printing Basic statistics of the micropulses  ###################################

print('Mean of widths')
print(np.mean(widths1))
print('Median of widths')
print(np.median(widths1))

######################  Scatter plot of Intensity versus width  ####################################

#fig=plt.figure(figsize=(12,8),dpi=256)
plt.xlabel('Width (us)',fontsize=15)
plt.ylabel('Peak intensity (arbitrary units)',fontsize=15)
plt.yscale('log')
plt.scatter(widths1,intensity)
plt.legend()
plt.grid(which='both',alpha=0.5)
plt.show()
