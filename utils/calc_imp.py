import sympy as sp

"""
Todos los calculos se guardarán en un diccionario de resultados para evitar cálculos repetidos y para centralizar la información.
LEYENDA DE ALMACENAMIENTO DE RESULTADOS:
res = {
    'f' : ...            #Ecuación de la superficie. Debe ser expresión que hace que al igualarla a 0 de la ecuación de la superficie
    'x' : ...              #Primera variable de dependencia. Debe ser de tipo sp.Symbol
    'y' : ...              #Segunda variable de dependencia. Debe ser de tipo sp.Symbol
    'z' : ...              #Tercera variable de dependencia. Debe ser de tipo sp.Symbol

    'x0': ...              #Componente x del punto de interés
    'y0': ...              #Componente y del punto de interés
    'z0': ...              #Componente z del punto de interés

    'dx' : ...             #Derivada de la superficie con respecto a x
    'dy' : ...             #Derivada de la superficie con respecto a y
    'dz' : ...             #Derivada de la superficie con respecto a z
    'gradiente' : ...     #gradiente de la superficie
    'normal' : ...         #Vector normal a la superficie
    'tangente' : ...       #Vector tangente a la superficie

    'dx_pt' : ...           #Derivada de la superficie con respecto a x en el punto indicado
    'dy_pt' : ...           #Derivada de la superficie con respecto a y en el punto indicado
    'dz_pt' : ...           #Derivada de la superficie con respecto a z en el punto indicado
    'gradiente_pt' : ...     #gradiente de la superficie en el punto indicado
    'normal_pt' : ...         #Vector normal a la superficie en el punto indicado
    'tangente_pt' : ...       #Vector tangente a la superficie en el punto indicado
"""


"""
-------------------------------------------------------------------------------
AUXILIARES
-------------------------------------------------------------------------------
"""
def esSupNivel(res : dict ={}) -> bool:
    """
    Determina si una función es una superficie de nivel
    Argumentos:
    f       función
    x       primera variable
    y       segunda variable
    z       tercera variable
    res     diccionario donde se guardan los resultados intermedios
    """
    res['dx'] = sp.diff(res['sup'], res['x'])
    res['dy'] = sp.diff(res['sup'], res['y'])
    res['dz'] = sp.diff(res['sup'], res['z'])
    try:
        return not sp.solve([sp.Eq(res['sup'], 0), sp.Eq(res['dx'], 0), sp.Eq(res['dy'], 0), sp.Eq(res['dz'], 0)], (res['x'], res['y'], res['z']), set=True)[1]
    except:
        return True

"""
-------------------------------------------------------------------------------
VECTOR NORMAL
-------------------------------------------------------------------------------
"""
def normal(res: dict={}) -> dict:
    """
    Calcula el vector normal a la superficie en un punto genérico.
    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'dx' not in res:
        res['dx'] = sp.simplify(sp.diff(res['sup'], res['x']))

    if 'dy' not in res:
        res['dy'] = sp.simplify(sp.diff(res['sup'], res['y']))

    if 'dz' not in res:
        res['dz'] = sp.simplify(sp.diff(res['sup'], res['z']))

    if 'gradiente' not in res:
        res['gradiente'] = sp.Matrix([res['dx'], res['dy'], res['dz']]).T

    res['normal'] = sp.simplify(res['gradiente'].normalized())
    return res

def normal_pt(res: dict={}) -> dict:
    """
    Calcula el vector normal a la superficie en un punto.
    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    ec_subs = res['sup'].subs({res['x']: res['x0'], res['y']: res['y0'], res['z']: res['z0']})
    if len(ec_subs.free_symbols)==0 and abs(ec_subs) > 0.1:
        raise ValueError('El punto no está en la superficie')
    
    if 'dx' not in res:
        res['dx'] = sp.simplify(sp.diff(res['sup'], res['x']))
    res['dx_pt'] = res['dx'].subs({res['x']: res['x0'], res['y']: res['y0'], res['z']: res['z0']})

    if 'dy' not in res:
        res['dy'] = sp.simplify(sp.diff(res['sup'], res['y']))
    res['dy_pt'] = res['dy'].subs({res['x']: res['x0'], res['y']: res['y0'], res['z']: res['z0']})

    if 'dz' not in res:
        res['dz'] = sp.simplify(sp.diff(res['sup'], res['z']))
    res['dz_pt'] = res['dz'].subs({res['x']: res['x0'], res['y']: res['y0'], res['z']: res['z0']})

    res['gradiente_pt'] = sp.Matrix([res['dx_pt'], res['dy_pt'], res['dz_pt']]).T
    res['normal_pt'] = sp.simplify(res['gradiente_pt'].normalized())
    return res


"""
-------------------------------------------------------------------------------
PLANO TANGENTE
-------------------------------------------------------------------------------
"""
def tangente(res: dict={}) -> dict:
    """
    Calcula el plano tangente a la superficie en un punto genérico.
    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'dx' not in res:
        res['dx'] = sp.simplify(sp.diff(res['sup'], res['x']))

    if 'dy' not in res:
        res['dy'] = sp.simplify(sp.diff(res['sup'], res['y']))

    if 'dz' not in res:
        res['dz'] = sp.simplify(sp.diff(res['sup'], res['z']))

    if 'gradiente' not in res:
        res['gradiente'] = sp.Matrix([res['dx'], res['dy'], res['dz']]).T

    x0, y0, z0 = sp.symbols('x_0 y_0 z_0', real=True)
    gradiente_pt = sp.simplify(res['gradiente'].subs({res['x']: x0, res['y']: y0, res['z']: z0}))
    res['tangente'] = sp.simplify(sp.Eq(gradiente_pt.dot(sp.Matrix([res['x'], res['y'], res['z']])), 
                                        gradiente_pt.dot(sp.Matrix([x0, y0, z0]))))

    return res

def tangente_pt(res: dict={}) -> dict:
    """
    Calcula el vector normal a la superficie en un punto.
    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    ec_subs = res['sup'].subs({res['x']: res['x0'], res['y']: res['y0'], res['z']: res['z0']})
    if len(ec_subs.free_symbols)==0 and abs(ec_subs) > 0.1:
        raise ValueError('El punto no está en la superficie')
    
    if 'dx' not in res:
        res['dx'] = sp.simplify(sp.diff(res['sup'], res['x']))
    res['dx_pt'] = res['dx'].subs({res['x']: res['x0'], res['y']: res['y0'], res['z']: res['z0']})

    if 'dy' not in res:
        res['dy'] = sp.simplify(sp.diff(res['sup'], res['y']))
    res['dy_pt'] = res['dy'].subs({res['x']: res['x0'], res['y']: res['y0'], res['z']: res['z0']})

    if 'dz' not in res:
        res['dz'] = sp.simplify(sp.diff(res['sup'], res['z']))
    res['dz_pt'] = res['dz'].subs({res['x']: res['x0'], res['y']: res['y0'], res['z']: res['z0']})

    res['gradiente_pt'] = sp.Matrix([res['dx_pt'], res['dy_pt'], res['dz_pt']]).T
    res['tangente_pt'] = sp.simplify(sp.Eq(res['gradiente_pt'].dot(sp.Matrix([res['x'], res['y'], res['z']])), 
                                        res['gradiente_pt'].dot(sp.Matrix([res['x0'], res['y0'], res['z0']]))))
    return res


"""
-------------------------------------------------------------------------------
ANÁLISIS COMPLETO
-------------------------------------------------------------------------------
"""

def descripccion(res: dict={}) -> dict:
    """
    Hace un cálculo general de todo lo que pueda
    No se hacen comprobaciones de tipo

    Argumentos:
    
    res          diccionario con todos los res calculados hasta el momento
    """
    normal(res)
    tangente(res)
    return res

def descripccion_pt_uv(res: dict={}) -> dict:
    """
    Hace un cálculo general de todo lo que pueda
    No se hacen comprobaciones de tipo

    Argumentos:
    
    res          diccionario con todos los res calculados hasta el momento
    """
    normal_pt(res)
    tangente_pt(res)
    return res
