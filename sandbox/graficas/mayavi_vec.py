import numpy as np
from mayavi import mlab

# Crear datos de ejemplo: un punto y un vector
origin = np.array([0, 0, 0])
vector = np.array([1, 2, 3])

# Graficar el punto
mlab.points3d(*origin, color=(1, 0, 0), scale_factor=0.5, mode='sphere')

# Graficar el vector como una flecha desde el origen
mlab.quiver3d(*origin, *vector, color=(0, 0, 1), scale_factor=1)

# Mostrar el gráfico en la ventana de Mayavi
mlab.show()
