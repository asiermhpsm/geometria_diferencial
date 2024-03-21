import plotly.graph_objects as go
import numpy as np
import sympy as sp

from .calc_param import descripccion_pt_uv
from .calc_imp import tangente_pt, normal_pt
from .utils import xyz_to_uv

def sup_param(sup, u, v, 
                             limite_inf_u=-5, limite_sup_u=5, limite_inf_v=-5, limite_sup_v=5, 
                             fig=None, resolucion=100, titulo='Superficie', color=None):
    sup = list(sup)
    parametric_surface = sp.lambdify((u, v), sup, 'numpy')
    u_values, v_values = np.mgrid[float(limite_inf_u):float(limite_sup_u):resolucion*1j, 
                                  float(limite_inf_v):float(limite_sup_v):resolucion*1j]
    X, Y, Z = parametric_surface(u_values, v_values)
    if np.isscalar(X):
        X = np.full_like(u_values, X)
    if np.isscalar(Y):
        Y = np.full_like(u_values, Y)
    if np.isscalar(Z):
        Z = np.full_like(u_values, Z)
    if not fig:
        fig = go.Figure()
    if color:
        fig.add_trace(go.Surface(x=X, 
                             y=Y, 
                             z=Z, 
                             colorbar=dict(x=-0.1), 
                             name=titulo,
                             colorscale=[[0, color], [1, color]],
                             showlegend=True))
    else:
        fig.add_trace(go.Surface(x=X, 
                             y=Y, 
                             z=Z, 
                             colorbar=dict(x=-0.1), 
                             name=titulo,
                             showlegend=True))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def sup_imp(sup, x, y, z, 
                          limite_inf_x=-5, limite_sup_x=5, 
                          limite_inf_y=-5, limite_sup_y=5, 
                          limite_inf_z=-5, limite_sup_z=5, 
                          fig=None, color='blue', titulo='Superficie implicita', resolucion=75):
    parametric_surface = sp.lambdify((x, y, z), sup, 'numpy')
    X, Y, Z = np.mgrid[float(limite_inf_x):float(limite_sup_x):resolucion*1j, 
                       float(limite_inf_y):float(limite_sup_y):resolucion*1j, 
                       float(limite_inf_z):float(limite_sup_z):resolucion*1j]
    values = parametric_surface(X, Y, Z)
    if not fig:
        fig = go.Figure()
    fig.add_trace(go.Isosurface(
                    x=X.flatten(),
                    y=Y.flatten(),
                    z=Z.flatten(),
                    value=values.flatten(),
                    isomin=0,
                    isomax=0,
                    surface_count=1,
                    showscale=False,
                    name=titulo,
                    colorscale=[[0, color], [1, color]],
                    showlegend=True
                    ))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def point(punto, fig=None, titulo=None):
    punto = [float(elem) for elem in punto]
    if not fig:
        fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=[punto[0]], y=[punto[1]], z=[punto[2]], mode='markers', marker=dict(size=8, color='black'), name=titulo))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def vector(inicio, vector, fig=None, color='red', titulo=None):
    if not fig:
        fig = go.Figure()
    inicio = [float(comp) for comp in inicio]
    vector = [float(comp) for comp in vector]
    fig.add_trace(go.Scatter3d(x=[inicio[0], inicio[0]+vector[0]], 
                               y=[inicio[1], inicio[1]+vector[1]], 
                               z=[inicio[2], inicio[2]+vector[2]],  
                               mode='lines',
                               line=dict(width=5, color=color),
                               name=titulo))
    fig.add_cone(x=[inicio[0]+vector[0]], 
                               y=[inicio[1]+vector[1]], 
                               z=[inicio[2]+vector[2]], 
                               u=[vector[0]], 
                               v=[vector[1]], 
                               w=[vector[2]],
                               sizeref=0.2,
                               colorscale=[[0, color], [1, color]],
                               name=titulo,
                               showscale=False)
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def circulo(centro, radio, dir1, dir2, 
            fig=None, color='red', titulo='circulo'):
    centro = [float(elem) for elem in centro]
    radio = float(radio)
    dir1 = [float(elem) for elem in dir1.normalized()]
    dir2 = [float(elem) for elem in dir2.normalized()]
    theta = np.linspace(0, 2*np.pi, 100)
    x = centro[0] + radio*np.cos(theta)*dir1[0] + radio*np.sin(theta)*dir2[0]
    y = centro[1] + radio*np.cos(theta)*dir1[1] + radio*np.sin(theta)*dir2[1]
    z = centro[2] + radio*np.cos(theta)*dir1[2] + radio*np.sin(theta)*dir2[2]
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name=titulo, line=dict(color=color, width=5)))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def param_desc_pt_uv(sup, u, v, u0, v0, 
               limite_inf_u=-5, limite_sup_u=5, 
               limite_inf_v=-5, limite_sup_v=5, 
               fig=None):
    sup = sp.Matrix(sup).T

    fig = sup_param(sup, u, v, limite_inf_u, limite_sup_u, limite_inf_v, limite_sup_v, fig, titulo=r'$\vec{\varphi}='+sp.latex(sup)+r'$')
    fig.data[0].update(opacity=0.4)

    resultados = {
        'sup' : sup,
        'u' : u,
        'v' : v,
        'u0' : u0,
        'v0' : v0
    }
    resultados = descripccion_pt_uv(resultados)
    punto = sup.subs({u:u0, v:v0})

    u, v = sp.symbols('u v', real=True)
    plano = sp.Matrix([u*resultados['d1_pt'].normalized() + v*resultados['d2_pt'].normalized() + punto])
    fig = sup_param(plano, u, v, 
                    limite_inf_u=-1, limite_sup_u=1, 
                    limite_inf_v=-1, limite_sup_v=1, 
                    fig=fig, titulo='Plano tangente', color='grey')

    
    fig.data[1].update(opacity=0.6)

    fig = point(punto, fig=fig, titulo='Punto')
    fig = vector(punto, resultados['d1_pt'], fig, 'blue', r'$\vec{d_1}$')
    if resultados['k1_pt'] !=0:
        radio = 1/resultados['k1_pt']
        fig = circulo(punto + radio*resultados['normal_pt'].normalized(), 
                            radio,
                            resultados['normal_pt'],
                            resultados['d1_pt'],
                            fig, 'blue', r'$r=1/k_1$')
    
    fig = vector(punto, resultados['d2_pt'], fig, 'green', r'$\vec{d_2}$')
    if resultados['k2_pt'] !=0:
        radio = 1/resultados['k2_pt']
        fig = circulo(punto + radio*resultados['normal_pt'].normalized(), 
                            radio,
                            resultados['normal_pt'],
                            resultados['d2_pt'],
                            fig, 'green', r'$r=1/k_2$')
    
    fig = vector(punto, tuple(float(comp) for comp in resultados['normal_pt']), fig, 'red', r'$\vec{n}$')
    fig.update_layout(
        legend=dict(font=dict(size=15)), 
        scene=dict(aspectmode='data'),
        title={
            'text': f"<b>SUPERFICIE 3D. </b><br><span style='font-size: 12px;'>Pinchar en un elemento de la leyenda permite hacerlo aparecer o desaparecer.</span>",
            'font': {'size': 24, 'family': 'Arial'},
            'x': 0.5,
            'xanchor': 'center'
        })
    return fig

def param_desc_pt_xyz(sup, u, v, x0, y0, z0, 
                       limite_inf_u=-5, limite_sup_u=5, 
                       limite_inf_v=-5, limite_sup_v=5, 
                       fig=None):
    u0, v0 = xyz_to_uv(sup, u, v, x0, y0, z0)
    if isinstance(u0, sp.Symbol):
        u0 = limite_inf_u
    if isinstance(v0, sp.Symbol):
        v0 = limite_inf_v
    return param_desc_pt_uv(sup, u, v, u0, v0, 
                             limite_inf_u=limite_inf_u, limite_sup_u=limite_sup_u, 
                             limite_inf_v=limite_inf_v, limite_sup_v=limite_sup_v, 
                             fig=fig)

def imp_desc_pt(f, x, y, z, x0, y0, z0, 
                       limite_inf_x=-5, limite_sup_x=5, 
                       limite_inf_y=-5, limite_sup_y=5,
                       limite_inf_z=-5, limite_sup_z=5, 
                       fig=None):
    fig = sup_imp(f, x, y, z, 
                  limite_inf_x, limite_sup_x,
                  limite_inf_y, limite_sup_y, 
                  limite_inf_z, limite_sup_z,
                  titulo=r'$'+sp.latex(f)+r'=0$')
    fig.data[0].update(opacity=0.4)

    resultados = {
        'f' : f,
        'x' : x,
        'y' : y,
        'z' : z,
        'x0' : x0,
        'y0' : y0,
        'z0' : z0
    }

    resultados = normal_pt(resultados)
    resultados = tangente_pt(resultados)

    punto = (x0, y0, z0)

    fig = sup_imp(resultados['tangente_pt'].rhs - resultados['tangente_pt'].lhs, 
                  x, y, z,
                  punto[0]-1, punto[0]+1,
                  punto[1]-1, punto[1]+1,
                  punto[2]-1, punto[2]+1,
                  fig=fig, color='grey', titulo='Plano tangente')
    fig.data[1].update(opacity=0.6)

    fig = point(punto, fig=fig, titulo='Punto')
    fig = vector(punto, resultados['normal_pt'], fig, 'red', r'$\vec{n}$')

    return fig




"""
def ejemplo_sup():
    u, v = sp.symbols('u v')
    superficies_parametrizadas = []
    superficies_parametrizadas.append( ((sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v) , sp.sin(u)), -sp.pi/2, sp.pi/2, 0, 2*sp.pi) )
    superficies_parametrizadas.append( ((u, v, 0), -1, 1, -1, 1) )
    superficies_parametrizadas.append( ((sp.cos(u + v), sp.sin(u - v), u - v), 0, 2*sp.pi, 0, 2*sp.pi) )
    superficies_parametrizadas.append( ((sp.sin(u), sp.cos(u), v), 0, 2*sp.pi, 0, 2*sp.pi) )
    superficies_parametrizadas.append( ((u*sp.cos(v),u*sp.sin(v), 0), 0, 2*sp.pi, 0, 2*sp.pi) )
    superficies_parametrizadas.append( ((u+v, u*v, u-v), -1, 1, -1, 1) )
    superficies_parametrizadas.append( ((u**2+v, u-v**2, u), -1, 1, -1, 1) )
    superficies_parametrizadas.append( ((u, 0, v), -1, 1, -1, 1) )
    superficies_parametrizadas.append( ((u, u**2, v), -1, 1, -1, 1) )
    superficies_parametrizadas.append( ((sp.cos(u), sp.sin(u), v), 0, 2*sp.pi, 0, 2*sp.pi) )
    superficies_parametrizadas.append( ( ((1 + 2*sp.cos(u))*sp.cos(v), (1 + 2*sp.cos(u))*sp.sin(v), 2*sp.sin(u)), 0, 2*sp.pi, 0, 2*sp.pi) )
    superficies_parametrizadas.append( ((u, u**2 + v, v), -1, 1, -1, 1) )
    superficies_parametrizadas.append( ((sp.cosh(u)*sp.cos(v), sp.cosh(u)*sp.sin(v), sp.sinh(u)), 0, 2*sp.pi, 0, 2*sp.pi) )
    superficies_parametrizadas.append( ((u, v, u**2 + v**2), -1, 1, -1, 1) )
    superficies_parametrizadas.append( ((u*sp.cos(v), u*sp.sin(v), u**2), 0, 2*sp.pi, 0, 2*sp.pi) )
    superficies_parametrizadas.append( ((sp.cos(u)*sp.cos(v), -sp.cos(u)*sp.sin(v), 2*sp.sin(u)), 0, 2*sp.pi, 0, 2*sp.pi) )
    superficies_parametrizadas.append( ((u*sp.cos(v), u*sp.sin(v), (u**2)/2), 0, 2*sp.pi, 0, 2*sp.pi) )
    superficies_parametrizadas.append( ((sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v) , sp.sin(u)*sp.cos(v)), 0, 2*sp.pi, 0, 2*sp.pi) )
    superficies_parametrizadas.append( ((u, v, u**2+v**2), -1, 1, -1, 1) )
    superficies_parametrizadas.append( ((sp.sqrt(1+v**2)*sp.cos(u), sp.sqrt(1+v**2)*sp.sin(u), v), 0, 2*sp.pi, -5, 5) )
    superficies_parametrizadas.append( ((u, v, sp.sqrt(1-u**2-v**2)), -1, 1, -1, 1) )

    while True:
        i = int(input(f'Indica entero del 0 al {len(superficies_parametrizadas)-1}:'))
        sup, inf_u, sup_u, inf_v, sup_v = superficies_parametrizadas[i]
        u0 = float(input(f'Indica u0:'))
        v0 = float(input(f'Indica v0:'))
        fig = desc_punto(sup, u, v, u0, v0, inf_u, sup_u, inf_v, sup_v)
        fig.show()

        """