import sympy as sp

"""resultados = {
    'du' : ...             #derivada de u
    'dv' : ...             #derivada de v
    'duu' : ...            #derivada de uu
    'duv' : ...            #derivada de uv
    'dvv' : ...            #derivada de vv
    'duXdv' : ...          #du producto vectorial dv
    'normal' : ...         #vector normal
    'E' : ...              #componente E de primera forma fundamental
    'F' : ...              #componente F de primera forma fundamental
    'G' : ...              #componente G de primera forma fundamental
    'e' : ...              #componente e de segunda forma fundamental
    'f' : ...              #componente f de segunda forma fundamental
    'g' : ...              #componente g de segunda forma fundamental
    'tangente' : ...       #Plano tangente general
    'tangente_afin' : ...  #Plano tangente general
    'curv_Gauss' : ...     #Curvatura de Gauss
    'curv_media' : ...     #Curvatura media
    'k1'                   #curvatura principal 1
    'k2'                   #curvatura principal 2
    'd1'                   #direccion principal 1
    'd2'                   #direccion principal 2

    'du_pt' : ...             #derivada de u
    'dv_pt' : ...             #derivada de v
    'duu_pt' : ...            #derivada de uu
    'duv_pt' : ...            #derivada de uv
    'dvv_pt' : ...            #derivada de vv
    'duXdv_pt' : ...          #du producto vectorial dv
    'normal_pt' : ...         #vector normal
    'E_pt' : ...              #componente E de primera forma fundamental
    'F_pt' : ...              #componente F de primera forma fundamental
    'G_pt' : ...              #componente G de primera forma fundamental
    'e_pt' : ...              #componente e de segunda forma fundamental
    'f_pt' : ...              #componente f de segunda forma fundamental
    'g_pt' : ...              #componente g de segunda forma fundamental
    'tangente_pt' : ...       #Plano tangente general
    'tangente_afin_pt' : ...  #Plano tangente general
    'curv_Gauss_pt' : ...     #Curvatura de Gauss
    'curv_media_pt' : ...     #Curvatura media
    'k1_pt'                   #curvatura principal 1
    'k2_pt'                   #curvatura principal 2
    'd1_pt'                   #direccion principal 1
    'd2_pt'                   #direccion principal 2
}"""

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
    if not isinstance(parametrizacion, sp.Matrix):
        parametrizacion = sp.Matrix(parametrizacion)
    return tuple(parametrizacion.subs({u:u0, v:v0}))

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
    punto = (float(x0), float(y0), float(z0))
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
def normal(parametrizacion, u, v, resultados={}):
    """
    Retorna el vector normal de una superficie
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if not isinstance(parametrizacion, sp.Matrix):
        parametrizacion = sp.Matrix(parametrizacion)
    if 'duXdv' not in resultados:
        if 'du' not in resultados:
            resultados['du'] = sp.diff(parametrizacion, u)
        if 'dv' not in resultados:
            resultados['dv'] = sp.diff(parametrizacion, v)
        resultados['duXdv'] = resultados['du'].cross(resultados['dv'])
    resultados['normal'] = normaliza(resultados['duXdv'])
    return resultados

def normal_pt_uv(parametrizacion, u, v, u0, v0, resultados={}):
    """
    Retorna el vector normal de una superficie en un punto descrito por u,v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if not isinstance(parametrizacion, sp.Matrix):
        parametrizacion = sp.Matrix(parametrizacion)
    if 'duXdv_pt' not in resultados:
        if not 'du_pt' in resultados:
            if not 'du' in resultados:
                resultados['du'] = sp.diff(parametrizacion, u)
            resultados['du_pt'] = resultados['du'].subs({u:u0, v:v0}) 
        if not 'dv_pt' in resultados:
            if not 'dv' in resultados:
                resultados['dv'] = sp.diff(parametrizacion, v)
            resultados['dv_pt'] = resultados['dv'].subs({u:u0, v:v0})
        resultados['duXdv_pt'] = resultados['du_pt'].cross(resultados['dv_pt'])
    resultados['normal_pt'] = normaliza(resultados['duXdv_pt'])
    return resultados

def normal_pt_xyz(parametrizacion, u, v, x0, y0, z0, resultados={}):
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
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    u0, v0 = xyz_to_uv(parametrizacion, u, v, x0, y0, z0)
    return normal_pt_uv(parametrizacion, u, v, u0, v0, resultados)


"""
-------------------------------------------------------------------------------
PLANO TANGENTE
-------------------------------------------------------------------------------
"""
def planoTangente(parametrizacion, u, v, resultados={}):
    """
    Retorna el plano tangente (sin igualar a cero) de una superficie parametrizada
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if not isinstance(parametrizacion, sp.Matrix):
        parametrizacion = sp.Matrix(parametrizacion)
    if 'duXdv' not in resultados:
        if 'du' not in resultados:
            resultados['du'] = sp.diff(parametrizacion, u)
        if 'dv' not in resultados:
            resultados['dv'] = sp.diff(parametrizacion, v)
        resultados['duXdv'] = resultados['du'].cross(resultados['dv'])
    x, y, z = sp.symbols('x, y, z', real = True)
    #TODO-¿igualo a 0?
    resultados['tangente'] = resultados['duXdv'].dot(sp.Matrix([x,y,z])) - sp.simplify(resultados['duXdv'].dot(parametrizacion))
    return resultados


def planoTangente_pt_uv(parametrizacion, u, v, u0, v0, resultados={}):
    """
    Retorna el plano tangente (sin igualar a cero) de una superficie parametrizada en un punto descrito con u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if not isinstance(parametrizacion, sp.Matrix):
        parametrizacion = sp.Matrix(parametrizacion)
    if 'duXdv_pt' not in resultados:
        if not 'du_pt' in resultados:
            if not 'du' in resultados:
                resultados['du'] = sp.diff(parametrizacion, u)
            resultados['du_pt'] = resultados['du'].subs({u:u0, v:v0}) 
        if not 'dv_pt' in resultados:
            if not 'dv' in resultados:
                resultados['dv'] = sp.diff(parametrizacion, v)
            resultados['dv_pt'] = resultados['dv'].subs({u:u0, v:v0})
        resultados['duXdv_pt'] = resultados['du_pt'].cross(resultados['dv_pt'])

    x, y, z = sp.symbols('x, y, z', real = True)
    resultados['tangente_afin_pt'] = resultados['duXdv_pt'].dot(sp.Matrix([x,y,z])) - sp.simplify(resultados['duXdv_pt'].dot(parametrizacion))
    return resultados

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
def primeraFormaFundamental(parametrizacion, u, v, resultados={}):
    """
    Retorna la primera forma fundamental en forma de Matrix(E, F, G)
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if not isinstance(parametrizacion, sp.Matrix):
        parametrizacion = sp.Matrix(parametrizacion)
    if 'du' not in resultados:
        resultados['du'] = sp.diff(parametrizacion, u)
    if 'dv' not in resultados:
        resultados['dv'] = sp.diff(parametrizacion, v)

    resultados['E'] = sp.simplify(resultados['du'].dot(resultados['du']))
    resultados['F'] = sp.simplify(resultados['du'].dot(resultados['dv']))
    resultados['G'] = sp.simplify(resultados['dv'].dot(resultados['dv']))

    return resultados

def primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, resultados={}):
    """
    Retorna en forma de Matrix(E, F, G) la primera forma fundamental en un punto  descrito por u,v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if not isinstance(parametrizacion, sp.Matrix):
        parametrizacion = sp.Matrix(parametrizacion)
    if not 'du_pt' in resultados:
        if not 'du' in resultados:
            resultados['du'] = sp.diff(parametrizacion, u)
        resultados['du_pt'] = resultados['du'].subs({u:u0, v:v0}) 
    if not 'dv_pt' in resultados:
        if not 'dv' in resultados:
            resultados['dv'] = sp.diff(parametrizacion, v)
        resultados['dv_pt'] = resultados['dv'].subs({u:u0, v:v0})

    resultados['E_pt'] = sp.simplify(resultados['du'].dot(resultados['du']))
    resultados['F_pt'] = sp.simplify(resultados['du'].dot(resultados['dv']))
    resultados['G_pt'] = sp.simplify(resultados['dv'].dot(resultados['dv']))

    return resultados

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
def segundaFormaFundamental(parametrizacion, u, v, resultados={}):
    """
    Retorna la segunda forma fundamental en forma de Matrix(e, f, g)
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if not isinstance(parametrizacion, sp.Matrix):
        parametrizacion = sp.Matrix(parametrizacion)
    if 'du' not in resultados:
        resultados['du'] = sp.diff(parametrizacion, u)
    if 'dv' not in resultados:
        resultados['dv'] = sp.diff(parametrizacion, v)
    if 'duu' not in resultados:
        resultados['duu'] = sp.diff(resultados['du'], u)
    if 'duv' not in resultados:
        resultados['duv'] = sp.diff(resultados['du'], v)
    if 'dvv' not in resultados:
        resultados['dvv'] = sp.diff( resultados['dv'], v)
    if 'normal' not in resultados:
        normal(parametrizacion, u, v, resultados)

    resultados['e'] = sp.simplify( resultados['normal'].dot(resultados['duu']))
    resultados['f'] = sp.simplify( resultados['normal'].dot(resultados['duv']))
    resultados['g'] = sp.simplify( resultados['normal'].dot(resultados['dvv']))
    
    return resultados

def segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, resultados={}):
    """
    Retorna en forma de Matrix(e, f, g) la segunda forma fundamental en un punto  descrito por u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if not isinstance(parametrizacion, sp.Matrix):
        parametrizacion = sp.Matrix(parametrizacion)
    if 'du' not in resultados:
        resultados['du'] = sp.diff(parametrizacion, u)
    if 'dv' not in resultados:
        resultados['dv'] = sp.diff(parametrizacion, v)
    if 'duu_pt' not in resultados:
        if 'duu' not in resultados:
            resultados['duu'] = sp.diff(resultados['du'], u)
        resultados['duu_pt'] = resultados['duu'].subs({u:u0, v:v0})
    if 'duv_pt' not in resultados:
        if 'duv' not in resultados:
            resultados['duv'] = sp.diff(resultados['du'], v)
        resultados['duv_pt'] = resultados['duv'].subs({u:u0, v:v0})
    if 'dvv_pt' not in resultados:
        if 'dvv' not in resultados:
            resultados['dvv'] = sp.diff(resultados['dv'], v)
        resultados['dvv_pt'] = resultados['dvv'].subs({u:u0, v:v0})
    if 'normal_pt' not in resultados:
        normal_pt_uv(parametrizacion, u, v, u0, v0, resultados)

    resultados['e_pt'] = sp.simplify( resultados['normal_pt'].dot(resultados['duu_pt']))
    resultados['f_pt'] = sp.simplify( resultados['normal_pt'].dot(resultados['duv_pt']))
    resultados['g_pt'] = sp.simplify( resultados['normal_pt'].dot(resultados['dvv_pt']))
    
    return resultados

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
def curvaturaGauss(parametrizacion, u, v, resultados={}):
    """
    Retorna la curvatura de Gauss
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if 'E' not in resultados:
        primeraFormaFundamental(parametrizacion, u, v, resultados)
    if 'e' not in resultados:
        segundaFormaFundamental(parametrizacion, u, v, resultados)
    resultados['K'] = sp.simplify((resultados['e']*resultados['g'] - resultados['f']**2)/(resultados['E']*resultados['G'] - resultados['F']**2))
    return resultados

def curvaturaGauss_pt_uv(parametrizacion, u, v, u0, v0, resultados={}):
    """
    Retorna la curvatura de Gauss en un punto descrito por u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if 'E_pt' not in resultados:
        primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, resultados)
    if 'e_pt' not in resultados:
        segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, resultados)

    resultados['K_pt'] = sp.simplify((resultados['e_pt']*resultados['g_pt'] - resultados['f_pt']**2)/(resultados['E_pt']*resultados['G_pt'] - resultados['F_pt']**2))
    return resultados

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
def curvaturaMedia(parametrizacion, u, v, resultados={}):
    """
    Retorna la curvatura media
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if 'E' not in resultados:
        primeraFormaFundamental(parametrizacion, u, v, resultados)
    if 'e' not in resultados:
        segundaFormaFundamental(parametrizacion, u, v, resultados)
    resultados['H'] = sp.simplify((resultados['e']*resultados['G'] + resultados['g']*resultados['E'] - 2*resultados['f']*resultados['F'])
                                  /(2*(resultados['E']*resultados['G'] - resultados['F']**2)))
    return resultados

def curvaturaMedia_pt_uv(parametrizacion, u, v, u0, v0, resultados={}):
    """
    Retorna la curvatura media en un punto descrito por u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if 'E_pt' not in resultados:
        primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, resultados)
    if 'e_pt' not in resultados:
        segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, resultados)
    
    resultados['H_pt'] = sp.simplify((resultados['e_pt']*resultados['G_pt'] + resultados['g_pt']*resultados['E_pt'] - 2*resultados['f_pt']*resultados['F_pt'])
                                     /(2*(resultados['E_pt']*resultados['G_pt'] - resultados['F_pt']**2)))
    return resultados

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
def curvaturasPrincipales(parametrizacion, u, v, resultados={}):
    """
    Retorna las curvaturas principales como tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if 'K' not in resultados:
        curvaturaGauss(parametrizacion, u, v, resultados)
    if 'H' not in resultados:
        curvaturaMedia(parametrizacion, u, v, resultados)
    raiz = sp.simplify(sp.sqrt(resultados['H']**2 - resultados['K']))
    resultados['k1'] = sp.simplify(resultados['H'] + raiz)
    resultados['k2'] = sp.simplify(resultados['H'] - raiz)
    return resultados

def curvaturasPrincipales_pt_uv(parametrizacion, u, v, u0, v0, resultados={}):
    """
    Retorna como tupla las curvaturas principales en un punto descrito como u,v
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacio      parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if 'K_pt' not in resultados:
        curvaturaGauss_pt_uv(parametrizacion, u, v, u0, v0, resultados)
    if 'H_pt' not in resultados:
        curvaturaMedia_pt_uv(parametrizacion, u, v, u0, v0, resultados)
    raiz = sp.simplify(sp.sqrt(resultados['H_pt']**2 - resultados['K_pt']))
    resultados['k1_pt'] = sp.simplify(resultados['H_pt'] + raiz)
    resultados['k2_pt'] = sp.simplify(resultados['H_pt'] - raiz)
    return resultados

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
def clasicPt_uv(parametrizacion, u, v, u0, v0, resultados={}):
    """
    Imprime la clasificacion de una superficie en un punto descrito con x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    #Se usa el hecho de que k1*k2=K
    if 'k1_pt' in resultados:
        K = resultados['k1_pt']*resultados['k2_pt']
        if K > 0:
            resultados['clasif_pt'] = 'Eliptico'
        elif K < 0:
            resultados['clasif_pt'] = 'Hiperbólitco'
        elif K == 0:
            if sp.simplify(resultados['k1_pt']-resultados['k2_pt']) == 0:
                return 'Planar'
            else:
                return 'Parabólico'
    else:
        if 'K_pt' not in resultados:
            curvaturaGauss_pt_uv(parametrizacion, u, v, u0, v0, resultados)
        if resultados['K_pt'] > 0:
            resultados['clasif_pt'] = 'Eliptico'
        elif resultados['K_pt'] < 0:
            resultados['clasif_pt'] = 'Hiperbólitco'
        elif resultados['K_pt'] == 0:
            if 'k1_pt' not in resultados:
                curvaturasPrincipales_pt_uv(parametrizacion, u, v, u0, v0, resultados)
            if sp.simplify(resultados['k1_pt']-resultados['k2_pt']) == 0:
                resultados['clasif_pt'] = 'Planar'
            else:
                resultados['clasif_pt'] = 'Parabólico'
    

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
def dirPrinc_pt(parametrizacion, u, v, resultados={}):
    """
    Calcula las direcciones principales en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if 'E' not in resultados:
        primeraFormaFundamental(parametrizacion, u, v, resultados)
    if 'e' not in resultados:
        segundaFormaFundamental(parametrizacion, u, v, resultados)

    denom = resultados['E']*resultados['G'] - resultados['F']**2
    W = sp.Matrix([[resultados['e']*resultados['G']-resultados['f']*resultados['F'], 
                    resultados['f']*resultados['G']-resultados['g']*resultados['F']], 
                    [resultados['f']*resultados['E']-resultados['e']*resultados['F'], 
                    resultados['g']*resultados['E']-resultados['f']*resultados['F']]])/denom
    autovalores = W.eigenvects(simplify=True)

    if autovalores[0][1] == 2:
        resultados['d1'] = tuple(autovalores[0][-1][0])
        resultados['d2'] = tuple(autovalores[0][-1][1])
        return resultados
    elif autovalores[0][1] == 1:
        resultados['d1'] = tuple(autovalores[0][-1][0])
        resultados['d2'] = tuple(autovalores[0][-1][0])
        return resultados
    else:
        raise Exception("No se ha podido calcular los autovectores")
    
def dirPrinc_pt_uv(parametrizacion, u, v, u0, v0, resultados={}):
    """
    Calcula las direcciones principales en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0                  valor u del punto
    v0                  valor v del punto
    resultados          diccionario con todos los resultados calculados hasta el momento
    """
    if 'E_pt' not in resultados:
        primeraFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, resultados)
    if 'e_pt' not in resultados:
        segundaFormaFundamental_pt_uv(parametrizacion, u, v, u0, v0, resultados)

    denom = resultados['E_pt']*resultados['G_pt'] - resultados['F_pt']**2
    W = sp.Matrix([[resultados['e_pt']*resultados['G_pt']-resultados['f_pt']*resultados['F_pt'], 
                    resultados['f_pt']*resultados['G_pt']-resultados['g_pt']*resultados['F_pt']], 
                    [resultados['f_pt']*resultados['E_pt']-resultados['e_pt']*resultados['F_pt'], 
                    resultados['g_pt']*resultados['E_pt']-resultados['f_pt']*resultados['F_pt']]])/denom
    autovalores = W.eigenvects(simplify=True)

    if autovalores[0][1] == 2:
        resultados['d1_pt'] = tuple(autovalores[0][-1][0])
        resultados['d2_pt'] = tuple(autovalores[0][-1][1])
        return resultados
    elif autovalores[0][1] == 1:
        resultados['d1_pt'] = tuple(autovalores[0][-1][0])
        resultados['d2_pt'] = tuple(autovalores[0][-1][0])
        return resultados
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