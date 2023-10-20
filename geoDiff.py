import sympy as sp
from points import xyz_to_uv


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
    return tuple(elem for elem in res)

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
        return tuple(sp.N(normal[i].subs([[u, u0],[v,v0]])) for i in range(3))
    
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    du_parametrizacion_pt = [sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_parametrizacion_pt = [sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    du_parametrizacion_X_dv_parametrizacion_pt = sp.Matrix(sp.Matrix(du_parametrizacion_pt).cross(sp.Matrix(dv_parametrizacion_pt))).normalized()

    return tuple(elem for elem in sp.Matrix(du_parametrizacion_X_dv_parametrizacion_pt))

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

    return E, F, G

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
        return (sp.N(EFG[0].subs([[u, u0],[v,v0]])), sp.N(EFG[1].subs([[u, u0],[v,v0]])), sp.N(EFG[2].subs([[u, u0],[v,v0]])))
    
    du_parametrizacion = [sp.diff(parametrizacion[i], u) for i in range(3)]
    dv_parametrizacion = [sp.diff(parametrizacion[i], v) for i in range(3)]

    du_parametrizacion_pt = [sp.N(du_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_parametrizacion_pt = [sp.N(dv_parametrizacion[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    E_pt=sp.Matrix(du_parametrizacion_pt).dot(sp.Matrix(du_parametrizacion_pt))
    F_pt=sp.Matrix(du_parametrizacion_pt).dot(sp.Matrix(dv_parametrizacion_pt))
    G_pt=sp.Matrix(dv_parametrizacion_pt).dot(sp.Matrix(dv_parametrizacion_pt))

    return E_pt, F_pt, G_pt

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
    
    return e, f, g

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
        return (sp.N(efg[0].subs([[u, u0],[v,v0]])), sp.N(efg[1].subs([[u, u0],[v,v0]])), sp.N(efg[2].subs([[u, u0],[v,v0]])))
    
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
    return sp.simplify(H + raiz), sp.simplify(H - raiz)

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
        return ( sp.N(curv[0].subs([[u, u0],[v,v0]])), sp.N(curv[1].subs([[u, u0],[v,v0]])))
    
    E_pt, F_pt, G_pt = primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)
    e_pt, f_pt, g_pt = segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)
    K_pt = curvaturaGauss_pt_uv(parametrizacion, u, v, u0, v0, EFG=(E_pt,F_pt, G_pt), efg=(e_pt,f_pt,g_pt))
    H_pt = curvaturaMedia_pt_uv(parametrizacion, u, v, u0, v0, EFG=(E_pt,F_pt, G_pt), efg=(e_pt,f_pt,g_pt))
    raiz = sp.sqrt(H_pt**2 - K_pt)
    return H_pt + raiz, H_pt - raiz

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
