import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def bola_unidad_3d():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Make data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 10 * np.outer(np.cos(u), np.sin(v))
    y = 10 * np.outer(np.sin(u), np.sin(v))
    z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

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
    
    # Establezco límites
    u_values = np.linspace(-np.pi/2, np.pi/2, 100)
    v_values = np.linspace(0, 2*np.pi, 100)
    
    resultados = np.zeros((len(u_values), len(v_values), len(parametrizacion)))
    for i, u_val in enumerate(u_values):
        for j, v_val in enumerate(v_values):
            result = [sp.N(func.subs({u: u_val, v: v_val})) for func in parametrizacion]
            resultados[i, j, :] = result
    print(resultados)
    x = 10 * np.outer( sp.N(parametrizacion[0].subs(u: u_val)), sp.N(parametrizacion[0].subs(v: v_val)) )
    y = 10 * np.outer(np.sin(u), np.sin(v))
    z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

    #Creo grafica
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(x, y, z)
    ax.set_aspect('equal')

    plt.show()

grafica_superficie(['cos(u)*sin(v)', 'cos(u)*sin(v)', 'sin(u)'])