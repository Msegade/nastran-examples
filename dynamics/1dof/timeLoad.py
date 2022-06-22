from pyNastran.bdf.bdf import BDF
import numpy as np
import subprocess

bdf = BDF()
bdf.read_bdf('1dof-load.bdf')

tstep = bdf.tsteps[888]
dt = tstep.DT[0]
n = tstep.N[0]

w = 3.4 # rad/s
P = 0.7 # load amplitude
x = np.linspace(0.0, dt*n, n)
y = P*np.sin(w*x)

tbdf = BDF()
tbdf.punch = True
tbdf.add_tabled1(444, x, y)
tbdf.add_darea(10, 2, 2, 1.0)
tbdf.add_tload1(111, 10, 444, 0.0, 0)
tbdf.write_bdf('tload.bdf')

# Add a blank line to the end to avoid nastran errors
with open('tload.bdf', 'a') as outfile:
    subprocess.run(['echo', '""'], shell=True, stdout=outfile)
