import sympy as sp
from points import xyz_to_uv


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
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    E=sp.simplify(sp.Matrix(du_parametrizacion).dot(sp.Matrix(du_parametrizacion)))
    F=sp.simplify(sp.Matrix(du_parametrizacion).dot(sp.Matrix(dv_parametrizacion)))
    G=sp.simplify(sp.Matrix(dv_parametrizacion).dot(sp.Matrix(dv_parametrizacion)))

    return sp.Matrix([E, F, G]).T

def primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, EFG=None):
    """
    Retorna en forma de tupla la primera forma fundamental en un punto  descrito por u,v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    EFG                 parametro opcional por si se tienen ya calculados E, F, G
    """
    if EFG:
        return sp.Matrix([sp.N(EFG[0].subs([[u, u0],[v,v0]])), sp.N(EFG[1].subs([[u, u0],[v,v0]])), sp.N(EFG[2].subs([[u, u0],[v,v0]]))]).T
    
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    du_parametrizacion_pt = [sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_parametrizacion_pt = [sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    E_pt=sp.Matrix(du_parametrizacion_pt).dot(sp.Matrix(du_parametrizacion_pt))
    F_pt=sp.Matrix(du_parametrizacion_pt).dot(sp.Matrix(dv_parametrizacion_pt))
    G_pt=sp.Matrix(dv_parametrizacion_pt).dot(sp.Matrix(dv_parametrizacion_pt))

    return sp.Matrix([E_pt, F_pt, G_pt]).T

def primeraFormaFundamental_pt_xyz(parametrizacion, u, v, x0, y0, z0, EFG=None):
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
    EFG                 parametro opcional por si se tienen ya calculados E, F, G
    """
    u0, v0 = xyz_to_uv(parametrizacion, u, v, x0, y0, z0)
    return primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, EFG)


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
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]
    duu_parametrizacion = [sp.diff(du_parametrizacion[i], u) for i in range(3)]
    duv_parametrizacion = [sp.diff(du_parametrizacion[i], v) for i in range(3)]
    dvv_parametrizacion = [sp.diff(dv_parametrizacion[i], v) for i in range(3)]

    e = sp.simplify(sp.det(sp.Matrix([du_parametrizacion, dv_parametrizacion, duu_parametrizacion]).T) / (sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion))).norm())
    f = sp.simplify(sp.det(sp.Matrix([du_parametrizacion, dv_parametrizacion, duv_parametrizacion]).T) / (sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion))).norm())
    g = sp.simplify(sp.det(sp.Matrix([du_parametrizacion, dv_parametrizacion, dvv_parametrizacion]).T) / (sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion))).norm())
    
    return sp.Matrix([e, f, g]).T

def segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, efg=None):
    """
    Retorna en forma de tupla la segunda forma fundamental en un punto  descrito por u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    efg                 parametro opcional por si se tienen ya calculados e, f, g
    """
    if efg:
        return sp.Matrix([sp.N(efg[0].subs([[u, u0],[v,v0]])), sp.N(efg[1].subs([[u, u0],[v,v0]])), sp.N(efg[2].subs([[u, u0],[v,v0]]))]).T
    
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
    
    return sp.Matrix([e_pt, f_pt, g_pt]).T

def segundaFormaFundamental_pt_xyz(parametrizacion, u, v, x0, y0, z0, efg=None):
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
    efg                 parametro opcional por si se tienen ya calculados e, f, g
    """
    u0, v0 = xyz_to_uv(parametrizacion, u, v, x0, y0, z0)
    return segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, efg)

