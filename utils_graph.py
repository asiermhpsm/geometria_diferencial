import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

from matplotlib import colormaps
import matplotlib.colors as mcolors

colormapas = list(colormaps)
colores = list(mcolors.BASE_COLORS.keys())+list(mcolors.TABLEAU_COLORS.keys()) + list(mcolors.CSS4_COLORS.keys()) + list(mcolors.XKCD_COLORS.keys())

def grafica_superficie(ax, X, Y, Z, opc):
    if 'color' in opc and 'cmap' in opc:
        del opc['color']
    surf = ax.plot_surface(X, Y, Z, **opc)
    ax.figure.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

def grafica_sup_param(ax, sup, u, v, limite_inf_u, limite_sup_u, limite_inf_v, limite_sup_v, opc):
    u_values = np.linspace(float(limite_inf_u), float(limite_sup_u), 100)
    v_values = np.linspace(float(limite_inf_v), float(limite_sup_v), 100)

    X = np.array([[float(sup[0].subs([[u, u_value], [v, v_value]])) for v_value in v_values] for u_value in u_values])
    Y = np.array([[float(sup[1].subs([[u, u_value], [v, v_value]])) for v_value in v_values] for u_value in u_values])
    Z = np.array([[float(sup[2].subs([[u, u_value], [v, v_value]])) for v_value in v_values] for u_value in u_values])

    grafica_superficie(ax, X, Y, Z, opc)

def grafica_sup_ec(ax, sup, x, y, z, limite_inf_x, limite_sup_x, limite_inf_y, limite_sup_y, opc):
    x_values = np.linspace(limite_inf_x, limite_sup_x, 100)
    y_values = np.linspace(limite_inf_y, limite_sup_y, 100)
    X, Y = np.meshgrid(x_values, y_values)

    ecuacion_resulta = sp.solve( sp.Eq(sup,0), z)
    for sol in ecuacion_resulta:
        funcion_z = sp.lambdify((x, y), sol, 'numpy')
        Z = funcion_z(X, Y)
        if np.isscalar(Z):
            Z = np.full_like(X, Z)
        grafica_superficie(ax, X, Y, Z, opc)

def grafica_punto(ax, punto, opc):
    ax.scatter(punto[0],punto[1],punto[2],**opc)

#TODO: graficar punto uv de superficie
    
def grafica_vector(ax, inicio, vector, opc):
    ax.quiver(inicio[0], inicio[1], inicio[2], vector[0], vector[1], vector[2], **opc)

#TODO: graficar vector segun uv de superficie





