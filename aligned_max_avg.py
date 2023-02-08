import matplotlib.pyplot as plt
import numpy as np
import os
folder=str(input("enter the name of source folder: "))
folder1=str(input("enter the name of destination folder: "))
output=str(folder1)+"/"+str(folder)+"_avg.txt"
os.system("mkdir "+folder1)
filenames=os.listdir(folder)
len_fil=[]
for fil in filenames:
	i=0
	for line in open(folder+"/"+fil,"r"):
		i=i+1
		len_fil.append(i)
size=max(len_fil)
mid=int(size/2.0)

X=np.arange(0,2*size,1)
I=np.zeros(2*size)
V=np.zeros(2*size)
L=np.zeros(2*size)
PA=np.zeros(2*size)
for fil in filenames:
	c_i=[]
	c_v=[]
	c_l=[]
	c_p=[]

	for x in open(folder+"/"+fil,"r"):
		s=[float(r) for r in x.split()]
		c_i.append(float(s[1]))
#		c_v.append(float(s[2]))
#		c_l.append(float(s[3]))
#		c_p.append(float(s[4]))
	c_i=np.array(c_i)
#	c_v=np.array(c_v)
#	c_l=np.array(c_l)
	c_i=c_i-(c_i[0]+c_i[-1])/2.0
#	c_v=c_v-(c_v[0]+c_v[-1])/2.0
#	c_l=c_i-(c_l[0]+c_l[-1])/2.0
		
	i_max=np.where(c_i==max(c_i))[0]
	
	
	for j in range(0,len(c_i)):
		I[mid-i_max+j]=c_i[j]+I[mid-i_max+j]
#	for j in range(0,len(c_i)):
#		V[mid-i_max+j]=c_v[j]+V[mid-i_max+j]
#	for j in range(0,len(c_i)):
#		L[mid-i_max+j]=c_l[j]+L[mid-i_max+j]
#	for j in range(0,len(c_i)):
#		if abs(c_p[j])>0.0:
#			PA[mid-i_max+j]=abs(c_p[j])+PA[mid-i_max+j]
#		else:
#		PA[mid-i_max+j]=(c_p[j])+PA[mid-i_max+j]
#A=PA/float(len(filenames))
f=open(output,'w+')

k=0
for x in I:
	f.write(str(x)+"      "+str(V[k])+"       "+str(L[k])+"          "+str(PA[k])+"\n")
	k=k+1
	
fig=plt.figure()
#ax1=fig.add_axes([0.1,0.1,0.9,0.3],ylim=(-90,90),xlabel='time in units of 15 micro-sec',ylabel='avg of absolute of value PA')


plt.plot(X,I,c='b',label='Intensity')
#ax2.plot(X,V,c='r',label='circular polarisation component')
#ax2.plot(X,L,c='g',label='linear polarisation component').plot(X,PA)
plt.legend()
plt.show()








	
	
	
	




