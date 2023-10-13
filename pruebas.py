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

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from matplotlib import cm
from matplotlib.ticker import LinearLocator

def sup_color():
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.3)
    X, Y = np.meshgrid(X, Y)
    print('X', X)
    print('Y', Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    print('Z', Z)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

#sup_color()


def bola_unidad_3d():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Make data
    u = np.linspace(0, 2*np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 10 * np.outer(np.cos(u), np.sin(v))
    print('X',x)
    y = 10 * np.outer(np.sin(u), np.sin(v))
    print('Y',y)
    z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))
    print('Z',z)

    # Plot the surface
    ax.plot_surface(x, y, z)

    # Set an equal aspect ratio
    ax.set_aspect('equal')

    plt.show()

#bola_unidad_3d()

def grafica_superficie(funciones):
    # Estandarizo funciones
    u, v = sp.symbols('u v')
    parametrizacion = [sp.sympify(func) for func in funciones]

    n_puntos=100
    
    # Establezco límites
    u_values = np.linspace(-np.pi/2, np.pi/2, n_puntos)
    v_values = np.linspace(0, 2*np.pi, n_puntos)

    X = []
    Y = []
    Z = []

    for u_value in u_values:
        x_aux = []
        y_aux = []
        z_aux = []
        for v_value in v_values:
            x_aux.append(float(parametrizacion[0].subs({u: u_value, v: v_value})))
            y_aux.append(float(parametrizacion[1].subs({u: u_value, v: v_value})))
            z_aux.append(float(parametrizacion[2].subs({u: u_value, v: v_value})))
        X.append(x_aux)
        Y.append(y_aux)
        Z.append(z_aux)
    
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)


    #Creo grafica
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(X, Y, Z)
    ax.set_aspect('equal')

    plt.show()

    


#grafica_superficie(['cos(u)*cos(v)', 'cos(u)*sin(v)', 'sin(v)'])