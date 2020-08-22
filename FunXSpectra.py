##Comentarios de código original en MATLAB

#function to compute spectra and cross-spectra from two time series y1 and
#y2. It uses a Hanning filter to average the spectra with (dof) degrees of
#freedom. It also requires the sampling rate in seconds.
#
#USAGE function [f,S1,S2,coh2,phase,bw,coh2Crit]=FunXSpectra(y1,y2,dt,dof,plot)
#
#Inputs
#------
#y1,y2      :time series sampled at 1/dt Hz.
#dof        : number of degrees of freedom.
#
#OUTPUTS
#-------
#f          :frequency domain
#S1,S2      :auto spectra of each series.
#coh2       :Coherence
#phase      : phase spectra
#bw         :effective bandwidth
#
#Coded by Patricio Catalan, OSU, 2004;

import matplotlib.pyplot as plt
import numpy as np

def FunXSpectra(y1,y2,dt,dof,plots):
   
    y1=y1-y1.mean() #demean
    y2=y2-y2.mean()
    N=len(y1)
    if len(y1) != len(y2):
        N=min(len(y1),len(y2))
    
    #correcting N to be power of 2.
    N=int(2**(np.floor(np.log(N)/np.log(2))))
    y1=y1[:N] #trim the series
    y2=y2[:N]
    T=N*dt #%record length, in units of time
    f=np.arange(1/T,1/(2*dt)+1/T,1/T) #frequency up to Nyquist
    
    #Hanning filter
    filt_length=(3/4*dof-1) #%Ex. if dof=12, filt_length=10 
    filt_length=(np.floor(filt_length/2)+0.5)*2 #and now is round up to next odd number up, 11
    hf=int(np.floor(filt_length/2)) #hmmm...what is this? Value 5.5 in our example
    hanning_filter=np.hanning(filt_length+2)[1:-1] #hanning curve of filt =length
    hanning_filter=hanning_filter/sum(hanning_filter) #normalized
    I=sum(hanning_filter*hanning_filter) #bandwidth in Hz, but why? 1/T is Delta f, which is amplified by the I to give the real bandwith afeter the filter is applied
    bw=1/(T*I)
    
    #AutoSpect
    Y1=np.fft.fft(y1,N) #FFT with N points, zero padded if needed
    Y1=Y1[1:int(N/2)+1]/N #one sided
    S1=np.real(2*T*np.conj(Y1)*Y1) #Gxx : one sided spectral density function (5.67 Bendat and Piersol)
    Sbar1=np.convolve(S1,hanning_filter) #smootehd version, contains extra points
    S1=Sbar1[hf:len(Sbar1)-hf] #smoothed (averaged) PSD
    
    #repeat for second signal
    Y2=np.fft.fft(y2,N) 
    Y2=Y2[1:int(N/2)+1]/N
    S2=np.real(2*T*np.conj(Y2)*Y2) #Gyy : one sided spectral density function (5.67 Bendat and Piersol)
    Sbar2=np.convolve(S2,hanning_filter)
    S2=Sbar2[hf:len(Sbar2)-hf]
    
    #Cross-spectrum
    xspect=2*T*Y1*np.conj(Y2) #Gxy : one sided cross-spectral density function Pxy (5.66 Bendat and Piersol)
    smoothed=np.convolve(xspect,hanning_filter) #filtered one sided cross SDF
    smoothed=smoothed[hf:int(N/2)+hf] #remove extra points
    
    #now compute the norm of the Magnitude Squared Coherence 
    #gamma^2=|Pxy|^2 /  (Pxx Pyy)
    norm=np.real((4*T*T*(np.conj(Y1)*Y1*(np.conj(Y2)*Y2)))**0.5) #||Gxx*Gyy|| %total Energy?
    smoothed_norm=np.convolve(norm,hanning_filter) #smooth it
    smoothed_norm=smoothed_norm[hf:int(N/2)+hf] #remove extra points
    #note: coherence gives f=1 for all frequencies if no windowing is applied.
    coh2=abs(smoothed)**2/smoothed_norm**2 #Gxy^2/(Gxx*Gyy)=gamma_xy^2 
    phase=np.angle(smoothed)
        
    if plots==1:
        fig = plt.figure(figsize=(8,7))
    
        ax1 = fig.add_subplot(321)
        plt.xscale('log')
        ax2 = fig.add_subplot(322,sharey=ax1,sharex=ax1)
        ax3 = fig.add_subplot(312,sharex=ax1)
        ax4 = fig.add_subplot(313,sharex=ax1)
    
        ax1.plot(f,S1)
        ax2.plot(f,S2,'r')
        ax3.plot(f,coh2)     
        ax4.plot(f,phase)
    
        plt.show()
    
    return f,S1,S2,coh2,phase,bw