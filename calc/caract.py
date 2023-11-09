import sympy as sp
from points import xyz_to_uv
from curv import curvaturaGauss_pt_uv, curvaturasPrincipales_pt_uv
from formFund import *


"""
-------------------------------------------------------------------------------
VECTOR NORMAL
-------------------------------------------------------------------------------
"""
def normal(parametrizacion, u, v):
    """
    Retorna el vector normal de una superficie
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]
    res = sp.simplify( sp.Matrix(sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion))).normalized() )
    return sp.Matrix([elem for elem in res]).T

def normal_pt_uv(parametrizacion, u, v, u0, v0, normal=None):
    """
    Retorna el vector normal de una superficie en un punto descrito por u,v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    normal              parametro opcional por si se tiene ya calculado el vector normal
    """
    if normal:
        return sp.Matrix([sp.N(normal[i].subs([[u, u0],[v,v0]])) for i in range(3)]).T
    
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    du_parametrizacion_pt = [sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_parametrizacion_pt = [sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    du_parametrizacion_X_dv_parametrizacion_pt = sp.Matrix(sp.Matrix(du_parametrizacion_pt).cross(sp.Matrix(dv_parametrizacion_pt))).normalized()

    return sp.Matrix([elem for elem in sp.Matrix(du_parametrizacion_X_dv_parametrizacion_pt)]).T

def normal_pt_xyz(parametrizacion, u, v, x0, y0, z0, normal=None):
    """
    Retorna el vector normal de una superficie en un punto descrito por x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )          
    x0                  valor x del punto
    y0                  valor y del punto
    z0                  valor z del punto
    normal              parametro opcional por si se tiene ya calculado el vector normal
    """
    u0, v0 = xyz_to_uv(parametrizacion, u, v, x0, y0, z0)
    return normal_pt_uv(parametrizacion, u, v, u0, v0, normal)



"""
-------------------------------------------------------------------------------
CLASIFICACION DE UN PUNTO
-------------------------------------------------------------------------------
"""
def clasicPt_uv(parametrizacion, u, v, u0, v0, curv=None, EFG=None, efg=None):
    """
    Imprime la clasificacion de una superficie en un punto descrito con x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    curv                parametro opcional por si ya se tiene calculada la curvatura de Gauss
    EFG                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados E, F, G en el punto deseado
    efg                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados e, f, g en el punto deseado
    """
    K_pt = curvaturaGauss_pt_uv(parametrizacion, u, v, u0, v0, curv, EFG, efg)
    if K_pt > 0:
        print('Eliptico')
    elif K_pt < 0:
        print('Hiperbólitco')
    elif K_pt == 0:
        print('Parabólico o planar')

def clasicPt_xyz(parametrizacion, u, v, x0, y0, z0, curv=None, EFG=None, efg=None):
    """
    Imprime la clasificacion de una superficie en un punto descrito con x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    x0                  valor x del punto
    y0                  valor y del punto
    z0                  valor z del punto
    """
    u0, v0 = xyz_to_uv(parametrizacion, u, v, x0, y0, z0)
    return clasicPt_uv(parametrizacion, u, v, u0, v0, curv, EFG, efg)


"""
-------------------------------------------------------------------------------
PLANO TANGENTE
-------------------------------------------------------------------------------
"""
def planoTangente(parametrizacion, u, v):
    """
    Retorna el plano tangente (sin igualar a cero) de una superficie parametrizada
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    x, y, z = sp.symbols('x, y, z', real = True)
    xyz = [x,y,z]

    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    return sp.Matrix( sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion)) ).dot( sp.Matrix( [(xyz[i]) for i in range(3)]) )

def planoTangente_pt_uv(parametrizacion, u, v, u0, v0, tang=None):
    """
    Retorna el plano tangente (sin igualar a cero) de una superficie parametrizada en un punto descrito con u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    tang                parametro opcional por si ya se tiene calculado la formula general plano tangente en funcion de u,v
    """
    if tang:
        return sp.N(tang.subs([[u, u0],[v,v0]]))
    
    x, y, z = sp.symbols('x, y, z', real = True)
    xyz = [x,y,z]
    parametrizacion_pt = [sp.N(parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    du_parametrizacion_pt = [sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_parametrizacion_pt = [sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    return sp.Matrix( sp.Matrix(du_parametrizacion_pt).cross(sp.Matrix(dv_parametrizacion_pt)) ).dot( sp.Matrix( [(xyz[i] - parametrizacion_pt[i]) for i in range(3)]) )

def planoTangente_pt_xyz(parametrizacion, u, v, x0, y0,z0, tang=None):
    """
    Retorna el plano tangente (sin igualar a cero) de una superficie parametrizada en un punto descrito con u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    x0                  valor x del punto
    y0                  valor y del punto
    z0                  valor z del punto
    tang                parametro opcional por si ya se tiene calculado la formula general plano tangente en funcion de u,v
    """
    u0, v0 = xyz_to_uv(parametrizacion, u, v, x0, y0, z0)
    return planoTangente_pt_uv(parametrizacion, u, v, u0, v0, tang)


"""
-------------------------------------------------------------------------------
DIRECCIONES PRINCIPALES
-------------------------------------------------------------------------------
"""
#NO ESTA BIEN HECHA
def dirPrinc_pt_uv(parametrizacion, u, v, u0, v0):
    """
    Calcula las direcciones principales en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    a, b = sp.symbols('u, v', real = True)

    k1_pt, k2_pt = curvaturasPrincipales_pt_uv(parametrizacion, u, v, u0, v0)
    E_pt, F_pt, G_pt = primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)
    e_pt, f_pt, g_pt = segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)

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

