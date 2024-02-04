import plotly.graph_objects as go
import numpy as np
import sympy as sp

def grafica_sup_param_plotly(sup, u, v, limite_inf_u=-5, limite_sup_u=5, limite_inf_v=-5, limite_sup_v=5, fig=None):
    parametric_surface = sp.lambdify((u, v), sup, 'numpy')
    u_values, v_values = np.mgrid[float(limite_inf_u):float(limite_sup_u):100j, float(limite_inf_v):float(limite_sup_v):100j]
    X, Y, Z = parametric_surface(u_values, v_values)
    if np.isscalar(X):
        X = np.full_like(u_values, X)
    if np.isscalar(Y):
        Y = np.full_like(u_values, Y)
    if np.isscalar(Z):
        Z = np.full_like(u_values, Z)
    
    if fig:
        fig.add_trace(go.Surface(x=X, y=Y, z=Z))
    else:
        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z)])
    return fig

def grafica_sup_ec_plotly(sup, x, y, z, limite_inf_x=-10, limite_sup_x=10, limite_inf_y=-10, limite_sup_y=10, limite_inf_z=-10, limite_sup_z=10,fig=None):
    parametric_surface = sp.lambdify((x, y, z), sup, 'numpy')
    X, Y, Z = np.mgrid[float(limite_inf_x):float(limite_sup_x):75j, float(limite_inf_y):float(limite_sup_y):75j, float(limite_inf_z):float(limite_sup_z):75j]
    values = parametric_surface(X, Y, Z)

    if fig:
        fig.add_trace(go.Isosurface(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            value=values.flatten(),
            isomin=0,
            isomax=0,
            surface_count=1,
            ))
    else:
        fig = go.Figure(data=[go.Isosurface(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            value=values.flatten(),
            isomin=0,
            isomax=0,
            surface_count=1,
            )])
        
    return fig

def grafica_punto_plotly(punto, fig=None):
    if not fig:
        fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=[punto[0]], y=[punto[1]], z=[punto[2]],  marker=dict(size=8)))

def grafica_vector_plotly(inicio, vector, fig=None):
    #Se asume vector unitario
    if not fig:
        fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=[inicio[0], inicio[0]+vector[0]], 
                               y=[inicio[1], inicio[1]+vector[1]], 
                               z=[inicio[2], inicio[2]+vector[2]],  
                               mode='lines',
                               line=dict(width=5, color='red')))
    fig.add_trace(go.Cone(x=[inicio[0]+vector[0]], 
                               y=[inicio[1]+vector[1]], 
                               z=[inicio[2]+vector[2]], 
                               u=[vector[0]], 
                               v=[vector[1]], 
                               w=[vector[2]],
                               sizeref=0.1,
                               colorscale=[[0, 'red'], [1, 'red']]))




u, v = sp.symbols('u v')
x, y, z = sp.symbols('x, y, z')

fig = go.Figure()

"""sup0 = [sp.sin(v)*sp.cos(u), sp.sin(v)*sp.sin(u), sp.cos(v)]
fig = grafica_sup_param_plotly(sup0, u, v, 0, 2*sp.pi, 0, sp.pi, fig)

sup1 = [sp.sin(v)*sp.cos(u) + 2, sp.sin(v)*sp.sin(u) + 2, sp.cos(v) + 2]
fig = grafica_sup_param_plotly(sup1, u, v, 0, 2*sp.pi, 0, sp.pi, fig)

sup2 = [sp.sin(v)*sp.cos(u) - 2, sp.sin(v)*sp.sin(u) - 2, sp.cos(v) - 2]
fig = grafica_sup_param_plotly(sup2, u, v, 0, 2*sp.pi, 0, sp.pi, fig)"""

sup3 = (x/3)**2 + (y/2)**2 + (z/1)**2 - 1
fig = grafica_sup_ec_plotly(sup3, x, y, z, -4, 4, -4, 4, -4, 4, fig)

#grafica_punto_plotly((0,0,1),fig)
#grafica_vector_plotly((0,0,1), (0,0,1),fig)

fig.update_layout(
    scene=dict(
        aspectmode='data',
        aspectratio=dict(x=1, y=1, z=1)
    )
)
fig.show()
