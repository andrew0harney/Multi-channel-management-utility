import numpy as np
import pandas as pd
from SignalManager import SignalManager
from gridFT import calcFFT
from signalUtils import longest_event
import matplotlib.pyplot as plt

#This script generates a synthetic dataset with periodic signals and experimental epochs.
#The FFT is then taken across experimental events in the signal to demonstrate the FFT functionality
#Note : This code was written for early versions of the SignalManager package and so may not be totally compatable

#Generate synthetic periodic data
delta = 0.001
ws = 0.1
x = np.linspace(-np.pi, np.pi,fs)
times = np.arange(0,4,1.0/fs)

sig1 = np.hstack([np.random.rand(len(x)),np.sin(100*x),np.sin(150*x),np.sin(150*x)])
sig2 = np.hstack([np.sin(50*x),np.sin(80*x),np.random.rand(len(x)),np.sin(10*x)])
sig3 = np.hstack([np.sin(10*x),np.sin(10*x),np.sin(40*x),np.sin(40*x)])
sig = np.array([sig1,sig2,sig3])


#Save the data in the format required by SignalManager 
dataName= 'PeriodicSTFT'
SignalManager.save_hdf(sig, times, ['s1','s2','s3'],base_file_name=dataName)

#Create synthetic experimental epochs in the data
events = np.vstack((times,times+0.1,np.zeros(len(times)))).T
events = pd.DataFrame(events,columns=['pulse.on','pulse.off','event.code'])
events.to_csv(dataName+'test_events.csv',columns=['pulse.on','pulse.off','event.code'],delimeter='\t')

############################################


#Load the synthetic data
dataName= 'PeriodicSTFT'
fs = 500
grid = SignalManager(dataName,log_file=dataName+'test_events.csv')
grid.set_wd(['s1','s2','s3'])

#Get experimental events
em = grid.event_matrix()
firstHalf = em[em['pulse.off']<2]
secondHalf = em[em['pulse.off']>=2]
blocks = pd.DataFrame(np.array([[0,0.998],[1,1.998],[2,2.998],[3,3.998]]),columns=['pulse.on','pulse.off'])
blocksLongest = longest_event(grid,blocks)

#Perfom the FFT on events in the data
result = calcFFT(grid,blocks,maxBlock = blocksLongest,zeroPadFactor=1)
(x,y,z) = result.shape

freq = np.fft.fftfreq(z,1.0/grid.fs())[:z/2]
plt.plot(freq[:z],result[0,2,:z/2],'r') # plotting the spectrum
plt.xlabel('Freq (Hz)')
plt.ylabel('|Y(freq)|')
plt.grid(True, which='both')
plt.show()
