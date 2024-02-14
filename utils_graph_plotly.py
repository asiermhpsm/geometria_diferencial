import plotly.graph_objects as go
import numpy as np
import sympy as sp
from utils import descripccion_pt_uv, norm, normaliza, xyz_to_uv

def grafica_sup_param_plotly(sup, u, v, 
                             limite_inf_u=-5, limite_sup_u=5, limite_inf_v=-5, limite_sup_v=5, 
                             fig=None, resolucion=100, titulo='Superficie'):
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
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorbar=dict(x=-0.1), name=titulo, showlegend=True))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def grafica_sup_ec_plotly(sup, x, y, z, 
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

def grafica_punto_plotly(punto, fig=None, titulo=None):
    punto = [float(elem) for elem in punto]
    if not fig:
        fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=[punto[0]], y=[punto[1]], z=[punto[2]], mode='markers', marker=dict(size=8, color='black'), name=titulo))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def grafica_vector_plotly(inicio, vector, fig=None, color='red', titulo='vector'):
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

def grafica_circulo(centro, radio, dir1, dir2, fig=None, color='red', titulo='circulo'):
    centro = [float(elem) for elem in centro]
    radio = float(radio)
    dir1 = [float(elem) for elem in normaliza(dir1)]
    dir2 = [float(elem) for elem in normaliza(dir2)]
    theta = np.linspace(0, 2*np.pi, 100)
    x = centro[0] + radio*np.cos(theta)*dir1[0] + radio*np.sin(theta)*dir2[0]
    y = centro[1] + radio*np.cos(theta)*dir1[1] + radio*np.sin(theta)*dir2[1]
    z = centro[2] + radio*np.cos(theta)*dir1[2] + radio*np.sin(theta)*dir2[2]
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name=titulo, line=dict(color=color, width=5)))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def anade_descr_pt_uv(sup, u, v, u0, v0, limite_inf_u=-5, limite_sup_u=5, limite_inf_v=-5, limite_sup_v=5, fig=None):
    sup = sp.Matrix(sup)

    fig = grafica_sup_param_plotly(sup, u, v, limite_inf_u, limite_sup_u, limite_inf_v, limite_sup_v, fig)
    fig.data[0].update(opacity=0.4)

    resultados = {}
    resultados = descripccion_pt_uv(sup, u, v, u0, v0, resultados)
    punto = sup.subs({u:u0, v:v0})

    x, y, z = sp.symbols('x y z')
    tamaño_plano = max(float(norm(resultados['du_pt'])), float(norm(resultados['dv_pt'])))
    grafica_sup_ec_plotly(resultados['tangente_afin_pt'].lhs-resultados['tangente_afin_pt'].rhs, 
                          x, y, z, 
                          limite_inf_x=punto[0]-tamaño_plano, limite_sup_x=punto[0]+tamaño_plano, 
                          limite_inf_y=punto[1]-tamaño_plano, limite_sup_y=punto[1]+tamaño_plano, 
                          limite_inf_z=punto[2]-tamaño_plano, limite_sup_z=punto[2]+tamaño_plano,
                          fig=fig, color='grey', titulo='Plano tangente', resolucion=30)
    fig.data[1].update(opacity=0.6)

    fig = grafica_punto_plotly(punto, fig=fig, titulo='Punto')
    fig = grafica_vector_plotly(punto, resultados['du_pt'], fig, 'blue', r'$\vec{\varphi_u}$')
    if resultados['k1_pt'] !=0:
        radio = 1/resultados['k1_pt']
        fig = grafica_circulo(punto + radio*normaliza(resultados['normal_pt']), 
                            radio,
                            resultados['normal_pt'],
                            resultados['du_pt'],
                            fig, 'blue', r'$r=1/k_1$')
    
    fig = grafica_vector_plotly(punto, resultados['dv_pt'], fig, 'green', r'$\vec{\varphi_v}$')
    if resultados['k2_pt'] !=0:
        radio = 1/resultados['k2_pt']
        fig = grafica_circulo(punto + radio*normaliza(resultados['normal_pt']), 
                            radio,
                            resultados['normal_pt'],
                            resultados['dv_pt'],
                            fig, 'green', r'$r=1/k_2$')
    
    fig = grafica_vector_plotly(punto, tuple(float(comp) for comp in resultados['normal_pt']), fig, 'red', r'$\vec{n}$')
    fig.update_layout(
        legend=dict(font=dict(size=15)), 
        scene=dict(aspectmode='data'),
        title={
            'text': "<b>SUPERFICIES 3D</b><br><span style='font-size: 12px;'>Pinchar en un elemento de la leyenda permite hacerlo aparecer o desaparecer.</span>",
            'font': {'size': 24, 'family': 'Arial'},
            'x': 0.5,
            'xanchor': 'center'
        })
    return fig

def anade_descr_pt_xyz(sup, u, v, x0, y0, z0, limite_inf_u=-5, limite_sup_u=5, limite_inf_v=-5, limite_sup_v=5, fig=None):
    u0, v0 = xyz_to_uv(sup, u, v, x0, y0, z0)
    if isinstance(u0, sp.Symbol):
        u0 = limite_inf_u
    if isinstance(v0, sp.Symbol):
        v0 = limite_inf_v
    return anade_descr_pt_uv(sup, u, v, u0, v0, 
                             limite_inf_u=limite_inf_u, limite_sup_u=limite_sup_u, 
                             limite_inf_v=limite_inf_v, limite_sup_v=limite_sup_v, 
                             fig=fig)



"""u, v = sp.symbols('u v')
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

while True:
    i = int(input(f'Indica entero del 0 al {len(superficies_parametrizadas)-1}:'))
    sup, inf_u, sup_u, inf_v, sup_v = superficies_parametrizadas[i]
    u0 = float(input(f'Indica u0:'))
    v0 = float(input(f'Indica v0:'))
    fig = anade_descr_pt_uv(sup, u, v, u0, v0, inf_u, sup_u, inf_v, sup_v)
    fig.show()"""