import numpy as np
from mayavi import mlab
import sympy as sp

mlab.clf()

x, y, z = sp.symbols('x y z')
#esfera = x**2 + y**2 + z**2 - 1
esfera = (x/3)**2 + (y/2)**2 + (z/1)**2

esfera_np = sp.lambdify((x, y, z), esfera, 'numpy')

x_vals, y_vals, z_vals = np.mgrid[-10:10:100j, -10:10:100j, -10:10:100j]

values = esfera_np(x_vals, y_vals, z_vals)

mlab.contour3d(x_vals, y_vals, z_vals, values, contours=[0])
mlab.axes()
mlab.show()
