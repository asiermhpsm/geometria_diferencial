import sympy as sp
from .utils import xyz_to_uv

"""
Todos los calculos se guardarán en un diccionario de resultados para evitar cálculos repetidos y para centralizar la información.
LEYENDA DE ALMACENAMIENTO DE RESULTADOS:
res = {
    'sup' : ...            #Parametrización de la superficie. Debe ser de tipo sympy.Matrx()
    'u' : ...              #Primera variable de dependencia. Debe ser de tipo sp.Symbol
    'v' : ...              #Segunda variable de dependencia. Debe ser de tipo sp.Symbol

    'du' : ...             #derivada de u
    'dv' : ...             #derivada de v
    'duu' : ...            #derivada de uu
    'duv' : ...            #derivada de uv
    'dvv' : ...            #derivada de vv
    'duXdv' : ...          #du producto vectorial dv
    'norma' : ...          #norma de duXdv
    'normal' : ...         #vector normal
    'E' : ...              #componente E de primera forma fundamental
    'F' : ...              #componente F de primera forma fundamental
    'G' : ...              #componente G de primera forma fundamental
    'e' : ...              #componente e de segunda forma fundamental
    'f' : ...              #componente f de segunda forma fundamental
    'g' : ...              #componente g de segunda forma fundamental
    'tangente' : ...       #Plano tangente general
    'curv_Gauss' : ...     #Curvatura de Gauss
    'curv_media' : ...     #Curvatura media
    'k1'                   #curvatura principal 1
    'k2'                   #curvatura principal 2
    'd1'                   #direccion principal 1
    'd2'                   #direccion principal 2
    'W'                    #Matriz de Weingarten

    'du_pt' : ...             #derivada de u
    'dv_pt' : ...             #derivada de v
    'duu_pt' : ...            #derivada de uu
    'duv_pt' : ...            #derivada de uv
    'dvv_pt' : ...            #derivada de vv
    'duXdv_pt' : ...          #du producto vectorial dv
    'norma_pt' : ...          #norma de duXdv_pt
    'normal_pt' : ...         #vector normal
    'E_pt' : ...              #componente E de primera forma fundamental
    'F_pt' : ...              #componente F de primera forma fundamental
    'G_pt' : ...              #componente G de primera forma fundamental
    'e_pt' : ...              #componente e de segunda forma fundamental
    'f_pt' : ...              #componente f de segunda forma fundamental
    'g_pt' : ...              #componente g de segunda forma fundamental
    'tangente_pt' : ...       #Plano tangente general
    'curv_Gauss_pt' : ...     #Curvatura de Gauss
    'curv_media_pt' : ...     #Curvatura media
    'k1_pt'                   #curvatura principal 1
    'k2_pt'                   #curvatura principal 2
    'd1_pt'                   #direccion principal 1
    'd2_pt'                   #direccion principal 2
    'W_pt'                    #Matriz de Weingarten
}
"""

"""
-------------------------------------------------------------------------------
METODOS AUXILIARES
-------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------
VECTOR NORMAL
-------------------------------------------------------------------------------
"""
def normal(res : dict ={}) -> dict:
    """
    Retorna el vector normal de una superficie
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'duXdv' not in res:
        if 'du' not in res:
            res['du'] = sp.diff(res['sup'], res['u'])
        if 'dv' not in res:
            res['dv'] = sp.diff(res['sup'], res['v'])
        res['duXdv'] = sp.simplify(res['du'].cross(res['dv']))
    res['norma'] = sp.simplify(res['duXdv'].norm())
    res['normal'] = sp.simplify(res['duXdv'].normalized())
    return res

def normal_pt_uv(res : dict ={}) -> dict:
    """
    Retorna el vector normal de una superficie en un punto descrito por u,v
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'duXdv_pt' not in res:
        if not 'du_pt' in res:
            if not 'du' in res:
                res['du'] = sp.diff(res['sup'], res['u'])
            res['du_pt'] = res['du'].subs({res['u']:res['u0'], res['v']:res['v0']}) 
        if not 'dv_pt' in res:
            if not 'dv' in res:
                res['dv'] = sp.diff(res['sup'], res['v'])
            res['dv_pt'] = res['dv'].subs({res['u']:res['u0'], res['v']:res['v0']})
        res['duXdv_pt'] = res['du_pt'].cross(res['dv_pt'])
    res['norma_pt'] = sp.simplify(res['duXdv_pt'].norm())
    res['normal_pt'] = sp.simplify(res['duXdv_pt'].normalized())
    return res

def normal_pt_xyz(res : dict ={}) -> dict:
    """
    Retorna el vector normal de una superficie en un punto descrito por x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return normal_pt_uv(res)


"""
-------------------------------------------------------------------------------
PLANO TANGENTE
-------------------------------------------------------------------------------
"""
def planoTangente(res : dict ={}) -> dict:
    """
    Retorna el plano tangente (sin igualar a cero) de una superficie parametrizada
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'duXdv' not in res:
        if 'du' not in res:
            res['du'] = sp.diff(res['sup'], res['u'])
        if 'dv' not in res:
            res['dv'] = sp.diff(res['sup'], res['v'])
        res['duXdv'] = sp.simplify(res['du'].cross(res['dv']))
    x, y, z = sp.symbols('x, y, z', real = True)
    res['tangente'] = sp.Eq(sp.simplify(res['duXdv'].dot(sp.Matrix([x,y,z]))), sp.simplify(res['duXdv'].dot(res['sup'])))
    return res

def planoTangente_pt_uv(res : dict ={}) -> dict:
    """
    Retorna el plano tangente (sin igualar a cero) de una superficie parametrizada en un punto descrito con u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'duXdv_pt' not in res:
        if not 'du_pt' in res:
            if not 'du' in res:
                res['du'] = sp.diff(res['sup'], res['u'])
            res['du_pt'] = res['du'].subs({res['u']:res['u0'], res['v']:res['v0']}) 
        if not 'dv_pt' in res:
            if not 'dv' in res:
                res['dv'] = sp.diff(res['sup'], res['v'])
            res['dv_pt'] = res['dv'].subs({res['u']:res['u0'], res['v']:res['v0']})
        res['duXdv_pt'] = res['du_pt'].cross(res['dv_pt'])

    x, y, z = sp.symbols('x, y, z', real = True)
    res['tangente_pt'] = sp.Eq(sp.simplify(res['duXdv_pt'].dot(sp.Matrix([x,y,z]))), sp.simplify(res['duXdv_pt'].dot(res['sup'].subs({res['u']:res['u0'], res['v']:res['v0']}))))
    return res

def planoTangente_pt_xyz(res : dict ={}) -> dict:
    """
    Retorna el plano tangente (sin igualar a cero) de una superficie parametrizada en un punto descrito con u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return planoTangente_pt_uv(res)


"""
-------------------------------------------------------------------------------
PRIMERA FORMA FUNDAMENTAL
-------------------------------------------------------------------------------
"""
def primeraFormaFundamental(res : dict ={}) -> dict:
    """
    Retorna la primera forma fundamental en forma de Matrix(E, F, G)
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'du' not in res:
        res['du'] = sp.diff(res['sup'], res['u'])
    if 'dv' not in res:
        res['dv'] = sp.diff(res['sup'], res['v'])

    res['E'] = sp.simplify(res['du'].dot(res['du']))
    res['F'] = sp.simplify(res['du'].dot(res['dv']))
    res['G'] = sp.simplify(res['dv'].dot(res['dv']))

    return res

def primeraFormaFundamental_pt_uv(res : dict ={}) -> dict:
    """
    Retorna en forma de Matrix(E, F, G) la primera forma fundamental en un punto  descrito por u,v
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if not 'du_pt' in res:
        if not 'du' in res:
            res['du'] = sp.diff(res['sup'], res['u'])
        res['du_pt'] = res['du'].subs({res['u']:res['u0'], res['v']:res['v0']}) 
    if not 'dv_pt' in res:
        if not 'dv' in res:
            res['dv'] = sp.diff(res['sup'], res['v'])
        res['dv_pt'] = res['dv'].subs({res['u']:res['u0'], res['v']:res['v0']})

    res['E_pt'] = sp.simplify(res['du_pt'].dot(res['du_pt']))
    res['F_pt'] = sp.simplify(res['du_pt'].dot(res['dv_pt']))
    res['G_pt'] = sp.simplify(res['dv_pt'].dot(res['dv_pt']))

    return res

def primeraFormaFundamental_pt_xyz( res : dict ={}) -> dict:
    """
    Retorna en forma de Matrix(E, F, G) la primera forma fundamental en un punto  descrito por x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return primeraFormaFundamental_pt_uv(res)


"""
-------------------------------------------------------------------------------
SEGUNDA FORMA FUNDAMENTAL
-------------------------------------------------------------------------------
"""
def segundaFormaFundamental(res : dict ={}) -> dict:
    """
    Retorna la segunda forma fundamental en forma de Matrix(e, f, g)
    No se hacen comprobaciones de tipo

    Argumentos:
    
    res          diccionario con todos los res calculados hasta el momento
    """
    if 'du' not in res:
        res['du'] = sp.diff(res['sup'], res['u'])
    if 'dv' not in res:
        res['dv'] = sp.diff(res['sup'], res['v'])
    if 'duu' not in res:
        res['duu'] = sp.diff(res['du'], res['u'])
    if 'duv' not in res:
        res['duv'] = sp.diff(res['du'], res['v'])
    if 'dvv' not in res:
        res['dvv'] = sp.diff( res['dv'], res['v'])
    if 'normal' not in res:
        normal(res)

    res['e'] = sp.simplify( res['normal'].dot(res['duu']))
    res['f'] = sp.simplify( res['normal'].dot(res['duv']))
    res['g'] = sp.simplify( res['normal'].dot(res['dvv']))
    
    return res

def segundaFormaFundamental_pt_uv(res : dict ={}) -> dict:
    """
    Retorna en forma de Matrix(e, f, g) la segunda forma fundamental en un punto  descrito por u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'du' not in res:
        res['du'] = sp.diff(res['sup'], res['u'])
    if 'dv' not in res:
        res['dv'] = sp.diff(res['sup'], res['v'])
    if 'duu_pt' not in res:
        if 'duu' not in res:
            res['duu'] = sp.diff(res['du'], res['u'])
        res['duu_pt'] = res['duu'].subs({res['u']:res['u0'], res['v']:res['v0']})
    if 'duv_pt' not in res:
        if 'duv' not in res:
            res['duv'] = sp.diff(res['du'], res['v'])
        res['duv_pt'] = res['duv'].subs({res['u']:res['u0'], res['v']:res['v0']})
    if 'dvv_pt' not in res:
        if 'dvv' not in res:
            res['dvv'] = sp.diff(res['dv'], res['v'])
        res['dvv_pt'] = res['dvv'].subs({res['u']:res['u0'], res['v']:res['v0']})
    if 'normal_pt' not in res:
        normal_pt_uv(res)

    res['e_pt'] = sp.simplify( res['normal_pt'].dot(res['duu_pt']))
    res['f_pt'] = sp.simplify( res['normal_pt'].dot(res['duv_pt']))
    res['g_pt'] = sp.simplify( res['normal_pt'].dot(res['dvv_pt']))
    
    return res

def segundaFormaFundamental_pt_xyz(res : dict ={}) -> dict:
    """
    Retorna en forma de Matrix(e, f, g) la segunda forma fundamental en un punto  descrito por x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return segundaFormaFundamental_pt_uv(res)


"""
-------------------------------------------------------------------------------
CURVATURA DE GAUSS
-------------------------------------------------------------------------------
"""
def curvaturaGauss(res : dict ={}) -> dict:
    """
    Retorna la curvatura de Gauss
    No se hacen comprobaciones de tipo

    Argumentos:
    
    res          diccionario con todos los res calculados hasta el momento
    """
    if 'E' not in res:
        primeraFormaFundamental(res)
    if 'e' not in res:
        segundaFormaFundamental(res)
    res['K'] = sp.simplify((res['e']*res['g'] - res['f']**2)/(res['E']*res['G'] - res['F']**2))
    return res

def curvaturaGauss_pt_uv(res : dict ={}) -> dict:
    """
    Retorna la curvatura de Gauss en un punto descrito por u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'E_pt' not in res:
        primeraFormaFundamental_pt_uv(res)
    if 'e_pt' not in res:
        segundaFormaFundamental_pt_uv(res)

    res['K_pt'] = sp.simplify((res['e_pt']*res['g_pt'] - res['f_pt']**2)/(res['E_pt']*res['G_pt'] - res['F_pt']**2))
    return res

def curvaturaGauss_pt_xyz(res : dict ={}) -> dict:
    """
    Retorna la curvatura de Gauss en un punto descrito por x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return curvaturaGauss_pt_uv(res)


"""
-------------------------------------------------------------------------------
CURVATURA MEDIA
-------------------------------------------------------------------------------
"""
def curvaturaMedia(res : dict ={}) -> dict:
    """
    Retorna la curvatura media
    No se hacen comprobaciones de tipo

    Argumentos:
    
    res          diccionario con todos los res calculados hasta el momento
    """
    if 'E' not in res:
        primeraFormaFundamental(res)
    if 'e' not in res:
        segundaFormaFundamental(res)
    res['H'] = sp.simplify((res['e']*res['G'] + res['g']*res['E'] - 2*res['f']*res['F'])
                                  /(2*(res['E']*res['G'] - res['F']**2)))
    return res

def curvaturaMedia_pt_uv(res : dict ={}) -> dict:
    """
    Retorna la curvatura media en un punto descrito por u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'E_pt' not in res:
        primeraFormaFundamental_pt_uv(res)
    if 'e_pt' not in res:
        segundaFormaFundamental_pt_uv(res)
    
    res['H_pt'] = sp.simplify((res['e_pt']*res['G_pt'] + res['g_pt']*res['E_pt'] - 2*res['f_pt']*res['F_pt'])
                                     /(2*(res['E_pt']*res['G_pt'] - res['F_pt']**2)))
    return res

def curvaturaMedia_pt_xyz(res : dict ={}) -> dict:
    """
    Retorna la curvatura media en un punto descrito por x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return curvaturaMedia_pt_uv(res)


"""
-------------------------------------------------------------------------------
CURVATURAS PRINCIPALES
-------------------------------------------------------------------------------
"""
def curvaturasPrincipales(res : dict ={}) -> dict:
    """
    Retorna las curvaturas principales como tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    
    res          diccionario con todos los res calculados hasta el momento
    """
    if 'K' not in res:
        curvaturaGauss(res)
    if 'H' not in res:
        curvaturaMedia(res)
    raiz = sp.simplify(sp.sqrt(res['H']**2 - res['K']))
    res['k1'] = sp.simplify(res['H'] + raiz)
    res['k2'] = sp.simplify(res['H'] - raiz)
    return res

def curvaturasPrincipales_pt_uv(res : dict ={}) -> dict:
    """
    Retorna como tupla las curvaturas principales en un punto descrito como u,v
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'K_pt' not in res:
        curvaturaGauss_pt_uv(res)
    if 'H_pt' not in res:
        curvaturaMedia_pt_uv(res)
    raiz = sp.simplify(sp.sqrt(res['H_pt']**2 - res['K_pt']))
    res['k1_pt'] = sp.simplify(res['H_pt'] + raiz)
    res['k2_pt'] = sp.simplify(res['H_pt'] - raiz)
    return res

def curvaturasPrincipales_pt_xyz(res : dict ={}) -> dict:
    """
    Retorna como tupla las curvaturas principales en un punto descrito como x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return curvaturasPrincipales_pt_uv(res)


"""
-------------------------------------------------------------------------------
CLASIFICACION DE UN PUNTO
-------------------------------------------------------------------------------
"""
def clasicPt_uv(res : dict ={}) -> dict:
    """
    Imprime la clasificacion de una superficie en un punto descrito con x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    #Se usa el hecho de que k1*k2=K
    if 'k1_pt' in res:
        K = res['k1_pt']*res['k2_pt']
        if K > 0:
            res['clasif_pt'] = 'Eliptico'
        elif K < 0:
            res['clasif_pt'] = 'Hiperbólitco'
        elif K == 0:
            if sp.simplify(res['k1_pt']-res['k2_pt']) == 0:
                return 'Planar'
            else:
                return 'Parabólico'
    else:
        if 'K_pt' not in res:
            curvaturaGauss_pt_uv(res)
        if res['K_pt'] > 0:
            res['clasif_pt'] = 'Eliptico'
        elif res['K_pt'] < 0:
            res['clasif_pt'] = 'Hiperbólitco'
        elif res['K_pt'] == 0:
            if 'k1_pt' not in res:
                curvaturasPrincipales_pt_uv(res)
            if sp.simplify(res['k1_pt']-res['k2_pt']) == 0:
                res['clasif_pt'] = 'Planar'
            else:
                res['clasif_pt'] = 'Parabólico'
    return res
    
def clasicPt_xyz(res : dict ={}) -> dict:
    """
    Imprime la clasificacion de una superficie en un punto descrito con x, y, z
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return clasicPt_uv(res)


"""
-------------------------------------------------------------------------------
DIRECCIONES PRINCIPALES
-------------------------------------------------------------------------------
"""
def weingarten(res : dict ={}) -> dict:
    """
    Devuelve la matriz de weingarten
    No se hacen comprobaciones de tipo

    Argumentos:
    
    res          diccionario con todos los res calculados hasta el momento
    """
    if 'E' not in res:
        primeraFormaFundamental(res)
    if 'e' not in res:
        segundaFormaFundamental(res)

    denom = res['E']*res['G'] - res['F']**2
    res['W'] = sp.Matrix([[res['e']*res['G']-res['f']*res['F'], 
                    res['f']*res['G']-res['g']*res['F']], 
                    [res['f']*res['E']-res['e']*res['F'], 
                    res['g']*res['E']-res['f']*res['F']]])/denom
    return res

def weingarten_pt_uv(res : dict ={}) -> dict:
    """
    Devuelve la matriz de weingarten en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'E_pt' not in res:
        primeraFormaFundamental_pt_uv(res)
    if 'e_pt' not in res:
        segundaFormaFundamental_pt_uv(res)

    denom = res['E_pt']*res['G_pt'] - res['F_pt']**2
    res['W_pt'] = sp.Matrix([[res['e_pt']*res['G_pt']-res['f_pt']*res['F_pt'], 
                    res['f_pt']*res['G_pt']-res['g_pt']*res['F_pt']], 
                    [res['f_pt']*res['E_pt']-res['e_pt']*res['F_pt'], 
                    res['g_pt']*res['E_pt']-res['f_pt']*res['F_pt']]])/denom
    return res

def weingarten_pt_xyz(res : dict ={}) -> dict:
    """
    Devuelve la matriz de weingarten en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return weingarten_pt_uv(res)


"""
-------------------------------------------------------------------------------
DIRECCIONES PRINCIPALES
-------------------------------------------------------------------------------
"""
def dirPrinc(res : dict ={}) -> dict:
    """
    Calcula las direcciones principales
    No se hacen comprobaciones de tipo

    Argumentos:
    
    res          diccionario con todos los res calculados hasta el momento
    """
    if 'W' not in res:
        weingarten(res)

    autovalores = res['W'].eigenvects(simplify=True)

    if autovalores[0][1] == 2:
        res['k1'] = autovalores[0][0]
        res['k2'] = autovalores[0][0]
        res['d1'] = list(autovalores[0][-1][0])
        res['d2'] = list(autovalores[0][-1][1])
        return res
    elif autovalores[0][1] == 1:
        res['k1'] = autovalores[0][0]
        res['k2'] = autovalores[1][0]
        res['d1'] = list(autovalores[0][-1][0])
        res['d2'] = list(autovalores[1][-1][0])
        return res
    else:
        raise Exception("No se ha podido calcular los autovectores")
    
def dirPrinc_pt_uv(res : dict ={}) -> dict:
    """
    Calcula las direcciones principales en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'W_pt' not in res:
        weingarten_pt_uv(res)

    autovalores = res['W_pt'].eigenvects(simplify=True)

    if autovalores[0][1] == 2:
        res['d1_pt'] = list(autovalores[0][-1][0])
        res['d2_pt'] = list(autovalores[0][-1][1])
        return res
    elif autovalores[0][1] == 1:
        res['d1_pt'] = list(autovalores[0][-1][0])
        res['d2_pt'] = list(autovalores[0][-1][0])
        return res
    else:
        raise Exception("No se ha podido calcular los autovectores")

def dirPrinc_pt_xyz(res : dict ={}) -> dict:
    """
    Calcula las direcciones principales en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return dirPrinc_pt_uv(res)

"""
-------------------------------------------------------------------------------
PUNTOS UMBÍLICOS
-------------------------------------------------------------------------------
"""
def umbilico(res : dict ={}) -> dict:
    """
    Calcula los puntos umbílicos
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los res calculados hasta el momento
    """
    res = curvaturasPrincipales(res)
    if res['k1'] == res['k2']:
        res['umbilico'] = set([(res['u'], res['v'])])
    else:
        soluciones = sp.solve(sp.Eq(res['k1'], res['k2']), (res['u'], res['v']))
        res['umbilico'] = set([(sp.re(sol[0]), sp.re(sol[1])) for sol in soluciones])
    return res

def umbilico_pt_uv(res : dict ={}) -> dict:
    """
    Calcula si un punto es umbílico
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los res calculados hasta el momento
    """
    res = curvaturasPrincipales_pt_uv(res)
    res['umbilico_pt'] = res['k1_pt']== res['k2_pt']
    return res

def umbilico_pt_xyz(res : dict ={}) -> dict:
    """
    Calcula los puntos umbílicos
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los res calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return dirPrinc_pt_uv(res)

"""
-------------------------------------------------------------------------------
CÁLCULO COMPLETO
-------------------------------------------------------------------------------
"""
def descripccion(res : dict ={}) -> dict:
    """
    Hace un cálculo general de todo lo que pueda
    No se hacen comprobaciones de tipo

    Argumentos:
    
    res          diccionario con todos los res calculados hasta el momento
    """
    curvaturaGauss(res)
    curvaturaMedia(res)
    planoTangente(res)
    denom = res['E']*res['G'] - res['F']**2
    W = sp.Matrix([[res['e']*res['G']-res['f']*res['F'], 
                    res['f']*res['G']-res['g']*res['F']], 
                    [res['f']*res['E']-res['e']*res['F'], 
                    res['g']*res['E']-res['f']*res['F']]])/denom
    res['W'] = sp.simplify(W)
    autovalores = W.eigenvects(simplify=True)

    if autovalores[0][1] == 2:
        res['k1'] = autovalores[0][0]
        res['k2'] = autovalores[0][0]
        res['d1'] = list(autovalores[0][-1][0])
        res['d2'] = list(autovalores[0][-1][1])
        return res
    elif autovalores[0][1] == 1:
        res['k1'] = autovalores[0][0]
        res['k2'] = autovalores[1][0]
        res['d1'] = list(autovalores[0][-1][0])
        res['d2'] = list(autovalores[1][-1][0])
        return res
    else:
        raise Exception("No se ha podido calcular los autovectores")

def descripccion_pt_uv(res : dict ={}) -> dict:
    """
    Hace un cálculo general de todo lo que pueda
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    curvaturaGauss_pt_uv(res)
    curvaturaMedia_pt_uv(res)
    planoTangente_pt_uv(res)
    denom = res['E_pt']*res['G_pt'] - res['F_pt']**2
    W = sp.Matrix([[res['e_pt']*res['G_pt']-res['f_pt']*res['F_pt'], 
                    res['f_pt']*res['G_pt']-res['g_pt']*res['F_pt']], 
                    [res['f_pt']*res['E_pt']-res['e_pt']*res['F_pt'], 
                    res['g_pt']*res['E_pt']-res['f_pt']*res['F_pt']]])/denom
    res['W_pt'] = sp.simplify(W)
    autovalores = W.eigenvects(simplify=True)

    if autovalores[0][1] == 2:
        res['k1_pt'] = autovalores[0][0]
        res['k2_pt'] = autovalores[0][0]
        res['d1_pt'] = list(autovalores[0][-1][0])
        res['d2_pt'] = list(autovalores[0][-1][1])
    elif autovalores[0][1] == 1:
        res['k1_pt'] = autovalores[0][0]
        res['k2_pt'] = autovalores[1][0]
        res['d1_pt'] = list(autovalores[0][-1][0])
        res['d2_pt'] = list(autovalores[1][-1][0])
    else:
        raise Exception("No se ha podido calcular los autovectores")
    clasicPt_uv(res)
    return res
    
def descripccion_pt_xyz(res : dict ={}) -> dict:
    """
    Hace un cálculo general de todo lo que pueda
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    res['u0'], res['v0'] = xyz_to_uv(res['sup'], res['u'], res['v'], res['x0'], res['y0'], res['z0'])
    return descripccion_pt_uv(res)