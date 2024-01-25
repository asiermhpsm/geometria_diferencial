import numpy as np
from mayavi import mlab
import sympy as sp

def grafica_sup_param(sup, u, v, limite_inf_u, limite_sup_u, limite_inf_v, limite_sup_v):
    parametric_surface = sp.lambdify((u, v), sup, 'numpy')
    u_values = np.linspace(float(limite_inf_u), float(limite_sup_u), 100)
    v_values = np.linspace(float(limite_inf_v), float(limite_sup_v), 100)
    u_values, v_values = np.meshgrid(u_values, v_values)
    x, y, z = parametric_surface(u_values, v_values)
    #mlab.mesh(x, y, z, colormap='viridis')
    mlab.mesh(x, y, z, color=(0.2980392156862745, 0.4470588235294118, 0.6901960784313725))

def grafica_sup_ec(sup, x, y, z, limite_inf_x, limite_sup_x, limite_inf_y, limite_sup_y):
    parametric_surface = sp.lambdify((x, y, z), sup, 'numpy')
    x_vals, y_vals, z_vals = np.mgrid[limite_inf_x:limite_sup_x:50j, limite_inf_y:limite_sup_y:50j, -10:10:50j]
    values = parametric_surface(x_vals, y_vals, z_vals)
    mlab.contour3d(x_vals, y_vals, z_vals, values, contours=[0])

def grafica_punto(punto):
    mlab.points3d(*punto, color=(1, 0, 0), scale_factor=0.1, mode='sphere')

def grafica_vector(inicio, vector):
    mlab.quiver3d(*inicio, *vector, color=(0, 0, 1), scale_factor=1)

"""mlab.plot3d([0, 2], [0, 0], [0, 0], color=(1, 0, 0), tube_radius=None)
mlab.plot3d([0, 0], [0, 2], [0, 0], color=(0, 1, 0), tube_radius=None)
mlab.plot3d([0, 0], [0, 0], [0, 2], color=(0, 0, 1), tube_radius=None)"""

u, v = sp.symbols('u v')
parametrizacion = (sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v) , sp.sin(u))
grafica_sup_param(parametrizacion, u, v, -sp.pi/2, sp.pi/2, 0, 2*sp.pi)

x, y, z = sp.symbols('x y z')
plano = z - 1
#grafica_sup_ec(plano, x, y, z, -1, 1, -1, 1)

punto = np.array([0, 0, 1])
#grafica_punto(punto)

vector = np.array([0, 0, 1])
#grafica_vector(punto, vector)

mlab.axes()
#mlab.orientation_axes()
mlab.show()