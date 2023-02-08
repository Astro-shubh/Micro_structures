import struct
import matplotlib.pyplot as plt
import numpy as np
filename='fullDM_filtered_DM_2.975.dat_part2'
fn=open(filename,'rb')
write_directory='part2'

########## Parameters of time series   ###################

del_t=0.00000512          #  sampling time interval in seconds
period=0.2530587         #  Period of pulsar

##########  Reading data   ###############################

noise=[]

while True:
        num=fn.read(4)
        if num==b'':
                break;
        noise.append(struct.unpack('f',num)[0])


############  Downsampling  ############################       
df=1
i=0
sum=0
new_t=[]

for x in noise:
	sum=sum+x
	
	if(i%df==0):
		new_t.append(sum/float(df))
		sum=0
	i=i+1

noise=np.array(new_t)

##########   Folding   ##################################

del_t=df*del_t
size=len(noise)
p=int(period/del_t)
phase=np.arange(p)/float(p)
I1=np.ones(p)
I=[]
cycle=0
n1=0
plt.ion()
fig = plt.figure()

profile=np.zeros(p)
for i in range(len(noise)):
	j=int(((i*del_t)/period-int((i*del_t)/period))*p)
	profile[j]=profile[j]+noise[i]
profile=profile/(float(len(noise))/p)
plt.plot(phase,profile)
plt.show()

############  Getting ON and OFF winodw ###################

start=float(input('Enter ON pulse phase start\n'))
end=float(input('Enter ON pulse phase end\n'))

off_start=float(input('Enter OFF pulse phase start\n'))
off_end=float(input('Enter OFF pulse phase end\n'))

############  Starting individual pulse analysis  ########## 

while True:
	n=(input('Enter your option ( n to jump n pulses, "q" to quit)'))
	if(str(n)=='h'):
		print('  enter q to quit\n enter p to set phase range\n enter w to write current pulse in file\n enter integer n to jump by n pulses\n enter s to save figure\n enter d to downsample\n enter h to get this help\n')
	elif(str(n)=='q'):
		break;
	elif(str(n)=='p'):
		start=float(input('phase start'))
		end=float(input('phase end'))
	elif(str(n)=='d'):
		df=int(input('enter downsampling factor'))

	elif(str(n)=='w'):
		sup=str(input('enter extension'))
		fw=open(write_directory+'/'+'pulse2_'+str(cycle)+'_'+sup+'.txt','w')
		j=0
		for r in phase1:
			fw.write(str(r)+'	'+str(I1[j])+'\n')
			j=j+1
		fw.close()
	elif(str(n)=='s'):
		plt.clf()
		plt.xlabel('phase')
		plt.ylabel('intensity')
		plt.title('Pulse number'+str(cycle))
		plt.plot(phase1,I1)
		plt.savefig('pulse_'+str(cycle)+'.png')
		
##############  Implementing Running median subtraction   ###################################		
		
	elif (str(n)=='rms'):
		box=float(input('enter boxcar size (in units of phase):'))
		size=len(I1)
		w=int((box*period)/del_t)
		sum=[]
		baseline=[]
		for i in range(size):
			if (i==0):
				for j in range(i-int(w/2),i+int(w/2)):
					if (j<0):
						j=size+j
					if(j>=size):
						j=j-size
					sum.append(I1[j])
			else:
				j=i+int(w/2)
				if(j>=size):
					j=j-size
				sum=np.delete(sum,0)
				sum=np.r_[sum,[I1[j]]]
			baseline.append(float(np.median(sum)))
			if (i%w>=w-1):
				print("done "+str(int(float(i)/float(size)*100))+"% of data")
		baseline=np.array(baseline)
		I2=I1-baseline
		plt.xlabel('phase')
		plt.ylabel('intensity')
		plt.title('Pulse number'+str(cycle))
		plt.plot(phase1,I1)
		plt.plot(phase1,baseline)
		plt.plot(phase1,I2)
		plt.show()
		next=str(input('Want to go ahead [Y/N]:'))
		if(next=='Y'):
			continue;

#############    Implementing micropulse selection    #######################################################			

	elif (str(n)=='micro'):
		index=[]
		k=0
		for l in range(0,len(I2)):
			if (I2[l]>4*off_rms):
				if (baseline[l]<I2[l]/10.0):
					index.append(l)
					k=k+1
			if (I2[l]<4*off_rms):
				if(k<1):
					continue;
				else:
					micro_I=[]
					micro_phase=[]
					for m in range(index[0]-3,index[-1]+3):
						micro_I.append(I1[m])
						micro_phase.append(phase1[m])
					plt.xlabel('Phase')
					plt.ylabel('Intensity')
					plt.plot(micro_phase, micro_I)
					plt.show()
					write=str(input('Want to write?[Y/N]'))
					if(write=='Y'):
						extension=str(input('Enter extension:'))
						fw=open('pulse_'+str(cycle)+'_'+extension+'.txt','w')
						i=0
						for x in micro_phase:
							fw.wrtie(str(x)+'   '+str(micro_I[i])+'\n')
							i=i+1
						index=[]
						k=0
					else:
						index=[]
						k=0					
	else:
		n1=int(n)
	plt.clf()
	plt.xlabel('Phase')
	plt.ylabel('Intensity')
	plt.title('Pulse number: '+str(n1+cycle))
	phase=[]
	b=0

###############  Implementing Zoom ############################

	start_samp=int(((n1+cycle)*period)/del_t)
	end_samp=int(((n1+cycle+1)*period)/del_t)
#	start_samp=(cycle+n1)*p
#	end_samp=(cycle+n1+1)*p
	print('start samp is'+str(start_samp)+'\n')
	print('end samp is '+str(end_samp)+'\n')
	for l in range(start_samp, end_samp):
		I.append(noise[l])
		phase.append(b)
		b=b+1
	phase=np.array(phase)/float(b)
	I=np.array(I)
	phase1=[]
	I1=[]
	p1=end_samp-start_samp
	
############   Storing ON pulse   ##############################	
	
	for k in range(int(start*p1),int(end*p1)):
		phase1.append(phase[k])
		I1.append(I[k])	

###########   Calculating OFF RMS and MEDIAN #######################
	off=[]
	for k in range(int(off_start*p1),int(off_end*p1)):
		off.append(I[k])
	off_rms=np.std(np.array(off))
	off_med=np.median(np.array(off))
	print('Off RMS is '+str(off_rms))
	print('Off meadian is '+str(off_med))

#######   Implementing downsampling    ########################

	i=0
	sum=0
	new_t=[]
	new_phase=[]
	for x in I1:
		sum=sum+x
		
		if(i%df==0):
			new_t.append(sum/float(df))
			new_phase.append(phase1[i])
			sum=0
		i=i+1
	I1=np.array(new_t)[1:]
	base1=np.ones(len(I1))*off_med
	I1=I1-base1
	phase1=np.array(new_phase)[1:]

 ############    PLotting     ###################################

	cycle=cycle+n1
	plt.plot(phase1,I1)
	plt.show()
	I=[]
	n1=0
        

