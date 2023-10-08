import numpy as np
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Definir arreglos unidimensionales para coordenadas x e y
x = [1,2]
print(x)
y = [3,4]
print(y)

# Crear una malla bidimensional utilizando np.meshgrid()
X, Y = np.meshgrid(x, y)
Z=np.array([[1,2], [3,4]])

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