

"""
Plot IV curves for different resting mcommand potential. 
"""

from brian2 import *

prefs.codegen.target = 'cython'

August = False

if August==True:
    path = "/media/sarah/storage/Data/Sarah/Patch August 2018/2018083007/"
    #files = ["180830_001.VC_threshold_adapt80.4.txt", "180830_001.VC_threshold_adapt70.3.txt",  "180830_001.VC_threshold_adapt65.3.txt",\
    #          "180830_001.VC_threshold_adapt55.2.txt"] # for cell 5
    files = ["180830_001.VC_threshold_adapt80.7.txt", "180830_001.VC_threshold_adapt75.7.txt", "180830_001.VC_threshold_adapt70.6.txt", \
             "180830_001.VC_threshold_adapt65.5.txt", "180830_001.VC_threshold_adapt60.5.txt", "180830_001.VC_threshold_adapt55.4.txt"] # for cell 7

    n_samples = 24832   
    dt = 0.01999*ms 
    Dt = 496.39*ms
    start = int(400.20*ms/dt)
    end = int(420.0*ms/dt)
    
    fig_title = "Cell 20180830 07: $C_m = 5.9$ pF, $R_s = 22.4$ MOhm"
else:
    path = "/media/sarah/storage/Data/Sarah/Patch October 2018/2018102402/"
    files = ["181024_001.VC_threshold_adapt80.2.txt", "181024_001.VC_threshold_adapt75.2.txt", "181024_001.VC_threshold_adapt70.2.txt", \
             "181024_001.VC_threshold_adapt65.1.txt", "181024_001.VC_threshold_adapt60.1.txt", "181024_001.VC_threshold_adapt55.1.txt"]
    
    n_samples = 12544 #Dt/dt
    dt = 0.019989999999999*ms 
    Dt = 250.7346*ms
    start = int(200.20*ms/dt)
    end = int(220.0*ms/dt)
    
    fig_title = 'Cell 20181024 02, $C_m = 4.6$ pF, $R_s = 27$ MOhm '
    
vr = [-80, -75, -70, -65, -60, -55]
vs = linspace(-80, -20, 31)

cmap = plt.get_cmap('viridis')
colors = [cmap(i) for i in np.linspace(0, 1, (len(files)))]

thresholds = zeros(len(files))
#current_SI = zeros(len(files))
peak_axonal_current = zeros(len(files))

figure('IV curve')

for k in range(len(files)):
    file = files[k]
    print file
    name = path + file

    # Plot data
    f = open(name,"r")
    data = f.readlines()

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

    idx_peaks = []
    i_peaks = []
    
    for i in range(j-1): 
        ts,Is,Vs = array(sweeps[i]).T 
        peak = argmin(Is[start:end]) + start
        idx_peaks.append(peak)
        i_peaks.append(Is[peak])
        
    # Analysis
    #baseline = mean(i_peaks[:15])
    idx_th = where(array(i_peaks)>=-200.)[0][-1]
    thresholds[k] = vs[idx_th]
    #current_SI[k] = i_peaks[idx_th] - baseline
    peak_i = i_peaks[idx_th+1] - i_peaks[idx_th]
    peak_axonal_current[k] = peak_i
        
    plot(vs[:-1], i_peaks, '-o', color = colors[k], label='Vr = %i mV' %vr[k])
    
xlabel('V (mV)', fontsize=16)
ylabel('Peak I (pA)', fontsize=16)
title('%s ' %fig_title)
tight_layout()
legend(frameon=False)

show()

print thresholds
print peak_axonal_current
