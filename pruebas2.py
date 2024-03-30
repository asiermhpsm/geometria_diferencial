import numpy as np
import plotly.graph_objects as go
import sympy as sp

def genera_malla(a, b, num_points):
    #Genera la malla del conjunto a*u^2 + b*v^2 < 1
    t = np.linspace(0, 2 * np.pi, num_points)
    r = np.linspace(0, 0.98, num_points)
    T, R = np.meshgrid(t, r)
    X = 1/np.sqrt(float(a)) * R * np.cos(T)
    Y = 1/np.sqrt(float(b))* R * np.sin(T)
    return X, Y


u, v = sp.symbols('u v', real=True)
sup = [u, v, sp.sqrt(1-u**2-v**2)]
parametric_surface = sp.lambdify((u, v), sup, 'numpy')
u_values, v_values = genera_malla(1, 1, 100)
X, Y, Z = parametric_surface(u_values, v_values)
if np.isscalar(X):
    X = np.full_like(u_values, X)
if np.isscalar(Y):
    Y = np.full_like(u_values, Y)
if np.isscalar(Z):
    Z = np.full_like(u_values, Z)
print(X)
print(Y)
print(Z)
fig = go.Figure()
fig.add_trace(go.Surface(x=X, y=Y, z=Z))
fig.update_layout(scene=dict(aspectmode='data'))
fig.show()