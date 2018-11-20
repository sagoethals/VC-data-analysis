"""
Relationship between the cell capacitance and the peaka xonal current.

!!! cells from 30.08 are with Martijn's IC and from 24.10 with mine.

"""

from brian2 import *
import pandas as pd

prefs.codegen.target = 'cython'

# Good cells
data = pd.read_excel("/media/sarah/storage/Data/Sarah/Na activation analysis.xlsx")

cell = ['2018300807', '2018102402']
cell_capa = array([5.9 , 4.6])
peak_current_80 = array([data['Ia'][0], data['Ia'][6]])

peak_current = array([data['Ia'][:6], data['Ia'][6:]])
Vc_rest = array(data['Vr'][:6])

print cell, cell_capa, peak_current_80

# Cells with higher Rs but still clamped
cell_bad = ['2018083005', '2018102409']
cell_capa_bad = array([3.1, 4.2])
peak_current_80_bad = array([-366.82, -572])

# Plots
figure(1)
plot(cell_capa, abs(peak_current_80), 'go')
plot(cell_capa_bad, abs(peak_current_80_bad), 'ro')
ylabel('-Ia (pA)')
xlabel('Cm (pF)')

tight_layout()

figure(2)
plot(Vc_rest, abs(peak_current[0]), '-o', label='%s' %cell[0])
plot(Vc_rest, abs(peak_current[1]), '-o', label='%s' %cell[1])
ylabel('-Ia (pA)')
xlabel('Vr')
legend(frameon=False)
tight_layout()

show()