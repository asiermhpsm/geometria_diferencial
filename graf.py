import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib import cm

from points import uv_to_xyz
from geoDiff import normal, normal_pt_uv, normal_pt_xyz, planoTangente, planoTangente_pt_uv, planoTangente_pt_xyz

def representa_3d(*args):
    """
    Representa todas lassuperficies que se pasan como parametros
    No se hacen comprobaciones de tipo

    Argumentos:
    tipo1               tipo de figura (superficie, punto, vector)
    X1                  vector 2D que se debe pasar a ax.plot_surface()
    Y1                  vector 2D que se debe pasar a ax.plot_surface()
    Z1                  vector 2D que se debe pasar a ax.plot_surface()
    opcion1             depende de tipo de representacion: color_map(booleano para representar con mapa de color), marker('o' predeterminado)
    color1              color de la superficie
    ...
    tipoN               tipo de figura (superficie, punto, vector)
    XN                  vector 2D que se debe pasar a ax.plot_surface()
    YN                  vector 2D que se debe pasar a ax.plot_surface()
    ZN                  vector 2D que se debe pasar a ax.plot_surface()
    opcionN             depende de tipo de representacion: color_map(booleano para representar con mapa de color), marker('o' predeterminado)
    colorN              color de la superficie
    """

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    for i in range(0, len(args), 6):
        tipo, X, Y, Z, opcion, color = args[i], args[i + 1], args[i + 2], args[i + 3], args[i + 4], args[i + 5]
        if tipo == 'superficie':
            if opcion:
                surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
                fig.colorbar(surf, shrink=0.5, aspect=5)
            elif color is None:
                ax.plot_surface(X, Y, Z)
            else:
                ax.plot_surface(X, Y, Z, color=color)
        elif tipo == 'punto':
            ax.scatter(X, Y, Z, c=color, marker=opcion, s=100)   
        elif tipo == 'vector':
            print()  
    ax.set_aspect('equal')
    plt.show()


def procesa_sup_uv(parametrizacion, u, v, limite_inf_u, limite_sup_u, limite_inf_v, limite_sup_v, color_map=False, color=None, resolucion=50):
    """
    Devuelve los valores X, Y, Z, cmap, color que se deben pasar a la funcion ax.plot_surface() para representar la superficie, ademas del tipo de figura (superficie)
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    limite_inf_u        limite inferior de la variable u
    limite_sup_u        limite superior de la variable u
    limite_inf_v        limite inferior de la variable v
    limite_sup_v        limite superior de la variable v
    color_map           booleano para representar con mapa de calor
    color               opcional, color de la superficie
    resolucion          resolucion con la que se grafica la superficie (50 significa 50x50 puntos)
    """
    # Establezco límites
    u_values = np.linspace(limite_inf_u, limite_sup_u, resolucion)
    v_values = np.linspace(limite_inf_v, limite_sup_v, resolucion)

    X = np.array([[float(parametrizacion[0].subs([[u, u_value],[v,v_value]])) for v_value in v_values] for u_value in u_values])
    Y = np.array([[float(parametrizacion[1].subs([[u, u_value],[v,v_value]])) for v_value in v_values] for u_value in u_values])
    Z = np.array([[float(parametrizacion[2].subs([[u, u_value],[v,v_value]])) for v_value in v_values] for u_value in u_values])

    return 'superficie', X, Y, Z, color_map, color

def procesa_plano_xyz(plano, x, y, z, limite_inf_x, limite_sup_x, limite_inf_y, limite_sup_y, color_map=False, color='grey', resolucion=20):
    """
    Devuelve los valores X, Y, Z, cmap que se deben pasar a la funcion ax.plot_surface() para representar el plano tangente
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     ecuacion del plano (de la forma a*x+b*y+c*z)
    x                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    y                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    z                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    limite_inf_x        limite inferior de la variable x
    limite_sup_x        limite superior de la variable x
    limite_inf_y        limite inferior de la variable y
    limite_sup_y        limite superior de la variable y
    nivel_color         booleano para representar con mapa de calor
    resolucion          resolucion con la que se grafica la superficie (20 significa 20x20 puntos)
    """
    x_values = np.linspace(limite_inf_x, limite_sup_x, resolucion)
    y_values = np.linspace(limite_inf_y, limite_sup_y, resolucion)
    X, Y = np.meshgrid(x_values, y_values)

    Z = np.array([[sp.solve(plano.subs([[x, x_value],[y,y_value]]), z)[0] for y_value in y_values] for x_value in x_values])

    return 'superficie',X, Y, Z, color_map, color

def procesa_punto_uv(parametrizacion, u, v, u0, v0, color='black', marker='o'):
    """
    Devuelve los valores X, Y, Z, marker, color que se deben pasar a la funcion ax.scatter() para representar el punto
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     ecuacion del plano (de la forma a*x+b*y+c*z)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    color               opcional, color del plano
    """
    X, Y, Z = uv_to_xyz(parametrizacion, u, v, u0, v0)
    return 'punto',X, Y, Z, marker, color

def procesa_punto_xyz(x0, y0, z0, color='black', marker='o'):
    """
    Devuelve los valores X, Y, Z, marker, color que se deben pasar a la funcion ax.scatter() para representar el punto
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     ecuacion del plano (de la forma a*x+b*y+c*z)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    color               opcional, color del plano
    """
    return 'punto',x0, y0, z0, marker, color