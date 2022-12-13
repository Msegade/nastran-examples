import numpy as np

rho = 1.225
xf = 3.0
c = 6.0

b = c/2
a = xf/b-1

K = 50.0 

aMoment = 2*np.pi*rho*b**2*(a+1/2)
Ud = np.sqrt(K/aMoment)
qd = 1/2*rho*Ud**2

print(f"Divergence speed = {Ud}")
print(f"Divergence dynamic pressure = {qd}")
