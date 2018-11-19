

"""
Read test pulse data from txt files.
"""

from brian2 import *
from traces_analysis import *

prefs.codegen.target = 'cython'

#path = "/media/sarah/storage/Data/Sarah/Patch April-June 2018/Data/"
#path = "/media/sarah/storage/Data/Sarah/Patch August 2018/2018083007/"
path = "/media/sarah/storage/Data/Sarah/Patch August 2018/2018083007/"
file = "180830_001.VC_test_pulse.11.txt"

name = path + file

# Plot data

f = open(name,"r")
data = f.readlines()

sweeps = []
M = []

n_samples = 4096
j = 1
for i, line in enumerate(data):
    if  i < j*n_samples:
        M.append(([float(x.replace(',', '.')) for x in line.split()]))
    else:  
        sweeps.append(M)
        M = []
        j = j+1

figure(1)
cmap = plt.get_cmap('gnuplot')
colors = [cmap(i) for i in np.linspace(0, 1, j-1)]

Is = zeros((j-1, n_samples-1))
Vs = zeros((j-1, n_samples-1))

for i in range(j-1):
    t,I,V=array(sweeps[i]).T
    
    if len(I) == 4095:
        Is[i,:] = I
        Vs[i,:] = V
    else:
        Is[i,:] = I[1:]
        Vs[i,:] = V[1:]
    
    subplot(211)
    plot(t,I, color = colors[i])
    ylabel('I (pA)', fontsize=16)
    #xlim(0.395,0.425)
    
    subplot(212)
    plot(t,V-80, color = colors[i])
    xlabel('Time (s)', fontsize=16)
    ylabel('V (mV)', fontsize=16)
    #xlim(0.395,0.425)
    tight_layout()
    
# Analysis

I_mean = mean(Is, axis=0)
V_mean = mean(Vs, axis=0)

figure(2)
plot(t, I_mean, 'k')


dt = t[1] - t[0] #2.44*1e-5

# Find the peak of the first transient current 
transient_time = find_spikes_at(I_mean, dt, -100.)
I_peak = find_peak(I_mean, dt, transient_time[0]) # contains the index and value
plot((I_peak[0]+1)*dt, I_peak[1], 'ro')

# Series resistance
base = np.where((t>0.005)&(t<0.03))
I_baseline = mean(I_mean[base[0]])
plot(t, I_baseline*ones(len(I_mean)), 'c--', label='baseline')

I_amp_peak1 = abs(I_peak[1]-I_baseline) # pA
V_baseline = mean(V_mean[base[0]]) # the true baseline potential
V_step = abs(V_mean[int(I_peak[0]+1)]-V_baseline) # true voltage step, in mV
print 'Peak current amplitude:', I_amp_peak1
print 'V step:', V_step

Rs = (V_step/I_amp_peak1)*1e3 # mV/pA -> GOhm

print 'Leak current:', I_baseline, 'pA'
print 'series resistance:', Rs, 'MOhm'

# Membrane resistance
plat = np.where((t>0.035)&(t<0.05))
I_plat = mean(I_mean[plat[0]])
I_amp_plat1 = abs(I_plat-I_baseline)
plot(t, I_plat*ones(len(I_mean)), 'm--', label='plateau')

Rm = (V_step/I_amp_plat1)*1e3

print 'membrane resistance:', Rm, 'MOhm'

# Membrane area
areabox = abs(0.02 * I_amp_plat1) # area btw baseline and the plateau, due to Rm
area_idx = np.where((t>0.03)&(t<0.05))
area_time = t[area_idx[0]]
area_I = I_mean[area_idx[0]]-I_baseline

area = 0
for i in range(len(area_I)-1): 
    area = area + (area_I[i]*(area_time[i+1]-area_time[i])) + (0.5*((area_I[i+1]-area_I[i])*(area_time[i+1]-area_time[i])))

#print 'area tot', area

area = (abs(area) - areabox) # s*pA 
#print 'area peak', area

# membrane capacitance
Cm = (area/V_step) * 1e3 # pS

print 'cell capacitance:', Cm
print 'time cst:', Cm*Rs, 'us'

legend(frameon=False)

show()





















    
