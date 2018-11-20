#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Read data in txt files
"""

from brian2 import *

prefs.codegen.target = 'cython'

#path = "/media/sarah/storage/Data/Sarah/Patch April-June 2018/Data/"
path = "/media/sarah/storage/Data/Sarah/Patch August 2018/201808290/"
#path = "/media/sarah/storage/Data/Sarah/Patch August 2018/2018082807/"

#file = "180830_001.VC_prepulse.9.txt"
#file = "180830_001.VC_threshold_adapt80.4.txt"
file = "180829_001.VC_threshold_adapt80.4.txt"
Rs = 58

name = path + file

# Plot data

f = open(name,"r")
data = f.readlines()

n_samples = 24832
dt = 0.01999*ms 
Dt = 496.39*ms

sweeps = []
M = []

j = 1
for i, line in enumerate(data):
    if  i < j*n_samples:
        M.append(([float(x.replace(',', '.')) for x in line.split()]))
    else: 
        sweeps.append(M)
        M = []
        j = j+1

figure('Data')
cmap = plt.get_cmap('gnuplot')
colors = [cmap(i) for i in np.linspace(0, 1, j-1)]

for i in range(j-1):
    t,I,V=array(sweeps[i]).T
    
    #print V[20050]-80
    
    title('20180830 07')
    subplot(211)
    #title('Cell 1: Cp = 6.7 pF, Rs = 17Mohm, Rs comp = 75%')
    #title('Cell 2: Cp = 7.1 pF, Rs = 13Mohm, Rs comp = 50%')
    plot(t,I, color = colors[i])
    ylabel('I (pA)', fontsize=16)
    xlim(0.395,0.425)
    
    subplot(212)
    plot(t,V-80, color = colors[i])
    xlabel('Time (s)', fontsize=16)
    ylabel('V (mV)', fontsize=16)
    xlim(0.395,0.425)
    tight_layout()


# IV curve

## for data from June 2018
#vs = linspace(-90, 30, 31)
#dt = 60*ms/4096
#start = int(20.2*ms/dt)
#end = int(40*ms/dt)
    
# for data from August 2018
vs = linspace(-80, -20, 31)
start = int(400.20*ms/dt)
end = int(420.0*ms/dt)
idx_peaks = []
v_peak = []
i_peaks = []

for i in range(j-1): 
    ts,Is,Vs = array(sweeps[i]).T 
    peak = argmin(Is[start:end]) + start
    true_vs_peak = Vs[peak]-80 - 0.75*Rs*1e-3*Is[peak]
    idx_peaks.append(peak)
    v_peak.append(true_vs_peak)
    i_peaks.append(Is[peak])
    
# Analysis
    
idx_th = where(array(i_peaks)>=-200.)[0][-1]
v_threshold = vs[idx_th]
#current_SI[k] = i_peaks[idx_th] - baseline
peak_i = i_peaks[idx_th+1] - i_peaks[idx_th]

print 'Threshold:', v_threshold
print 'Peak axonal current:', peak_i

figure('IV curve')
plot(vs[:-1], i_peaks, '-o', color='k')
plot(v_peak, i_peaks, 'k--o', color='k')
#plot(vs[14:-2], i_peaks[14:], 'ro', label='bad clamp')
xlabel('V (mV)', fontsize=16)
ylabel('Peak I (pA)', fontsize=16)
title('20180830 07') # $C_m \simeq 6.4$ pF')
tight_layout()
    
show()



