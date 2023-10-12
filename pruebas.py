import numpy as np
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Definir arreglos unidimensionales para coordenadas x e y
x = [1,2,3]
print(x)
y = [4,5]
print(y)

# Crear una malla bidimensional utilizando np.meshgrid()
X, Y = np.meshgrid(x, y)
Z=np.array([[1,2,3], [4,5,6]])

# Imprimir las matrices resultantes X e Y
print("Matriz X:")
print(X)
print("\nMatriz Y:")
print(Y)
print("\nMatriz Z:")
print(Z)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# Customize the z axis.
#ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')
# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

import sympy as sp

# Define las incógnitas
x, y = sp.symbols('x y')

# Define el sistema de ecuaciones
ecuacion1 = sp.Eq(2*x + 3*y, 7)
ecuacion2 = sp.Eq(4*x - y, 6)
print(ecuacion2)

# Resuelve el sistema
solucion = sp.solve((ecuacion1, ecuacion2), (x, y))

# Imprime la solución
print("Solución:")
print(solucion)
