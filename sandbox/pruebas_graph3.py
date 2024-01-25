import numpy as np
from mayavi import mlab

mlab.clf()
x, y, z = np.mgrid[-3:3:50j, -3:3:50j, -3:3:50j]

# Plot a sphere of radius 1
values = x*x + y*y + z*z - 1
mlab.contour3d(x, y, z, values, contours=[0])
mlab.axes()

# Plot a torus
R = 2
r = 1
values = (R - np.sqrt(x**2 + y**2))**2 + z**2 - r**2
mlab.figure()
mlab.contour3d(x, y, z, values, contours=[0])
mlab.axes()

# Plot a Scherk's second surface
x, y, z = np.mgrid[-4:4:100j, -4:4:100j, -8:8:100j]
values = np.sin(z) - np.sinh(x)*np.sinh(y)
mlab.figure()
mlab.contour3d(x, y, z, values, contours=[0])
mlab.axes()
mlab.show()