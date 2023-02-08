import os
import numpy as np
import matplotlib.pyplot as plt
dir=str(input("enter directory name: "))
bin_size=(input("enter size: "))
width=[]
j=0
for fil in os.listdir(dir):
	I=[]
	for line in open(dir+"/"+fil,"r"):
		s=[float(r) for r in line.split()]
		I.append(s[1])
	mean=np.mean(I)
	mn_off=(I[0]+I[-1]+I[1]+I[-2])/4.0
	base=np.ones(len(I))
	base=base*mn_off
	I=I-base
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
			width.append(2*p)
			break;
	
	j=j+1
width=np.array(width)*5.12
avg=np.mean(width)
bins=np.arange(0,max(width)+2,bin_size)
print('avg width :'+str(avg))
#bins=[]
#bn=0
#while bn < max(width)+1:
#	bn=1+bn+int(bn*8.0/max(width))*0.5
#	bins.append(bn)
#print("avg width is: "+str(avg))

#plt.title('histogram (bin_size):'+str(bin_size)+" "+str(dir)+' with '+str(j)+' pulses, avg pulse width: '+str(avg),fontsize=18)
fig=plt.figure(figsize=(12,8),dpi=256)
plt.xlabel('width ('+r'$\mu$ s)',fontsize=15)
plt.xlim(-20.0,400.0)
plt.ylabel('number of micropulses',fontsize=15) 
plt.ylim(0.0,100.0)
plt.hist(width,bins=bins,rwidth=1.0,color='g',alpha=0.8)
plt.grid(which='both',alpha=0.4)
plt.savefig('widths.png')

