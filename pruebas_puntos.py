import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from metodos import *

u, v = sp.symbols('u, v', real = True)
x, y, z = sp.symbols('x, y z', real = True)

ecuaciones1 = [u*sp.cos(v), u*sp.sin(v), 2*u]
u0 = 1
v0 = 2*np.pi

representa_3d(*procesa_punto_uv(ecuaciones1, u, v, u0, v0))
