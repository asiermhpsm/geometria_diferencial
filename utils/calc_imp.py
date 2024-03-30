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
    'laplaciano' : ...     #Laplaciano de la superficie
    'normal' : ...         #Vector normal a la superficie
    'tangente' : ...       #Vector tangente a la superficie

    'dx_pt' : ...           #Derivada de la superficie con respecto a x en el punto indicado
    'dy_pt' : ...           #Derivada de la superficie con respecto a y en el punto indicado
    'dz_pt' : ...           #Derivada de la superficie con respecto a z en el punto indicado
    'laplaciano_pt' : ...     #Laplaciano de la superficie en el punto indicado
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
        return False if sp.solve([sp.Eq(res['sup'], 0), 
                              sp.Eq(res['dx'], 0), 
                              sp.Eq(res['dy'], 0), 
                              sp.Eq(res['dz'], 0)], (res['x'], res['y'], res['z']), set=True)[1] else True
    except:
        return False

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

    if 'laplaciano' not in res:
        res['laplaciano'] = sp.Matrix([res['dx'], res['dy'], res['dz']])

    x0, y0, z0 = sp.symbols('x_0 y_0 z_0', real=True)
    laplaciano_pt = sp.simplify(res['laplaciano'].subs({res['x']: x0, res['y']: y0, res['z']: z0}))
    res['tangente'] = sp.simplify(sp.Eq(laplaciano_pt.dot(sp.Matrix([res['x'], res['y'], res['z']])), 
                                        laplaciano_pt.dot(sp.Matrix([x0, y0, z0]))))

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

    res['laplaciano_pt'] = sp.Matrix([res['dx_pt'], res['dy_pt'], res['dz_pt']])
    res['tangente_pt'] = sp.simplify(sp.Eq(res['laplaciano_pt'].dot(sp.Matrix([res['x'], res['y'], res['z']])), 
                                        res['laplaciano_pt'].dot(sp.Matrix([res['x0'], res['y0'], res['z0']]))))
    return res


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

    if 'laplaciano' not in res:
        res['laplaciano'] = sp.Matrix([res['dx'], res['dy'], res['dz']])

    #TODO- Revisar si es normalized
    res['normal'] = sp.simplify(res['laplaciano'].normalized())
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

    res['laplaciano_pt'] = sp.Matrix([res['dx_pt'], res['dy_pt'], res['dz_pt']])
    res['normal_pt'] = sp.simplify(res['laplaciano_pt'].normalized())
    return res