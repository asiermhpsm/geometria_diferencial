import plotly.graph_objects as go
import numpy as np
import sympy as sp

from .calc_param import descripccion_pt_uv
from .calc_imp import tangente_pt, normal_pt
from .utils import xyz_to_uv

"""
-------------------------------------------------------------------------------
METODOS AUXILIARES
-------------------------------------------------------------------------------
"""
def point(punto, fig=None, titulo=None):
    """
    Dibuja un punto en el espacio
    Argumentos:
    punto       coordenadas del punto (cualquier tipo que se pueda transformar a lista de float)
    fig         figura de plotly donde se añadirá el punto
    titulo      nombre del punto
    """
    punto = [float(elem) for elem in punto]
    if not fig:
        fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=[punto[0]],
            y=[punto[1]],
            z=[punto[2]],
            mode='markers',
            marker=dict(size=8, color='black'),
            name=titulo))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def vector(inicio, vector, fig=None, color='red', titulo=None):
    """
    Dibuja un vector en el espacio
    Argumentos:
    inicio      coordenadas del punto de inicio del vector (cualquier tipo que se pueda transformar a lista de float)
    vector      coordenadas del vector (cualquier tipo que se pueda transformar a lista de float)
    fig         figura de plotly donde se añadirá el vector
    color       color del vector
    titulo      nombre del vector
    """
    if not fig: fig = go.Figure()
    inicio = [float(comp) for comp in inicio]
    vector = [float(comp) for comp in vector]
    fig.add_trace(
        go.Scatter3d(x=[inicio[0], inicio[0]+vector[0]],
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

def circulo(centro, radio, dir1, dir2, fig=None, color='red', titulo='circulo'):
    """
    Dibuja un círculo en el espacio 3D que contenga los vectotes dir1 y dir2
    Argumentos:
    centro      coordenadas del centro del círculo (cualquier tipo que se pueda transformar a lista de float)
    radio       radio del círculo
    dir1        vector director 1 del círculo
    dir2        vector director 2 del círculo
    fig         figura de plotly donde se añadirá el círculo
    color       color del círculo
    titulo      nombre del círculo
    """
    centro = [float(elem) for elem in centro]
    radio = float(radio)
    dir1 = [float(elem) for elem in dir1.normalized()]
    dir2 = [float(elem) for elem in dir2.normalized()]
    theta = np.linspace(0, 2*np.pi, 100)
    x = centro[0] + radio*np.cos(theta)*dir1[0] + radio*np.sin(theta)*dir2[0]
    y = centro[1] + radio*np.cos(theta)*dir1[1] + radio*np.sin(theta)*dir2[1]
    z = centro[2] + radio*np.cos(theta)*dir1[2] + radio*np.sin(theta)*dir2[2]
    fig.add_trace(
        go.Scatter3d(x=x, y=y, z=z, 
                     mode='lines', 
                     name=titulo, 
                     line=dict(color=color, width=5)))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def genera_malla_elipse(a, b, num_points):
    """
    Genera la malla del conjunto a*u^2 + b*v^2 < 1
    Argumentos:
    a           semieje a
    b           semieje b
    num_points  resolución de la malla
    """
    t = np.linspace(0, 2 * np.pi, num_points)
    r = np.linspace(0, 0.98, num_points)
    T, R = np.meshgrid(t, r)
    X = 1/np.sqrt(float(a)) * R * np.cos(T)
    Y = 1/np.sqrt(float(b)) * R * np.sin(T)
    return X, Y


"""
-------------------------------------------------------------------------------
SUPERFICIES PARAMÉTRICAS
-------------------------------------------------------------------------------
"""
def sup_param(sup, u, v, dom_u=sp.Interval(-5,5), dom_v=sp.Interval(-5,5), 
              fig=None, resolucion=100, titulo='Superficie', color=None):
    """
    Grafica una superficie paramétrica
    Argumentos:
    sup         superficie paramétrica
    u           primera variable de dependencia
    v           segunda variable de dependencia
    dom_u       dominio de la primera variable
    dom_v       dominio de la segunda variable
    fig         figura de plotly donde se añadirá la superficie
    resolucion  resolución de la malla
    titulo      nombre de la superficie
    color       color de la superficie
    """
    sup = list(sup)
    parametric_surface = sp.lambdify((u, v), sup, 'numpy')
    u_values, v_values = np.mgrid[float(dom_u.start):float(dom_u.end):resolucion*1j, 
                                  float(dom_v.start):float(dom_v.end):resolucion*1j]
    X, Y, Z = parametric_surface(u_values, v_values)
    if np.isscalar(X): X = np.full_like(u_values, X)
    if np.isscalar(Y): Y = np.full_like(u_values, Y)
    if np.isscalar(Z): Z = np.full_like(u_values, Z)
    if not fig: fig = go.Figure()
    if color:
        fig.add_trace(
            go.Surface(x=X, y=Y, z=Z,
                       colorbar=dict(x=-0.1),
                       name=titulo,
                       colorscale=[[0, color], [1, color]],
                       showlegend=True))
    else:
        fig.add_trace(
            go.Surface(x=X, y=Y, z=Z,
                       colorbar=dict(x=-0.1),
                       name=titulo,
                       showlegend=True))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def param_desc_pt_uv(sup, u, v, u0, v0, dom_u=sp.Interval(-5,5), dom_v=sp.Interval(-5,5), fig=None):
    """
    Dada una superficie paramétrica, pinta la superficie, el plano tangente, el vector normal 
    y las direcciones principales en un punto que depende de las variables u y v
    Argumentos:
    sup         superficie paramétrica
    u           primera variable de dependencia
    v           segunda variable de dependencia
    u0          valor de u en el punto
    v0          valor de v en el punto
    dom_u       dominio de la primera variable
    dom_v       dominio de la segunda variable
    fig         figura de plotly donde se añadirá la superficie
    """
    sup = sp.Matrix(sup).T
    fig = sup_param(sup, u, v, dom_u, dom_v, fig=fig, titulo=r'$\vec{\varphi}='+sp.latex(sup)+r'$')
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

    #u, v = sp.symbols('u v', real=True)
    plano = sp.Matrix([u*resultados['d1_pt'].normalized() + v*resultados['d2_pt'].normalized() + punto])
    fig = sup_param(plano, u, v, dom_u=sp.Interval(-1,1), dom_v=sp.Interval(-1,1), 
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

def param_desc_pt_xyz(sup, u, v, x0, y0, z0, dom_u=sp.Interval(-5,5), dom_v=sp.Interval(-5,5), fig=None):
    """
    Dada una superficie paramétrica, pinta la superficie, el plano tangente, el vector normal 
    y las direcciones principales en un punto que depende de las variables x, y, z
    Argumentos:
    sup         superficie paramétrica
    u           primera variable de dependencia
    v           segunda variable de dependencia
    x0          valor de x en el punto
    y0          valor de y en el punto
    z0          valor de z en el punto
    dom_u       dominio de la primera variable
    dom_v       dominio de la segunda variable
    fig         figura de plotly donde se añadirá la superficie
    """
    u0, v0 = xyz_to_uv(sup, u, v, x0, y0, z0)
    return param_desc_pt_uv(sup, u, v, u0, v0, dom_u=dom_u, dom_v=dom_v, fig=fig)

def sup_param_cond_elipse(sup, u, v, a, b ,fig=None, resolucion=100, titulo='Superficie'):
    """
    Grafica una superficie paramétrica con restricción de elipse (a*u^2 + b*v^2 < 1)
    Argumentos:
    sup         superficie paramétrica
    u           primera variable de dependencia
    v           segunda variable de dependencia
    a           semieje a
    b           semieje b
    fig         figura de plotly donde se añadirá la superficie
    """
    sup = list(sup)
    parametric_surface = sp.lambdify((u, v), sup, 'numpy')
    u_values, v_values = genera_malla_elipse(a, b, resolucion)
    X, Y, Z = parametric_surface(u_values, v_values)
    if np.isscalar(X): X = np.full_like(u_values, X)
    if np.isscalar(Y): Y = np.full_like(u_values, Y)
    if np.isscalar(Z): Z = np.full_like(u_values, Z)
    if not fig: fig = go.Figure()
    fig.add_trace(go.Surface(x=X, y=Y, z=Z))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

"""
-------------------------------------------------------------------------------
SUPERFICIES IMPLICITAS
-------------------------------------------------------------------------------
"""
def sup_imp(sup, x, y, z, dom_x=sp.Interval(-5,5), dom_y=sp.Interval(-5,5), dom_z=sp.Interval(-5,5),
            fig=None, color='blue', titulo='Superficie implicita', resolucion=75):
    parametric_surface = sp.lambdify((x, y, z), sup, 'numpy')
    X, Y, Z = np.mgrid[float(dom_x.start):float(dom_x.end):resolucion*1j, 
                       float(dom_y.start):float(dom_y.end):resolucion*1j, 
                       float(dom_z.start):float(dom_z.end):resolucion*1j]
    values = parametric_surface(X, Y, Z)
    if not fig: fig = go.Figure()
    fig.add_trace(
        go.Isosurface(
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
            showlegend=True))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def imp_desc_pt(f, x, y, z, x0, y0, z0, 
                dom_x=sp.Interval(-5,5), dom_y=sp.Interval(-5,5), dom_z=sp.Interval(-5,5), 
                fig=None):
    fig = sup_imp(f, x, y, z, dom_x=dom_x, dom_y=dom_y, dom_z=dom_z, titulo=r'$'+sp.latex(f)+r'=0$')
    fig.data[0].update(opacity=0.4)

    resultados = {
        'sup' : f,
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
                  sp.Interval(punto[0]-1, punto[0]+1),
                  sp.Interval(punto[1]-1, punto[1]+1),
                  sp.Interval(punto[2]-1, punto[2]+1),
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