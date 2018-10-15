#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 16:14:39 2018

@author: sarah
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Read data in txt files
"""

from brian2 import *

prefs.codegen.target = 'cython'

path = "/media/sarah/storage/Data/Sarah/Patch April-June 2018/Data/"

file = "180620_002.VC_activation.7.txt"

name = path + file

# Plot data

f = open(name,"r")
data = f.readlines()

n_samples = 4096

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
    
    title('20180620 02')
    subplot(211)
    #title('Cell 1: Cp = 6.7 pF, Rs = 17Mohm, Rs comp = 75%')
    #title('Cell 2: Cp = 7.1 pF, Rs = 13Mohm, Rs comp = 50%')
    plot(t,I, color = colors[i])
    ylabel('I (pA)', fontsize=16)
    #xlim(0.395,0.425)
    
    subplot(212)
    plot(t,V-80, color = colors[i])
    xlabel('Time (s)', fontsize=16)
    ylabel('V (mV)', fontsize=16)
    #xlim(0.395,0.425)
    tight_layout()


# IV curve

vs = linspace(-90, 22, 29)
dt = 60.*ms/n_samples
start = int(20.5*ms/dt)
end = int(40*ms/dt)
    
idx_peaks = []
i_peaks = []

for i in range(j-1): 
    ts,Is,_ = array(sweeps[i]).T 
    peak = argmin(Is[start:end]) + start
    print peak
    idx_peaks.append(peak)
    i_peaks.append(Is[peak])
    
figure('IV curve')
plot(vs, i_peaks, 'k-')
plot(vs, i_peaks, 'ko', label='clamped')
#plot(vs[14:-2], i_peaks[14:], 'ro', label='bad clamp')
xlabel('V (mV)', fontsize=16)
ylabel('Peak I (pA)', fontsize=16)
title('20180620 02')
tight_layout()
    
show()



