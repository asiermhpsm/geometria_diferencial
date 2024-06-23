import plotly.graph_objects as go
import numpy as np
import sympy as sp

import utils.calc_param as calcp
import utils.calc_imp as calci

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
            name=titulo,
            hovertemplate="Punto"))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def vector(inicio, vector, fig=None, color='red', titulo=None, hovertemplate="v"):
    """
    Dibuja un vector en el espacio
    Argumentos:
    inicio      coordenadas del punto de inicio del vector (cualquier tipo que se pueda transformar a lista de float)
    vector      coordenadas del vector (cualquier tipo que se pueda transformar a lista de float)
    fig         figura de plotly donde se añadirá el vector
    color       color del vector
    titulo      nombre del vector
    hovertemplate   texto que aparece al pasar el ratón por encima del vector
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
                     name=titulo,
                     legendgroup=titulo,
                     hovertemplate=hovertemplate))
    fig.add_cone(x=[inicio[0]+vector[0]],
                 y=[inicio[1]+vector[1]],
                 z=[inicio[2]+vector[2]],
                 u=[vector[0]],
                 v=[vector[1]],
                 w=[vector[2]],
                 sizeref=0.2,
                 colorscale=[[0, color], [1, color]],
                 name=titulo,
                 showscale=False,
                 legendgroup=titulo,
                 hovertemplate=hovertemplate)
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def circulo(centro, radio, dir1, dir2, fig=None, color='red', titulo='circulo', hovertemplate="κ"):
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
    hovertemplate   texto que aparece al pasar el ratón por encima del círculo
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
                     line=dict(color=color, width=5),
                     hovertemplate=hovertemplate))
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
              fig=None, resolucion=100, titulo='Superficie', color=None, leyenda=False, hovertemplate="φ"):
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
    leyenda     si se pinta la leyenda
    hovertemplate   texto que aparece al pasar el ratón por encima de la superficie
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
                       name=titulo if leyenda else "",
                       colorscale=[[0, color], [1, color]],
                       showlegend=leyenda, 
                       showscale=False,
                       hovertemplate=hovertemplate))
    else:
        fig.add_trace(
            go.Surface(x=X, y=Y, z=Z,
                       colorbar=dict(x=-0.1),
                       name=titulo if leyenda else "",
                       colorscale='ice',
                       showlegend=leyenda, 
                       showscale=False,
                       hovertemplate=hovertemplate))
    fig.update_layout(scene=dict(aspectmode='data'),)
    return fig

def sup_param_cond_elipse(sup, u, v, a, b ,fig=None, resolucion=100, titulo='Superficie',leyenda=False, hovertemplate="φ"):
    """
    Grafica una superficie paramétrica con restricción de elipse (a*u^2 + b*v^2 < 1)
    Argumentos:
    sup         superficie paramétrica
    u           primera variable de dependencia
    v           segunda variable de dependencia
    a           semieje a
    b           semieje b
    fig         figura de plotly donde se añadirá la superficie
    resolucion  resolución de la malla
    titulo      nombre de la superficie
    leyenda     si se pinta la leyenda
    hovertemplate   texto que aparece al pasar el ratón por encima de la superficie
    """
    sup = list(sup)
    parametric_surface = sp.lambdify((u, v), sup, 'numpy')
    u_values, v_values = genera_malla_elipse(a, b, resolucion)
    X, Y, Z = parametric_surface(u_values, v_values)
    if np.isscalar(X): X = np.full_like(u_values, X)
    if np.isscalar(Y): Y = np.full_like(u_values, Y)
    if np.isscalar(Z): Z = np.full_like(u_values, Z)
    if not fig: fig = go.Figure()
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='ice', name=titulo if leyenda else "", showlegend=leyenda, showscale=False, hovertemplate=hovertemplate))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def param_desc_pt_uv(sup, u, v, u0, v0, dom_u=sp.Interval(-5,5), dom_v=sp.Interval(-5,5), a=None, b=None, fig=None, 
                     tangente=True, normal=True, dirs_principales=True, curvs_principales=True, dirs_asintoticas=True, 
                     leyenda=False):
    """
    Dada una superficie paramétrica, pinta la superficie, el plano tangente, el vector normal 
    y las direcciones principales en un punto que depende de las variables u y v
    Argumentos:
    sup                 superficie paramétrica
    u                   primera variable de dependencia
    v                   segunda variable de dependencia
    u0                  valor de u en el punto
    v0                  valor de v en el punto
    dom_u               dominio de la primera variable
    dom_v               dominio de la segunda variable
    fig                 figura de plotly donde se añadirá la superficie
    tangente            si se pinta el plano tangente
    normal              si se pinta el vector normal
    dirs_principales    si se pintan las direcciones principales
    curvs_principales   si se pintan las curvas principales
    dirs_asintoticas    si se pintan las direcciones asintóticas
    leyenda             si se pinta la leyenda
    """
    sup = sp.Matrix(sup)
    if a!=None and b!=None:
        fig = sup_param_cond_elipse(sup, u, v, a, b, titulo=r'$\vec{\varphi}='+sp.latex(sup, mat_delim='(')+r'$' if leyenda else "")
    else:
        fig = sup_param(sup, u, v, dom_u, dom_v, titulo=r'$\vec{\varphi}='+sp.latex(sup, mat_delim='(')+r'$' if leyenda else "")

    resultados = {
        'sup' : sup,
        'u' : u,
        'v' : v,
        'u0' : u0,
        'v0' : v0
    }
    resultados = calcp.descripccion_pt_uv(resultados)

    if tangente or normal or dirs_principales or curvs_principales or dirs_asintoticas:
        fig.data[0].update(opacity=0.7)
    
    punto = sup.subs({u:u0, v:v0})
    fig = point(punto, fig=fig, titulo=r'$\varphi('+sp.latex(u0)+r','+sp.latex(v0)+r')='+sp.latex(punto, mat_delim='(')+r'$' if leyenda else "")
    
    if tangente:
        plano = sp.Matrix([u*resultados['d1_pt'].normalized() + v*resultados['d2_pt'].normalized() + punto])
        fig = sup_param(plano, u, v, dom_u=sp.Interval(-1,1), dom_v=sp.Interval(-1,1), 
                        fig=fig, titulo='Plano tangente' if leyenda else "", color='grey', hovertemplate="Plano tangente")
        fig.data[1].update(opacity=0.5)

    if normal:
        fig = vector(punto, tuple(float(comp) for comp in resultados['normal_pt']), fig, 'red', r'$\vec{n}$' if leyenda else "", hovertemplate="vec. normal")

    if dirs_principales:
        fig = vector(punto, resultados['d1_pt'], fig, 'yellow', r'$\vec{d_1}$' if leyenda else "", hovertemplate="dir. principal 1")
        fig = vector(punto, resultados['d2_pt'], fig, 'green', r'$\vec{d_2}$' if leyenda else "", hovertemplate="dir. principal 2")

    if curvs_principales:
        if resultados['k1_pt'] !=0:
            radio = 1/resultados['k1_pt']
            fig = circulo(punto + radio*resultados['normal_pt'].normalized(), 
                        radio,
                        resultados['normal_pt'],
                        resultados['d1_pt'],
                        fig, 'yellow', r'$r=1/\kappa_1$' if leyenda else "", hovertemplate="κ1")
        if resultados['k2_pt'] !=0:
            radio = 1/resultados['k2_pt']
            fig = circulo(punto + radio*resultados['normal_pt'].normalized(),
                        radio,
                        resultados['normal_pt'],
                        resultados['d2_pt'],
                        fig, 'green', r'$r=1/\kappa_2$' if leyenda else "", hovertemplate="κ2")
            
    if dirs_asintoticas:
        t = sp.symbols('t', real=True)
        colores = ['orange', 'purple']
        for i, dir in enumerate(resultados['Dirs_asint']):
            if isinstance(dir[0], sp.Symbol):
                continue
            puntos_posibles = set()
            ti = (dom_u.start-resultados['u0'])/dir[0]
            puntos_posibles.add((resultados['u0']+ti*dir[0], resultados['v0']+ti*dir[1]))
            ti = (dom_v.start-resultados['v0'])/dir[1]
            puntos_posibles.add((resultados['u0']+ti*dir[0], resultados['v0']+ti*dir[1]))
            ti = (dom_u.end-resultados['u0'])/dir[0]
            puntos_posibles.add((resultados['u0']+ti*dir[0], resultados['v0']+ti*dir[1]))
            ti = (dom_v.end-resultados['v0'])/dir[1]
            puntos_posibles.add((resultados['u0']+ti*dir[0], resultados['v0']+ti*dir[1]))
            puntos = [pto for pto in puntos_posibles if pto[0] in sp.Interval(dom_u.start, dom_u.end) and pto[1] in sp.Interval(dom_v.start, dom_v.end)]
            puntos = [sp.Matrix(pto).T for pto in puntos]
            if len(puntos)!=2:
                raise Exception('Error en la dirección asintótica')
            p1, p2 = puntos
            linea = p1 + t*(p2-p1)

            curva = list(resultados['sup'].subs({resultados['u']:linea[0], resultados['v']:linea[1]}))
            func_curva = sp.lambdify(t, curva, 'numpy')
            t_values = np.linspace(0, 1, 50)
            X, Y, Z = func_curva(t_values)
            if np.isscalar(X): X = np.full_like(t_values, X)
            if np.isscalar(Y): Y = np.full_like(t_values, Y)
            if np.isscalar(Z): Z = np.full_like(t_values, Z)
            fig.add_trace(
                go.Scatter3d(x=X, y=Y, z=Z, 
                            mode='lines', 
                            name=f'Dir. asintótica {i+1}' if leyenda else "", 
                            line=dict(color=colores[i], width=10),
                            hovertemplate=f"Dir. asintótica {i}"))
    
    if leyenda:
        fig.update_layout(
            legend=dict(font=dict(size=15)), 
            scene=dict(aspectmode='data'),
            title={
                'text': f"<b>SUPERFICIE 3D. </b><br><span style='font-size: 12px;'>Pinchar en un elemento de la leyenda permite hacerlo aparecer o desaparecer.</span>",
                'font': {'size': 24, 'family': 'Arial'},
                'x': 0.5,
                'xanchor': 'center'
            })
    else:
        fig.update_layout(
            scene=dict(aspectmode='data'),
            showlegend=False
            )
    
    return fig


"""
-------------------------------------------------------------------------------
SUPERFICIES IMPLICITAS
-------------------------------------------------------------------------------
"""
def sup_imp(sup, x, y, z, dom_x=sp.Interval(-5,5), dom_y=sp.Interval(-5,5), dom_z=sp.Interval(-5,5),
            fig=None, color=None, titulo='Superficie implicita', resolucion=75, leyenda=False, hovertemplate="Superficie"):
    """
    Grafica una superficie implícita
    Argumentos:
    sup         superficie implícita
    x           variable x
    y           variable y
    z           variable z
    dom_x       dominio de x
    dom_y       dominio de y
    dom_z       dominio de z
    fig         figura de plotly donde se añadirá la superficie
    color       color de la superficie
    titulo      nombre de la superficie
    resolucion  resolución de la malla
    leyenda     si se pinta la leyenda
    hovertemplate   texto que aparece al pasar el ratón por encima de la superficie
    """
    parametric_surface = sp.lambdify((x, y, z), sup, 'numpy')
    X, Y, Z = np.mgrid[float(dom_x.start):float(dom_x.end):resolucion*1j, 
                       float(dom_y.start):float(dom_y.end):resolucion*1j, 
                       float(dom_z.start):float(dom_z.end):resolucion*1j]
    values = parametric_surface(X, Y, Z)
    if not fig: fig = go.Figure()
    if color:
        fig.add_trace(
        go.Isosurface(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            value=values.flatten(),
            isomin=0,
            isomax=0,
            surface_count=1,
            showscale=leyenda,
            name=titulo if leyenda else "",
            colorscale=[[0, color], [1, color]],
            showlegend=leyenda,
            hovertemplate=hovertemplate))
    else:
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
            name=titulo if leyenda else "",
            colorscale='ice',
            showlegend=leyenda,
            hovertemplate=hovertemplate))
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def imp_desc_pt(f, x, y, z, x0, y0, z0, 
                dom_x=sp.Interval(-5,5), dom_y=sp.Interval(-5,5), dom_z=sp.Interval(-5,5), 
                tangente=True, normal=True,fig=None, leyenda=False):
    """
    Dada una superficie implícita, pinta la superficie, el plano tangente y el vector normal en un punto
    Argumentos:
    f           superficie implícita
    x           variable x
    y           variable y
    z           variable z
    x0          valor de x en el punto
    y0          valor de y en el punto
    z0          valor de z en el punto
    dom_x       dominio de x
    dom_y       dominio de y
    dom_z       dominio de z
    tangente    si se pinta el plano tangente
    normal      si se pinta el vector normal
    fig         figura de plotly donde se añadirá la superficie
    leyenda     si se pinta la leyenda
    """
    fig = sup_imp(f, x, y, z, dom_x=dom_x, dom_y=dom_y, dom_z=dom_z, titulo=r'$'+sp.latex(f)+r'=0$' if leyenda else "", leyenda=leyenda)

    if tangente or normal:
        fig.data[0].update(opacity=0.6)

    punto = (x0, y0, z0)
    fig = point(punto, fig=fig, titulo='Punto' if leyenda else "")

    resultados = {
        'sup' : f,
        'x' : x,
        'y' : y,
        'z' : z,
        'x0' : x0,
        'y0' : y0,
        'z0' : z0
    }

    resultados = calci.descripccion_pt_uv(resultados)

    if tangente:
        fig = sup_imp(resultados['tangente_pt'].rhs - resultados['tangente_pt'].lhs, 
                    x, y, z,
                    sp.Interval(punto[0]-1, punto[0]+1),
                    sp.Interval(punto[1]-1, punto[1]+1),
                    sp.Interval(punto[2]-1, punto[2]+1),
                    fig=fig, color='grey', titulo='Plano tangente' if leyenda else "", hovertemplate="Plano tangente")
        fig.data[1].update(opacity=0.6)

    if normal:
        fig = vector(punto, resultados['normal_pt'], fig, 'red', r'$\vec{n}$' if leyenda else "", hovertemplate="vec. normal")

    fig.update_layout(
        scene=dict(aspectmode='data'),
        showlegend=leyenda
        )

    return fig



