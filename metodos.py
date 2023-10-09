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

def sustParam(u_values, v_values, func):
    if (isinstance(u_values, list) and all( (isinstance(u_value, float) or isinstance(u_value, int)) for u_value in u_values)) and (isinstance(v_values, list) and all( (isinstance(v_value, float) or isinstance(v_value, int)) for v_value in v_values)):
        func.subs({u: u_values, v: u_values})

def grafica_superficie(funciones):
    # Estandarizo funciones
    u, v = sp.symbols('u v')
    parametrizacion = [sp.sympify(func) for func in funciones]
    print(type(parametrizacion[0]))

    n_puntos=100
    
    # Establezco límites
    u_values = np.linspace(-np.pi/2, np.pi/2, n_puntos)
    u_values = np.linspace(0, 2*np.pi, n_puntos)

    X, Y = np.meshgrid(parametrizacion[0].subs({u: u_values, v: u_values}), parametrizacion[1].subs({u: u_values, v: u_values}))
    print(X)
    print(Y)

    """
    x=[]
    y=[]
    z=[]
    for u_val in u_values:
        x_aux = []
        y_aux = []
        z_aux = []
        for v_val in v_values:
            x_aux.append(10*parametrizacion[0].subs({u: u_val, v: v_val}))
            y_aux.append(10*parametrizacion[1].subs({u: u_val, v: v_val}))
            z_aux.append(10*parametrizacion[2].subs({u: u_val, v: v_val}))
        x.append(x_aux)
        y.append(y_aux)
        z.append(z_aux)
    
    x=np.array(x)
    y=np.array(y)
    z=np.array(z)

    print('X', x)
    print('Y',y)
    print('Z', z)
    """
    """
    #Creo grafica
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(x, y, z)
    ax.set_aspect('equal')

    plt.show()
    """


grafica_superficie(['cos(u)*cos(v)', 'cos(u)*sin(v)', 'sin(u)'])