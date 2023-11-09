import sympy as sp
from formFund import *
from points import xyz_to_uv


"""
-------------------------------------------------------------------------------
CURVATURA DE GAUSS
-------------------------------------------------------------------------------
"""
def curvaturaGauss(parametrizacion, u, v, EFG=None, efg=None):
    """
    Retorna la curvatura de Gauss
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    EFG                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados E, F, G
    efg                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados e, f, g
    """
    E, F, G = EFG if EFG else primeraFormaFundamental(parametrizacion, u, v)
    e, f, g = efg if efg else segundaFormaFundamental(parametrizacion, u, v)
    return sp.simplify((e*g - f**2) / (E*G - F**2))

def curvaturaGauss_pt_uv(parametrizacion, u, v, u0, v0, curv=None, EFG=None, efg=None):
    """
    Retorna la curvatura de Gauss en un punto descrito por u, v
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
    if curv:
        return sp.N(curv.subs([[u, u0],[v,v0]]))
    
    E_pt, F_pt, G_pt = EFG if EFG else primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)
    e_pt, f_pt, g_pt = efg if efg else segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)
    return (e_pt*g_pt - f_pt**2) / (E_pt*G_pt - F_pt**2)

def curvaturaGauss_pt_xyz(parametrizacion, u, v, x0, y0, z0, curv=None, EFG=None, efg=None):
    """
    Retorna la curvatura de Gauss en un punto descrito por x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    x0                  valor x del punto
    y0                  valor y del punto
    z0                  valor z del punto
    curv                parametro opcional por si ya se tiene calculada la curvatura de Gauss
    EFG                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados E, F, G en el punto deseado
    efg                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados e, f, g en el punto deseado
    """
    u0, v0 = xyz_to_uv(parametrizacion, u, v, x0, y0, z0)
    return curvaturaGauss_pt_uv(parametrizacion, u, v, u0, v0, curv, EFG, efg)


"""
-------------------------------------------------------------------------------
CURVATURA MEDIA
-------------------------------------------------------------------------------
"""
def curvaturaMedia(parametrizacion, u, v, EFG=None, efg=None):
    """
    Retorna la curvatura media
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    EFG                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados E, F, G
    efg                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados e, f, g
    """
    E, F, G = EFG if EFG else primeraFormaFundamental(parametrizacion, u, v)
    e, f, g = efg if efg else segundaFormaFundamental(parametrizacion, u, v)
    return sp.simplify((e*G + g*E - 2*f*F) / (2*(E*G - F**2)))

def curvaturaMedia_pt_uv(parametrizacion, u, v, u0, v0, curv=None, EFG=None, efg=None):
    """
    Retorna la curvatura media en un punto descrito por u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    curv                parametro opcional por si ya se tiene calculada la curvatura de media
    EFG                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados E, F, G en el punto deseado
    efg                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados e, f, g en el punto deseado
    """
    if curv:
        return sp.N(curv.subs([[u, u0],[v,v0]]))
    
    E_pt, F_pt, G_pt = EFG if EFG else primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)
    e_pt, f_pt, g_pt = efg if efg else segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)
    return (e_pt*G_pt + g_pt*E_pt - 2*f_pt*F_pt) / (2*(E_pt*G_pt - F_pt**2))

def curvaturaMedia_pt_xyz(parametrizacion, u, v, x0, y0, z0, curv=None, EFG=None, efg=None):
    """
    Retorna la curvatura media en un punto descrito por x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    x0                  valor x del punto
    y0                  valor y del punto
    z0                  valor z del punto
    curv                parametro opcional por si ya se tiene calculada la curvatura de media
    EFG                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados E, F, G en el punto deseado
    efg                 parametro opcional (tupla de longitud 3) por si se tienen ya calculados e, f, g en el punto deseado
    """
    u0, v0 = xyz_to_uv(parametrizacion, u, v, x0, y0, z0)
    return curvaturaMedia_pt_uv(parametrizacion, u, v, u0, v0, curv, EFG, efg)


"""
-------------------------------------------------------------------------------
CURVATURAS PRINCIPALES
-------------------------------------------------------------------------------
"""
def curvaturasPrincipales(parametrizacion, u, v, K=None, H=None, EFG=None, efg=None):
    """
    Retorna las curvaturas principales como tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    K                   parametro opcional por si se tiene ya calculada cruvatura Gauss
    H                   parametro opcional por si se tiene ya calculada curvatura Media
    """
    if not K and not H:
        E, F, G = primeraFormaFundamental(parametrizacion, u, v)
        e, f, g = segundaFormaFundamental(parametrizacion, u, v)
        K = curvaturaGauss(parametrizacion, u, v, EFG=(E, F, G), efg=(e,f,g))
        H = curvaturaMedia(parametrizacion, u, v, EFG=(E, F, G), efg=(e,f,g))
    elif not K:
        K = curvaturaGauss(parametrizacion, u, v)
    elif not H:
        H = curvaturaMedia(parametrizacion, u, v)
    raiz = sp.sqrt(H**2 - K)
    return sp.Matrix([sp.simplify(H + raiz), sp.simplify(H - raiz)]).T

def curvaturasPrincipales_pt_uv(parametrizacion, u, v, u0, v0, curv=None, K=None, H=None):
    """
    Retorna como tupla las curvaturas principales en un punto descrito como u,v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacio      parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    curv                parametro opcional por si ya se tienen calculadas las curvaturas principales
    K                   parametro opcional por si se tiene ya calculada cruvatura Gauss en el punto deseado
    H                   parametro opcional por si se tiene ya calculada curvatura Media en el punto deseado
    """
    if curv:
        return sp.Matrix([sp.N(curv[0].subs([[u, u0],[v,v0]])), sp.N(curv[1].subs([[u, u0],[v,v0]]))]).T
    
    E_pt, F_pt, G_pt = primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)
    e_pt, f_pt, g_pt = segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)
    K_pt = curvaturaGauss_pt_uv(parametrizacion, u, v, u0, v0, EFG=(E_pt,F_pt, G_pt), efg=(e_pt,f_pt,g_pt))
    H_pt = curvaturaMedia_pt_uv(parametrizacion, u, v, u0, v0, EFG=(E_pt,F_pt, G_pt), efg=(e_pt,f_pt,g_pt))
    raiz = sp.sqrt(H_pt**2 - K_pt)
    return sp.Matrix([H_pt + raiz, H_pt - raiz]).T

def curvaturasPrincipales_pt_xyz(parametrizacion, u, v, x0, y0, z0, curv=None, K=None, H=None):
    """
    Retorna como tupla las curvaturas principales en un punto descrito como x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacio      parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    curv                parametro opcional por si ya se tienen calculadas las curvaturas principales
    K                   parametro opcional por si se tiene ya calculada cruvatura Gauss en el punto deseado
    H                   parametro opcional por si se tiene ya calculada curvatura Media en el punto deseado
    """
    u0, v0 = xyz_to_uv(parametrizacion, u, v, x0, y0, z0)
    return curvaturasPrincipales_pt_uv(parametrizacion, u, v, u0, v0, curv, K, H)
