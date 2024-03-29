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
    #ax.figure.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

def grafica_sup_param(ax, sup, u, v, limite_inf_u, limite_sup_u, limite_inf_v, limite_sup_v, opc):
    parametric_surface = sp.lambdify((u, v), sup, 'numpy')
    u_values = np.linspace(float(limite_inf_u), float(limite_sup_u), 100)
    v_values = np.linspace(float(limite_inf_v), float(limite_sup_v), 100)
    u_values, v_values = np.meshgrid(u_values, v_values)
    X, Y, Z = parametric_surface(u_values, v_values)

def grafica_sup_ec(ax, sup, x, y, z, opc, limite_inf_x=-1, limite_sup_x=1, limite_inf_y=-1, limite_sup_y=1):
    soluciones = sp.solve(sp.Eq(sup, 0), z)
    x_values = np.linspace(limite_inf_x, limite_sup_x, 100)
    y_values = np.linspace(limite_inf_y, limite_sup_y, 100)
    x_values, y_values = np.meshgrid(x_values, y_values)
    X = np.array([])
    Y = np.array([])
    Z = np.array([])
    for sol in soluciones:
        parametric_surface = sp.lambdify((x, y), sol, 'numpy')
        z_values = parametric_surface(x_values, y_values)
        if not X.size:
            X = x_values.copy()
            Y = y_values.copy()
            Z = z_values.copy()
        else:
            X = np.vstack((X, x_values))
            Y = np.vstack((Y, y_values))
            Z = np.vstack((Z, z_values))
    union = sp.solve(sp.Eq(soluciones[0], soluciones[1]), y)
    f_union = sp.lambdify(x, union[0], 'numpy')
    y_valores_union = f_union(x_values)
    z_values = parametric_surface(x_values, y_valores_union)
    X = np.vstack((X, x_values))
    Y = np.vstack((Y, y_valores_union))
    Z = np.vstack((Z, z_values))

    grafica_superficie(ax, X, Y, Z, opc)
        
    

def grafica_punto(ax, punto, opc):
    ax.scatter(punto[0],punto[1],punto[2],**opc)
    
def grafica_vector(ax, inicio, vector, opc):
    ax.quiver(inicio[0], inicio[1], inicio[2], vector[0], vector[1], vector[2], **opc)

u, v = sp.symbols('u v')
x, y, z = sp.symbols('x y z')

parametrizacion = (sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v) , sp.sin(u))
limite_inf_u = -sp.pi/2
limite_sup_u = sp.pi/2
limite_inf_v = 0
limite_sup_v = 2*sp.pi

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

arg_opc = {}
#arg_opc['cmap'] = 'Blues'
#arg_opc['color'] = 'xkcd:boring green'
#arg_opc['alpha'] = 1
#arg_opc['norm'] = mcolors.Normalize(vmin=-1, vmax=4)
#arg_opc['linewidth'] = 0.5
#arg_opc['edgecolors'] = 'k'
#arg_opc['linestyles'] = 'solid'
#arg_opc['shade'] = False
#grafica_sup_param(ax,parametrizacion,u,v,limite_inf_u,limite_sup_u,limite_inf_v,limite_sup_v,arg_opc)


plano = x**2 + y**2 +z**2 - 1
#plano = z - 1
arg_opc2 = {}
#arg_opc2['cmap'] = 'Blues'
#arg_opc2['color'] = 'grey'
#arg_opc2['alpha'] = 1
#arg_opc2['norm'] = mcolors.Normalize(vmin=-1, vmax=1)
#arg_opc2['linewidth'] = 0.5
#arg_opc2['edgecolors'] = 'k'
#arg_opc2['linestyles'] = 'solid'
#arg_opc2['shade'] = False
grafica_sup_ec(ax,plano,x,y,z,arg_opc2)


arg_opc3 = {}
arg_opc3['s'] = 40
arg_opc3['color'] = 'black'
arg_opc3['alpha'] = 1
#arg_opc3['marker'] = '*'
#arg_opc3['edgecolors'] = 'yellow'
#grafica_punto(ax,(0,0,1),arg_opc3)


arg_opc4 = {}
arg_opc4['color'] = 'red'
arg_opc4['linewidth'] = 2
#arg_opc3['marker'] = '*'
#arg_opc3['edgecolors'] = 'yellow'
#grafica_vector(ax,(0,0,1), (0,0,1), arg_opc4)


ax.set_aspect('equal')
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('Eje Z')


plt.show()