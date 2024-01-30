import numpy as np
import sympy as sp

def grafica_superficie(ax, X, Y, Z, opc):
    if 'color' in opc and 'cmap' in opc:
        del opc['color']
    ax.plot_surface(X, Y, Z, **opc)

def grafica_sup_param_matplotlib(ax, sup, u, v, limite_inf_u=-10, limite_sup_u=10, limite_inf_v=-10, limite_sup_v=10, opc={}):
    parametric_surface = sp.lambdify((u, v), sup, 'numpy')
    u_values = np.linspace(float(limite_inf_u), float(limite_sup_u), 100)
    v_values = np.linspace(float(limite_inf_v), float(limite_sup_v), 100)
    u_values, v_values = np.meshgrid(u_values, v_values)
    X, Y, Z = parametric_surface(u_values, v_values)
    if np.isscalar(X):
        X = np.full_like(u_values, X)
    if np.isscalar(Y):
        Y = np.full_like(u_values, Y)
    if np.isscalar(Z):
        Z = np.full_like(u_values, Z)
    grafica_superficie(ax, X, Y, Z, opc)

def grafica_sup_ec_matplotlib(ax, sup, x, y, z, limite_inf_x=-10, limite_sup_x=10, limite_inf_y=-10, limite_sup_y=10, opc={}):
    x_values = np.linspace(limite_inf_x, limite_sup_x, 100)
    y_values = np.linspace(limite_inf_y, limite_sup_y, 100)
    X, Y = np.meshgrid(x_values, y_values)

    sol = sp.solve( sp.Eq(sup,0), z)
    if len(sol)>1:
        raise('Se se ha podido representar la superficie usando matplolib. Se recomienda usar mayavi')
    funcion_z = sp.lambdify((x, y), sol[0], 'numpy')
    Z = funcion_z(X, Y)
    if np.isscalar(Z):
        Z = np.full_like(X, Z)
    grafica_superficie(ax, X, Y, Z, opc)

def grafica_punto_matplotlib(ax, punto, opc):
    ax.scatter(punto[0],punto[1],punto[2],**opc)

    
def grafica_vector_matplotlib(ax, inicio, vector, opc):
    ax.quiver(inicio[0], inicio[1], inicio[2], vector[0], vector[1], vector[2], **opc)






