import sympy as sp
from sympy.plotting import plot_implicit

#x, y, z = sp.symbols('x y z')

#plot_implicit(x**2 + y**2 + z**2 < 1)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir la ecuación implícita
def implicit_equation(x, y, z):
    return x**2 + y**2 + z**2 - 1  # Ejemplo: esfera de radio 1

# Crear una malla de puntos en 3D
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
z = np.linspace(-1, 1, 100)
x, y, z = np.meshgrid(x, y, z)

# Calcular el valor de la ecuación implícita en cada punto de la malla
values = implicit_equation(x, y, z)

# Crear una figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Hacer el plot de la superficie para los puntos donde la ecuación es igual a cero
ax.contour3D(x, y, z, values, levels=[0], cmap='viridis')

# Configurar la visualización
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Plot de Ecuación Implícita en 3D')

# Mostrar el plot
plt.show()
