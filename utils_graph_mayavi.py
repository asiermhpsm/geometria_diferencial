import numpy as np
from mayavi import mlab
import sympy as sp

def grafica_sup_param_mayavi(sup, u, v, limite_inf_u=-10, limite_sup_u=10, limite_inf_v=-10, limite_sup_v=10):
    parametric_surface = sp.lambdify((u, v), sup, 'numpy')
    u_values = np.linspace(float(limite_inf_u), float(limite_sup_u), 100)
    v_values = np.linspace(float(limite_inf_v), float(limite_sup_v), 100)
    u_values, v_values = np.meshgrid(u_values, v_values)
    X, Y, Z = parametric_surface(u_values, v_values)
    if np.isscalar(X):
        X = np.full_like(u_values, X)
    if np.isscalar(Y):
        Y = np.full_like(u_values, Y)
    if np.isscalar(Z):
        Z = np.full_like(u_values, Z)
    mlab.mesh(X, Y, Z, color=(0.2980392156862745, 0.4470588235294118, 0.6901960784313725))

def grafica_sup_ec_mayavi(sup, x, y, z, limite_inf_x=-10, limite_sup_x=10, limite_inf_y=-10, limite_sup_y=10):
    parametric_surface = sp.lambdify((x, y, z), sup, 'numpy')
    X, Y, Z = np.mgrid[limite_inf_x:limite_sup_x:150j, limite_inf_y:limite_sup_y:150j, -10:10:150j]
    values = parametric_surface(X, Y, Z)
    mlab.contour3d(X, Y, Z, values, contours=[0], color=(0.2980392156862745, 0.4470588235294118, 0.6901960784313725))

def grafica_punto_mayavi(punto):
    mlab.points3d(*punto, color=(1, 0, 0), scale_factor=0.1, mode='sphere')

def grafica_vector_mayavi(inicio, vector):
    mlab.quiver3d(*inicio, *vector, color=(0, 0, 1), scale_factor=1)

#mlab.plot3d([0, 2], [0, 0], [0, 0], color=(1, 0, 0), tube_radius=None)
#mlab.plot3d([0, 0], [0, 2], [0, 0], color=(0, 1, 0), tube_radius=None)
#mlab.plot3d([0, 0], [0, 0], [0, 2], color=(0, 0, 1), tube_radius=None)
#parametrizacion = (sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v) , sp.sin(u)*sp.sin(v))
#grafica_sup_param_mayavi(parametrizacion, u, v, -sp.pi/2, sp.pi/2, 0, 2*sp.pi)
#x, y, z = sp.symbols('x y z')
#plano = (x/3)**2 + (y/2)**2 + (z/1)**2 - 1
#grafica_sup_ec_mayavi(plano, x, y, z, -10, 10, -10, 10)
#punto = np.array([0, 0, 1])
#grafica_punto_mayavi(punto)
#vector = np.array([0, 0, 1])
#grafica_vector_mayavi(punto, vector)
#mlab.axes()
#mlab.orientation_axes()
#mlab.show()