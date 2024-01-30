import sympy as sp

"""
-------------------------------------------------------------------------------
METODOS AUXILIARES
-------------------------------------------------------------------------------
"""
def norm(vector):
    """
    Retorna la norma de un vector
    No se hacen comprobaciones de tipo

    Argumentos:
    vector     lista con el vector en cuestion
    """
    sum = 0
    for elem in vector:
        sum = sum + elem**2
    return sp.simplify(sp.sqrt(sum))

def normaliza(vector):
    """
    Retorna el vector normalizado
    No se hacen comprobaciones de tipo

    Argumentos:
    vector     lista con el vector en cuestion
    """
    return sp.simplify(vector/norm(vector))


"""
-------------------------------------------------------------------------------
TRANSFORMACIONES DE PUNTOS
-------------------------------------------------------------------------------
"""
def uv_to_xyz(parametrizacion, u, v, u0, v0):
    """
    Sustituye u y v en la superficie parametrizada
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    x = float(sp.N(parametrizacion[0].subs([[u, u0],[v,v0]])))
    y = float(sp.N(parametrizacion[1].subs([[u, u0],[v,v0]])))
    z = float(sp.N(parametrizacion[2].subs([[u, u0],[v,v0]])))
    return x, y, z


def xyz_to_uv(parametrizacion, u, v, x0, y0, z0):
    """
    Dado un x,y,z devuelve su valor u y v de una superficie parametrizada. Se devuelve la primera solucion que se encuentre
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    x0                  valor x del punto
    y0                  valor y del punto
    z0                  valor z del punto
    """
    punto = (x0, y0, z0)
    ecuaciones = [sp.Eq(s, p) for s, p in zip(parametrizacion, punto)]
    soluciones = sp.solve(ecuaciones, (u, v))
    if not soluciones:
        raise('El punto dado no esta en la superficie.')
    
    #TODO- devuelvo todas las soluciones o solo una?
    if isinstance(soluciones, dict):
        return soluciones[u] ,soluciones[v]
    else:
        return soluciones[0]


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
    du_parametrizacion = [sp.diff(comp, u) for comp in parametrizacion]
    dv_parametrizacion = [sp.diff(comp, v) for comp in parametrizacion]

    res = normaliza(sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion)))
    return sp.Matrix([elem for elem in res]).T

def normal_pt_uv(parametrizacion, u, v, u0, v0):
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
    du_parametrizacion = [sp.diff(comp, u) for comp in parametrizacion]
    dv_parametrizacion = [sp.diff(comp, v) for comp in parametrizacion]

    du_parametrizacion_pt = [sp.N(comp.subs([[u, u0],[v,v0]])) for comp in du_parametrizacion]
    dv_parametrizacion_pt = [sp.N(comp.subs([[u, u0],[v,v0]])) for comp in dv_parametrizacion]

    res = normaliza(sp.Matrix(sp.Matrix(du_parametrizacion_pt).cross(sp.Matrix(dv_parametrizacion_pt))))
    return sp.Matrix([elem for elem in res]).T

def normal_pt_xyz(parametrizacion, u, v, x0, y0, z0):
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
    return normal_pt_uv(parametrizacion, u, v, u0, v0)


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
    du_parametrizacion = [sp.diff(comp, u) for comp in parametrizacion]
    dv_parametrizacion = [sp.diff(comp, v) for comp in parametrizacion]

    x, y, z = sp.symbols('x, y, z', real = True)
    #TODO-¿igualo a 0?
    return sp.Matrix(du_parametrizacion).cross(sp.Matrix(dv_parametrizacion)).dot(sp.Matrix([x,y,z]))

def planoTangente_pt_uv(parametrizacion, u, v, u0, v0):
    """
    Retorna el plano tangente (sin igualar a cero) de una superficie parametrizada en un punto descrito con u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    du_parametrizacion = [sp.diff(comp, u) for comp in parametrizacion]
    dv_parametrizacion = [sp.diff(comp, v) for comp in parametrizacion]

    parametrizacion_pt = [sp.N(comp.subs([[u, u0],[v,v0]])) for comp in parametrizacion]
    du_parametrizacion_pt = [sp.N(comp.subs([[u, u0],[v,v0]])) for comp in du_parametrizacion]
    dv_parametrizacion_pt = [sp.N(comp.subs([[u, u0],[v,v0]])) for comp in dv_parametrizacion]

    x, y, z = sp.symbols('x, y, z', real = True)
    xyz = [x,y,z]
    return sp.Matrix( sp.Matrix(du_parametrizacion_pt).cross(sp.Matrix(dv_parametrizacion_pt)) ).dot( sp.Matrix( [(xyz[i] - parametrizacion_pt[i]) for i in range(3)]) )

def planoTangente_pt_xyz(parametrizacion, u, v, x0, y0,z0):
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
    """
    u0, v0 = xyz_to_uv(parametrizacion, u, v, x0, y0, z0)
    return planoTangente_pt_uv(parametrizacion, u, v, u0, v0)


"""
-------------------------------------------------------------------------------
PRIMERA FORMA FUNDAMENTAL
-------------------------------------------------------------------------------
"""
def primeraFormaFundamental(parametrizacion, u, v):
    """
    Retorna la primera forma fundamental en forma de Matrix(E, F, G)
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    du_parametrizacion = sp.simplify(sp.Matrix([sp.diff(comp, u) for comp in parametrizacion]))
    dv_parametrizacion = sp.simplify(sp.Matrix([sp.diff(comp, v) for comp in parametrizacion]))

    E=sp.simplify(du_parametrizacion.dot(du_parametrizacion))
    F=sp.simplify(du_parametrizacion.dot(dv_parametrizacion))
    G=sp.simplify(dv_parametrizacion.dot(dv_parametrizacion))

    return sp.Matrix([E, F, G]).T

def primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0):
    """
    Retorna en forma de Matrix(E, F, G) la primera forma fundamental en un punto  descrito por u,v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    du_parametrizacion = [sp.diff(comp, u) for comp in parametrizacion]
    dv_parametrizacion = [sp.diff(comp, v) for comp in parametrizacion]

    du_parametrizacion_pt = sp.simplify(sp.Matrix([sp.N(comp.subs([[u, u0],[v,v0]])) for comp in du_parametrizacion]))
    dv_parametrizacion_pt = sp.simplify(sp.Matrix([sp.N(comp.subs([[u, u0],[v,v0]])) for comp in dv_parametrizacion]))

    E_pt=sp.simplify(du_parametrizacion_pt.dot(du_parametrizacion_pt))
    F_pt=sp.simplify(du_parametrizacion_pt.dot(dv_parametrizacion_pt))
    G_pt=sp.simplify(dv_parametrizacion_pt.dot(dv_parametrizacion_pt))

    return sp.Matrix([E_pt, F_pt, G_pt]).T

def primeraFormaFundamental_pt_xyz(parametrizacion, u, v, x0, y0, z0):
    """
    Retorna en forma de Matrix(E, F, G) la primera forma fundamental en un punto  descrito por x, y, z
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
    Retorna la segunda forma fundamental en forma de Matrix(e, f, g)
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    du_parametrizacion = sp.simplify(sp.Matrix([sp.diff(comp, u) for comp in parametrizacion]))
    dv_parametrizacion = sp.simplify(sp.Matrix([sp.diff(comp, v) for comp in parametrizacion]))
    duu_parametrizacion = sp.simplify(sp.Matrix([sp.diff(comp, u) for comp in du_parametrizacion]))
    duv_parametrizacion = sp.simplify(sp.Matrix([sp.diff(comp, v) for comp in du_parametrizacion]))
    dvv_parametrizacion = sp.simplify(sp.Matrix([sp.diff(comp, v) for comp in dv_parametrizacion]))

    n = normal(parametrizacion, u, v)

    e = sp.simplify(n.dot(duu_parametrizacion))
    f = sp.simplify(n.dot(duv_parametrizacion))
    g = sp.simplify(n.dot(dvv_parametrizacion))
    
    return sp.Matrix([e, f, g]).T

def segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0):
    """
    Retorna en forma de Matrix(e, f, g) la segunda forma fundamental en un punto  descrito por u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    du_parametrizacion = [sp.simplify(sp.diff(comp, u)) for comp in parametrizacion]
    dv_parametrizacion = [sp.simplify(sp.diff(comp, v)) for comp in parametrizacion]
    duu_parametrizacion = [sp.simplify(sp.diff(comp, u)) for comp in du_parametrizacion]
    duv_parametrizacion = [sp.simplify(sp.diff(comp, v)) for comp in du_parametrizacion]
    dvv_parametrizacion = [sp.simplify(sp.diff(comp, v)) for comp in dv_parametrizacion]

    duu_parametrizacion_pt = sp.simplify(sp.Matrix([sp.N(comp.subs([[u, u0],[v,v0]])) for comp in duu_parametrizacion]))
    duv_parametrizacion_pt = sp.simplify(sp.Matrix([sp.N(comp.subs([[u, u0],[v,v0]])) for comp in duv_parametrizacion]))
    dvv_parametrizacion_pt = sp.simplify(sp.Matrix([sp.N(comp.subs([[u, u0],[v,v0]])) for comp in dvv_parametrizacion]))

    n_pt = normal_pt_uv(parametrizacion, u, v, u0, v0)

    e_pt = sp.simplify(n_pt.dot(duu_parametrizacion_pt))
    f_pt = sp.simplify(n_pt.dot(duv_parametrizacion_pt))
    g_pt = sp.simplify(n_pt.dot(dvv_parametrizacion_pt))

    return sp.Matrix([e_pt, f_pt, g_pt]).T

def segundaFormaFundamental_pt_xyz(parametrizacion, u, v, x0, y0, z0):
    """
    Retorna en forma de Matrix(e, f, g) la segunda forma fundamental en un punto  descrito por x, y, z
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
    x0                  valor x del punto
    y0                  valor y del punto
    z0                  valor z del punto
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
def clasicPt_uv(parametrizacion, u, v, u0, v0):
    """
    Imprime la clasificacion de una superficie en un punto descrito con x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    """
    k1, k2 = curvaturasPrincipales_pt_uv(parametrizacion, u, v, u0, v0)
    if k1*k2 > 0:
        return 'Eliptico'
    elif k1*k2 < 0:
        return 'Hiperbólitco'
    elif k1*k2 == 0:
        if sp.simplify(k1-k2) == 0:
            return 'Planar'
        else:
            return 'Parabólico'

def clasicPt_xyz(parametrizacion, u, v, x0, y0, z0):
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
    return clasicPt_uv(parametrizacion, u, v, u0, v0)


"""
-------------------------------------------------------------------------------
DIRECCIONES PRINCIPALES
-------------------------------------------------------------------------------
"""
def dirPrinc_pt(parametrizacion, u, v):
    """
    Calcula las direcciones principales en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    E, F, G = primeraFormaFundamental(parametrizacion, u, v)
    e, f, g = segundaFormaFundamental(parametrizacion, u, v)

    denom = E*G - F**2
    W = sp.Matrix([[e*G-f*F, f*G-g*F], [f*E-e*F, g*E-f*F]])/denom
    autovalores = W.eigenvects(simplify=True)

    if autovalores[0][1] == 2:
        return tuple(autovalores[0][-1][0]), tuple(autovalores[0][-1][1])
    elif autovalores[0][1] == 1:
        return tuple(autovalores[0][-1][0]), tuple(autovalores[1][-1][0])
    else:
        raise Exception("No se ha podido calcular los autovectores")
    

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
    E_pt, F_pt, G_pt = primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)
    e_pt, f_pt, g_pt = segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0)

    denom = E_pt*G_pt - F_pt**2
    W = sp.Matrix([[e_pt*G_pt-f_pt*F_pt, f_pt*G_pt-g_pt*F_pt], [f_pt*E_pt-e_pt*F_pt, g_pt*E_pt-f_pt*F_pt]])/denom
    autovalores = W.eigenvects(simplify=True)

    if autovalores[0][1] == 2:
        return tuple(autovalores[0][-1][0]), tuple(autovalores[0][-1][1])
    elif autovalores[0][1] == 1:
        return tuple(autovalores[0][-1][0]), tuple(autovalores[1][-1][0])
    else:
        raise Exception("No se ha podido calcular los autovectores")

def dirPrinc_pt_xyz(parametrizacion, u, v, x0, y0, z0):
    """
    Calcula las direcciones principales en un punto
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
    return dirPrinc_pt_uv(parametrizacion, u, v, u0, v0)