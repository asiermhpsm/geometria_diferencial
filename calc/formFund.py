import sympy as sp
from points import xyz_to_uv
from caract import normal, normal_pt_uv, normal_pt_xyz


"""
-------------------------------------------------------------------------------
PRIMERA FORMA FUNDAMENTAL
-------------------------------------------------------------------------------
"""
def primeraFormaFundamental(parametrizacion, u, v):
    """
    Retorna la primera forma fundamental en forma de (E, F, G)
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    du_parametrizacion = sp.simplify(sp.Matrix([sp.diff(parametrizacion[i], u) for i in range(3)]))
    dv_parametrizacion = sp.simplify(sp.Matrix([sp.diff(parametrizacion[i], v) for i in range(3)]))

    E=sp.simplify(du_parametrizacion.dot(du_parametrizacion))
    F=sp.simplify(du_parametrizacion.dot(dv_parametrizacion))
    G=sp.simplify(dv_parametrizacion.dot(dv_parametrizacion))

    return sp.Matrix([E, F, G]).T

def primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0):
    """
    Retorna en forma de tupla la primera forma fundamental en un punto  descrito por u,v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    
    du_parametrizacion = sp.simplify(sp.Matrix([sp.diff(parametrizacion[i], u) for i in range(3)]))
    dv_parametrizacion = sp.simplify(sp.Matrix([sp.diff(parametrizacion[i], v) for i in range(3)]))

    du_parametrizacion_pt = sp.simplify(sp.Matrix([sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]))
    dv_parametrizacion_pt = sp.simplify(sp.Matrix([sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]))

    E_pt=sp.simplify(du_parametrizacion_pt.dot(du_parametrizacion_pt))
    F_pt=sp.simplify(du_parametrizacion_pt.dot(dv_parametrizacion_pt))
    G_pt=sp.simplify(dv_parametrizacion_pt.dot(dv_parametrizacion_pt))

    return sp.Matrix([E_pt, F_pt, G_pt]).T

def primeraFormaFundamental_pt_xyz(parametrizacion, u, v, x0, y0, z0):
    """
    Retorna en forma de tupla la primera forma fundamental en un punto  descrito por x, y, z
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
    return primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)


"""
-------------------------------------------------------------------------------
SEGUNDA FORMA FUNDAMENTAL
-------------------------------------------------------------------------------
"""
def segundaFormaFundamental(parametrizacion, u, v):
    """
    Retorna la segunda forma fundamental en forma de tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    du_parametrizacion = sp.simplify(sp.Matrix([sp.simplify(sp.diff(parametrizacion[i], u)) for i in range(3)]))
    dv_parametrizacion = sp.simplify(sp.Matrix([sp.simplify(sp.diff(parametrizacion[i], v)) for i in range(3)]))
    duu_parametrizacion = sp.simplify(sp.Matrix([sp.simplify(sp.diff(du_parametrizacion[i], u)) for i in range(3)]))
    duv_parametrizacion = sp.simplify(sp.Matrix([sp.simplify(sp.diff(du_parametrizacion[i], v)) for i in range(3)]))
    dvv_parametrizacion = sp.simplify(sp.Matrix([sp.simplify(sp.diff(dv_parametrizacion[i], v)) for i in range(3)]))

    n = normal(parametrizacion, u, v)
    e = sp.simplify(n.dot(duu_parametrizacion))
    f = sp.simplify(n.dot(duv_parametrizacion))
    g = sp.simplify(n.dot(dvv_parametrizacion))
    
    return sp.Matrix([e, f, g]).T

def segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0):
    """
    Retorna en forma de tupla la segunda forma fundamental en un punto  descrito por u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    
    du_parametrizacion = [sp.simplify(sp.diff(parametrizacion[i], u)) for i in range(3)]
    dv_parametrizacion = [sp.simplify(sp.diff(parametrizacion[i], v)) for i in range(3)]
    duu_parametrizacion = [sp.simplify(sp.diff(du_parametrizacion[i], u)) for i in range(3)]
    duv_parametrizacion = [sp.simplify(sp.diff(du_parametrizacion[i], v)) for i in range(3)]
    dvv_parametrizacion = [sp.simplify(sp.diff(dv_parametrizacion[i], v)) for i in range(3)]

    du_parametrizacion_pt = [sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_parametrizacion_pt = [sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    duu_parametrizacion_pt = [sp.N(duu_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    duv_parametrizacion_pt = [sp.N(duv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dvv_parametrizacion_pt = [sp.N(dvv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    denominador = sp.simplify((sp.Matrix(du_parametrizacion_pt).cross(sp.Matrix(dv_parametrizacion_pt))).norm())

    e_pt = sp.det(sp.Matrix([du_parametrizacion_pt, dv_parametrizacion_pt, duu_parametrizacion_pt]).T) / denominador
    f_pt = sp.det(sp.Matrix([du_parametrizacion_pt, dv_parametrizacion_pt, duv_parametrizacion_pt]).T) / denominador
    g_pt = sp.det(sp.Matrix([du_parametrizacion_pt, dv_parametrizacion_pt, dvv_parametrizacion_pt]).T) / denominador
    
    return sp.Matrix([e_pt, f_pt, g_pt]).T

def segundaFormaFundamental_pt_xyz(parametrizacion, u, v, x0, y0, z0):
    """
    Retorna en forma de tupla la segunda forma fundamental en un punto  descrito por x, y, z
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
    return segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)

