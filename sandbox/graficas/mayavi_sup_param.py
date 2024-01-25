import numpy as np
from mayavi import mlab
import sympy as sp

def grafica_sup_param(sup, u, v, limite_inf_u, limite_sup_u, limite_inf_v, limite_sup_v):
    parametric_surface = sp.lambdify((u, v), sup, 'numpy')

    u_values = np.linspace(float(limite_inf_u), float(limite_sup_u), 100)
    v_values = np.linspace(float(limite_inf_v), float(limite_sup_v), 100)
    u_values, v_values = np.meshgrid(u_values, v_values)

    x, y, z = parametric_surface(u_values, v_values)

    mlab.mesh(x, y, z, colormap='viridis')

u, v = sp.symbols('u v')
parametrizacion = (sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v) , sp.sin(u))
grafica_sup_param(parametrizacion, u, v, -sp.pi/2, sp.pi/2, 0, 2*sp.pi)

mlab.axes()
mlab.show()