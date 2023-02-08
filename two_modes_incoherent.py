#############   Code to simulate incoherent superposition of two elliptically polarized waves   ###############33

import matplotlib.pyplot as plt
import numpy as np
import math

#############  Function to generate stokes parameters for given amplitude, position angle and fractional polarization #####
def stokes(x,x0,sigma,f_l,f_v,psi,a):
	I1=[]
	Q1=[]
	U1=[]
	V1=[]	
	for r in x:
		value=a1*np.exp(-(r-x0)**2/(2*(sigma)**2))
		I1.append(value)
		Q1.append(f_l*value*math.cos(2*psi*np.pi/180.))
		U1.append(f_l*value*math.sin(2*psi*np.pi/180.))
		V1.append(f_v*value)
	I1=np.array(I1)
	V1=np.array(V1)
	U1=np.array(U1)
	Q1=np.array(Q1)
	L1=np.sqrt(Q1*Q1+U1*U1)
	return(I1,Q1,U1,V1,L1)

###### Function to generate position angle after incoherent superposition   ######  
	
def PPA(l1,l2,psi1,psi2):
	psi=[]
	for i in range(len(l1)):
		if(l1[i]>l2[i]):
			psi.append(psi1)
		else:
			psi.append(psi2)
	print(psi)
	return(psi)	

########   Function to generate polarized micropulse train  ###################
	
def stokes_micro(x,sep,sigma,f_l,f_v,a):
	I1=np.zeros(len(x))
	Q1=np.zeros(len(x))
	U1=np.zeros(len(x))
	V1=np.zeros(len(x))
	psi1=np.zeros(len(x))
	num_micro=int(len(x)/sep)
	for i in range(num_micro):
		k=0	
		for r in x:
			value=a*np.exp(-(r-i*sep)**2/(2*(sigma)**2))
			I1[k]=I1[k]+value
			Q1[k]=Q1[k]+f_l*value
			U1[k]=U1[k]-f_l*value
			V1[k]=V1[k]+f_v*value
			k=k+1
				
	I1=np.array(I1)
	V1=np.array(V1)
	U1=np.array(U1)
	Q1=np.array(Q1)
	L1=np.sqrt(Q1*Q1+U1*U1)
	return(I1,Q1,U1,V1,L1,psi1)

	
x=np.arange(600)

sep_micro=40.
sigma_micro=10.
f_l=0.9
f_v=-0.1

a_micro=0.8
#Im,Qm,Um,Vm,Lm,psim=stokes_micro(x,sep_micro,sigma_micro,f_l,f_v,a_micro)


#########  Parameters of two superpositing components  ####################

x01=380.
sigma1=40.
f_l=0.9
f_v=0.1
psi1=-30.0

a1=2.0
I1,Q1,U1,V1,L1=stokes(x,x01,sigma1,f_l,f_v,psi1,a1)


x02=250.
sigma2=100.
f_l=0.9
f_v=0.1
psi2=60.
a2=1.0
I2,Q2,U2,V2,L2=stokes(x,x02,sigma2,f_l,f_v,psi2,a2)
I=I1+I2
Q=Q1+Q2
U=U1+U2
V=V1+V2
L=np.sqrt(Q*Q+U*U)
psi=PPA(L1,L2,psi1,psi2)
psi1=np.ones(len(x))*psi1
psi2=np.ones(len(x))*psi2

##############    Plotting the results  #################################

fig=plt.figure(figsize=(5,5),dpi=100)
ax1=fig.add_axes([0.15,0.13,0.82,0.3],xlabel='Time',ylabel='PPA (degrees)')
ax1.set_ylim([-90,90])
ax2=fig.add_axes([0.15,0.42,0.82,0.5],ylabel='Stokes parameters')
ax2.set_xticklabels([])
ax2.plot(x,I,c='k',label='Stokes-I')
ax2.plot(x,L,c='g',label='Linear polarisation')
ax2.plot(x,V,c='r',label='Circular polarisation')
ax2.plot(x,I1,c='k',alpha=0.4,ls='dashed')
ax2.plot(x,L1,c='g',alpha=0.4,ls='dashed')
ax2.plot(x,V1,c='r',alpha=0.4,ls='dashed')
ax2.plot(x,I2,c='k',alpha=0.4,ls='dotted')
ax2.plot(x,L2,c='g',alpha=0.4,ls='dotted')
ax2.plot(x,V2,c='r',alpha=0.4,ls='dotted')
ax1.plot(x,psi,c='k')
ax1.plot(x,psi1,c='k',ls='dashed',alpha=0.4)
ax1.plot(x,psi2,c='k',ls='dotted',alpha=0.4)
ax1.grid()
ax2.grid(which='both')
ax2.legend(loc=2,prop = {'size' : 8})
plt.savefig('Incoherent_example.png')
