import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Crear una figura y un subgráfico 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Coordenadas del origen del vector
x_origin = 0
y_origin = 0
z_origin = 0

# Componentes del vector
x_component = 1
y_component = 2
z_component = 3

# Representar el vector en 3D
ax.quiver(x_origin, y_origin, z_origin, x_component, y_component, z_component)

# Configuraciones adicionales
ax.set_xlim([0, 5])  # Establecer límites de los ejes x
ax.set_ylim([0, 5])  # Establecer límites de los ejes y
ax.set_zlim([0, 5])  # Establecer límites de los ejes z

# Mostrar la gráfica
plt.show()