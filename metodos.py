import sympy as sp
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm

def uv_to_xyz(parametrizacion, u, v, u0, v0):
    """
    Sustituye u y v en la superficie parametrizada
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    x = float(parametrizacion[0].subs([[u, u0],[v,v0]]))
    y = float(parametrizacion[1].subs([[u, u0],[v,v0]]))
    z = float(parametrizacion[2].subs([[u, u0],[v,v0]]))
    return x, y, z

def xy_to_uv(parametrizacion, x0, y0, u, v):
    """
    Dado un x y un y consigo su valor u y v de una superficie parametrizada
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    x0                  valor x del punto
    y0                  valor y del punto
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    eq1 = sp.Eq(parametrizacion[0], x0)
    eq2 = sp.Eq(parametrizacion[1], y0)

    soluciones = sp.solve((eq1, eq2), (u, v))
    
    if not soluciones:
        raise('El punto dado no esta en la superficie.')

    return soluciones

def xyz_to_uv(parametrizacion, x0, y0, z0, u, v):
    """
    Dado un x,y,z un y consigo su valor u y v de una superficie parametrizada
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    x0                  valor x del punto
    y0                  valor y del punto
    z0                  valor z del punto
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    soluciones = xy_to_uv(parametrizacion, x0, y0, u, v)

    for sol in soluciones:
        if float(parametrizacion[2].subs([[u, sol[0]],[v,sol[1]]])) == z0:
            return sol

    raise('El punto dado no esta en la superficie.')


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
    if len(args) % 6 != 0:
        raise ValueError("La cantidad de argumentos no es válida. Deben ser grupos de (tipo, X, Y, Z, color_map) pero se han encontrado ", len(args), " argumentos.")

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
    Devuelve los valores X, Y, Z, cmap, color que se deben pasar a la funcion ax.plot_surface() para representar la superficie
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

def procesa_punto_xyz(parametrizacion, x0, y0, z0, color='black', marker='o'):
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


def normal(parametrizacion, u, v):
    """
    Retorna el vector normal de una superficie
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]
    res = sp.simplify( sp.Matrix(sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion))).normalized() )
    return [elem for elem in res]

def normal_pt(parametrizacion, u, v, u0, v0):
    """
    Retorna el vector normal de una superficie en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    du_parametrizacion_pt = [sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_parametrizacion_pt = [sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    du_parametrizacion_X_dv_parametrizacion_pt = sp.Matrix(sp.Matrix(du_parametrizacion_pt).cross(sp.Matrix(dv_parametrizacion_pt))).normalized()

    return [elem for elem in sp.Matrix(du_parametrizacion_X_dv_parametrizacion_pt)]


def primeraFormaFundamental(parametrizacion, u, v):
    """
    Retorna la primera forma fundamental en forma de (E, F, G)
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    E=sp.simplify(sp.Matrix(du_parametrizacion).dot(sp.Matrix(du_parametrizacion)))
    F=sp.simplify(sp.Matrix(du_parametrizacion).dot(sp.Matrix(dv_parametrizacion)))
    G=sp.simplify(sp.Matrix(dv_parametrizacion).dot(sp.Matrix(dv_parametrizacion)))

    return E, F, G

def primeraFormaFundamental_pt(parametrizacion, u, v, u0, v0):
    """
    Retorna la primera forma fundamental en un punto en forma de tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    du_parametrizacion_pt = [sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_parametrizacion_pt = [sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    E_pt=sp.Matrix(du_parametrizacion_pt).dot(sp.Matrix(du_parametrizacion_pt))
    F_pt=sp.Matrix(du_parametrizacion_pt).dot(sp.Matrix(dv_parametrizacion_pt))
    G_pt=sp.Matrix(dv_parametrizacion_pt).dot(sp.Matrix(dv_parametrizacion_pt))

    return E_pt, F_pt, G_pt


def segundoFormaFundamental(parametrizacion, u, v):
    """
    Retorna la segunda forma fundamental en forma de tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]
    duu_parametrizacion = [sp.diff(du_parametrizacion[i], u) for i in range(3)]
    duv_parametrizacion = [sp.diff(du_parametrizacion[i], v) for i in range(3)]
    dvv_parametrizacion = [sp.diff(dv_parametrizacion[i], v) for i in range(3)]

    e = sp.simplify(sp.det(sp.Matrix([du_parametrizacion, dv_parametrizacion, duu_parametrizacion]).T) / (sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion))).norm())
    f = sp.simplify(sp.det(sp.Matrix([du_parametrizacion, dv_parametrizacion, duv_parametrizacion]).T) / (sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion))).norm())
    g = sp.simplify(sp.det(sp.Matrix([du_parametrizacion, dv_parametrizacion, dvv_parametrizacion]).T) / (sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion))).norm())
    
    return e, f, g

def segundoFormaFundamental_pt(parametrizacion, u, v, u0, v0):
    """
    Retorna la segunda forma fundamental en un punto en forma de tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]
    duu_parametrizacion = [sp.diff(du_parametrizacion[i], u) for i in range(3)]
    duv_parametrizacion = [sp.diff(du_parametrizacion[i], v) for i in range(3)]
    dvv_parametrizacion = [sp.diff(dv_parametrizacion[i], v) for i in range(3)]

    du_parametrizacion_pt = [sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_parametrizacion_pt = [sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    duu_parametrizacion_pt = [sp.N(duu_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    duv_parametrizacion_pt = [sp.N(duv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dvv_parametrizacion_pt = [sp.N(dvv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    e_pt = sp.det(sp.Matrix([du_parametrizacion_pt, dv_parametrizacion_pt, duu_parametrizacion_pt]).T) / (sp.Matrix(du_parametrizacion_pt).cross(sp.Matrix(dv_parametrizacion_pt))).norm()
    f_pt = sp.det(sp.Matrix([du_parametrizacion_pt, dv_parametrizacion_pt, duv_parametrizacion_pt]).T) / (sp.Matrix(du_parametrizacion_pt).cross(sp.Matrix(dv_parametrizacion_pt))).norm()
    g_pt = sp.det(sp.Matrix([du_parametrizacion_pt, dv_parametrizacion_pt, dvv_parametrizacion_pt]).T) / (sp.Matrix(du_parametrizacion_pt).cross(sp.Matrix(dv_parametrizacion_pt))).norm()
    
    return e_pt, f_pt, g_pt


def curvaturaGauss(parametrizacion, u, v):
    """
    Retorna la curvatura de Gauss
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    E, F, G = primeraFormaFundamental(parametrizacion, u, v)
    e, f, g = segundoFormaFundamental(parametrizacion, u, v)
    return sp.simplify((e*g - f**2) / (E*G - F**2))

def curvaturaGauss_pt(parametrizacion, u, v, u0, v0):
    """
    Retorna la curvatura de Gauss en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    E_pt, F_pt, G_pt = primeraFormaFundamental_pt(parametrizacion, u, v, u0, v0)
    e_pt, f_pt, g_pt = segundoFormaFundamental_pt(parametrizacion, u, v, u0, v0)
    return (e_pt*g_pt - f_pt**2) / (E_pt*G_pt - F_pt**2)


def curvaturaMedia(parametrizacion, u, v):
    """
    Retorna la curvatura media
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    E, F, G = primeraFormaFundamental(parametrizacion, u, v)
    e, f, g = segundoFormaFundamental(parametrizacion, u, v)
    return sp.simplify((e*G + g*E - 2*f*F) / (2*(E*G - F**2)))

def curvaturaMedia_pt(parametrizacion, u, v, u0, v0):
    """
    Retorna la curvatura media en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    E_pt, F_pt, G_pt = primeraFormaFundamental_pt(parametrizacion, u, v, u0, v0)
    e_pt, f_pt, g_pt = segundoFormaFundamental_pt(parametrizacion, u, v, u0, v0)
    return (e_pt*G_pt + g_pt*E_pt - 2*f_pt*F_pt) / (2*(E_pt*G_pt - F_pt**2))


def curvaturasPrincipales(parametrizacion, u, v):
    """
    Retorna las curvaturas principales como tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    K = curvaturaGauss(parametrizacion, u, v)
    H = curvaturaMedia(parametrizacion, u, v)
    raiz = sp.sqrt(H**2 - K)
    return sp.simplify(H + raiz), sp.simplify(H - raiz)

def curvaturasPrincipales_pt(parametrizacion, u, v, u0, v0):
    """
    Retorna las curvaturas principales en un punto como tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacio      parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    K_pt = curvaturaGauss_pt(parametrizacion, u, v, u0, v0)
    H_pt = curvaturaMedia_pt(parametrizacion, u, v, u0, v0)
    raiz = sp.sqrt(H_pt**2 - K_pt)
    return H_pt + raiz, H_pt - raiz


def clasicfPt(parametrizacion, u, v, u0, v0):
    """
    Imprime la clasificacion de una superficie en un punto descrito con u y v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    K_pt = curvaturaGauss_pt(parametrizacion, u, v, u0, v0)
    if K_pt > 0:
        print('Eliptico')
    elif K_pt < 0:
        print('Hiperbólitco')
    elif K_pt == 0:
        print('Parabólico o planar')


def planoTangente(parametrizacion, u, v):
    """
    Imprime la clasificacion de una superficie en un punto descrito con u y v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    x, y, z = sp.symbols('x, y, z', real = True)
    xyz = [x,y,z]

    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    return sp.Matrix( sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion)) ).dot( sp.Matrix( [(xyz[i]) for i in range(3)]) )


def planoTangente_pt(parametrizacion, u, v, u0, v0):
    """
    Imprime la clasificacion de una superficie en un punto descrito con u y v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    x, y, z = sp.symbols('x, y, z', real = True)
    xyz = [x,y,z]
    parametrizacion_pt = [sp.N(parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    du_parametrizacion_pt = [sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_parametrizacion_pt = [sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    return sp.Matrix( sp.Matrix(du_parametrizacion_pt).cross(sp.Matrix(dv_parametrizacion_pt)) ).dot( sp.Matrix( [(xyz[i] - parametrizacion_pt[i]) for i in range(3)]) )


def dirPrinc_pt(parametrizacion, u, v, u0, v0):
    """
    Calcula las direcciones principales en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    a, b = sp.symbols('u, v', real = True)

    k1_pt, k2_pt = curvaturasPrincipales_pt(parametrizacion, u, v, u0, v0)
    E_pt, F_pt, G_pt = primeraFormaFundamental_pt(parametrizacion, u, v, u0, v0)
    e_pt, f_pt, g_pt = segundoFormaFundamental_pt(parametrizacion, u, v, u0, v0)

    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    du_parametrizacion_pt = [sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_parametrizacion_pt = [sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]


    ec1 = sp.Eq(sp.simplify(e_pt-k1_pt*E_pt)*a, sp.simplify(f_pt-k1_pt*F_pt)*b)
    ec2 = sp.Eq(sp.simplify(f_pt-k1_pt*F_pt)*a, sp.simplify(g_pt-k1_pt*G_pt)*b)
    sol1 = sp.solve((ec1, ec2), (a, b))
    vec1 = [sol1['a'] * du + sol1['b'] * dv for du, dv in zip(du_parametrizacion_pt, dv_parametrizacion_pt)]
    

    ec1 = sp.Eq(sp.simplify(e_pt-k2_pt*E_pt)*a, sp.simplify(f_pt-k2_pt*F_pt)*b)
    ec2 = sp.Eq(sp.simplify(f_pt-k2_pt*F_pt)*a, sp.simplify(g_pt-k2_pt*G_pt)*b)
    sol2 = sp.solve((ec1, ec2), (a, b))
    vec2 = [sol2['a'] * du + sol2['b'] * dv for du, dv in zip(du_parametrizacion_pt, dv_parametrizacion_pt)]

    return vec1, vec2
