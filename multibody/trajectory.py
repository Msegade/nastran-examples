import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import netCDF4

data = netCDF4.Dataset('pendulum.nc', 'r')

NodeLabel = 20
position = data.variables['node.struct.' + str(NodeLabel) + '.X']
t = data.variables['time'][:]

fig, ax = plt.subplots()
ax.set_aspect('equal')
x = position[:,0]
y = position[:,2]
ax.plot(x, y)
plt.savefig('trajectory.png')
plt.close()

fig, ax = plt.subplots()
angle = np.arctan(x/y)
ax.plot(t, angle)
plt.savefig('angle.png')


