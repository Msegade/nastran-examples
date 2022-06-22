from pyNastran.bdf.bdf import BDF
import numpy as np

bdf = BDF()
bdf.read_bdf('1dof-damping.bdf')

sub = bdf.subcases[0]
sub.add('DLOAD', 111, [], 'STRESS-type')

bdf.add_darea(10, 2, 2, 1.0)
bdf.add_tload1(111, 10, 444, 0.0, 0)
tstep = bdf.tsteps[888]
dt = tstep.DT[0]
n = tstep.N[0]

#w = 3.4*(2*np.pi)
w = 3.4
x = np.linspace(0.0, dt*n, n)
y = 0.7*np.sin(w*x)

bdf.add_tabled1(444, x, y)

bdf.write_bdf('1dof-loading.bdf')
