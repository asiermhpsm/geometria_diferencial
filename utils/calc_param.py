import sympy as sp

"""
Todos los calculos se guardarán en un diccionario de resultados para evitar cálculos repetidos y para centralizar la información.
LEYENDA DE ALMACENAMIENTO DE RESULTADOS: no tiene porque estar todos los resultados, solo los que se han calculado.
Lo que se puede asumir que esta siempre es sup, u, v, dom_u, dom_v
res = {
    'sup' : ...            #Parametrización de la superficie. Debe ser de tipo sympy.Matrx()
    'u' : ...              #Primera variable de dependencia. Debe ser de tipo sp.Symbol
    'v' : ...              #Segunda variable de dependencia. Debe ser de tipo sp.Symbol
    'cond' : ...           #Condicion de u y v que hacen que una operación sea negativa estricta. Por ejemplo si u^2+v^2<1 entonces poner u**2+v**2-1
    'dom_u' : ...          #Dominio de u
    'dom_v' : ...          #Dominio de v
    'u0' : ...             #Valor de u en un punto
    'v0' : ...             #Valor de v en un punto
    'x0' : ...             #Valor de x en un punto
    'y0' : ...             #Valor de y en un punto
    'z0' : ...             #Valor de z en un punto
    
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
    'coord_d1'             #coordenadas de direccion principal 1 respecto a dervadas parciales
    'coord_d2'             #coordenadas de direccion principal 2 respecto a dervadas parciales
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
    'coord_d1_pt'             #coordenadas de direccion principal 1 respecto a dervadas parciales
    'coord_d2_pt'             #coordenadas de direccion principal 2 respecto a dervadas parciales
    'W_pt'                    #Matriz de Weingarten
}
"""

"""
-------------------------------------------------------------------------------
AUXILIARES
-------------------------------------------------------------------------------
"""
def simplifica_cond(f, cond: sp.Expr) -> sp.Expr:
    """
    Simplifica f sabiendo que se cumple la condición cond
    Argumentos:
    f       función
    cond    condición de la forma menor que: ... < ...
    """
    aux_neg = sp.symbols('aux_neg', negative=True)
    sust = sp.simplify(f.subs(cond.lhs - cond.rhs, aux_neg).subs(cond.lhs, aux_neg + cond.rhs))
    return sp.simplify(sust.subs(aux_neg, cond.lhs - cond.rhs))

def simplifica_resultados_cond(res : dict) -> dict:
    """
    Simplifica todos los resultados sabiendo que se cumple la condición cond
    Argumentos:
    res     diccionario con todos los resultados calculados hasta el momento
    """
    for k, v in res.items():
        if k!='cond':
            try:
                res[k] = simplifica_cond(v, res['cond'])
            except: pass

def simplifica_resultados_trig(res):
    """
    Aplica la simplificación trignometrica a los resultados obtenidos
    """
    if 'dom_u' in res and isinstance(res['dom_u'], sp.Interval):
        simplifica_trig(res, res['u'], res['dom_u'])
    if 'dom_v' in res and isinstance(res['dom_v'], sp.Interval):
        simplifica_trig(res, res['v'], res['dom_v'])

def simplifica_trig(res, x, dom) -> dict:
    """
    Dada una variable, simplifica trigonométricamente los resultados obtenidos
    """
    n = sp.Symbol('n', integer=True)
    pos = sp.symbols('pos', positive=True)
    neg = sp.symbols('neg', negative=True)

    #Coseno positivo
    sol = sp.solve([
        -sp.pi/2+2*sp.pi*n <= dom.start,
        dom.end <= sp.pi/2+2*sp.pi*n ], n)
    if sol != False:
        for k, v in res.items():
            try:
                res[k] = sp.simplify(sp.simplify(v.subs(sp.cos(x), pos)).subs(pos, sp.cos(x)))
            except:
                pass
    #Coseno negativo
    sol = sp.solve([
        sp.pi/2+2*sp.pi*n <= dom.start,
        dom.end <= 3*sp.pi/2+2*sp.pi*n ], n)
    if sol != False:
        for k, v in res.items():
            try:
                res[k] = sp.simplify(sp.simplify(v.subs(sp.cos(x), neg)).subs(neg, sp.cos(x)))
            except:
                pass
    #Seno positivo
    sol = sp.solve([
        0+2*sp.pi*n <= dom.start,
        dom.end <= sp.pi+2*sp.pi*n ], n)
    if sol != False:
        for k, v in res.items():
            try:
                res[k] = sp.simplify(sp.simplify(v.subs(sp.sin(x), pos)).subs(pos, sp.sin(x)))
            except:
                pass
    #Seno negativo
    sol = sp.solve([
        sp.pi+2*sp.pi*n <= dom.start,
        dom.end <= 2*sp.pi+2*sp.pi*n ], n)
    if sol != False:
        for k, v in res.items():
            try:
                res[k] = sp.simplify(sp.simplify(v.subs(sp.sin(x), neg)).subs(neg, sp.sin(x)))
            except:
                pass
    #Tangente positiva
    sol = sp.solve([
        -sp.pi/2+2*sp.pi*n <= dom.start,
        dom.end <= sp.pi/2+2*sp.pi*n ], n)
    if sol != False:
        for k, v in res.items():
            try:
                res[k] = sp.simplify(sp.simplify(v.subs(sp.tan(x), pos)).subs(pos, sp.tan(x)))
            except:
                pass
    #Tangente negativa
    sol = sp.solve([
        sp.pi/2+2*sp.pi*n <= dom.start,
        dom.end <= 3*sp.pi/2+2*sp.pi*n ], n)
    if sol != False:
        for k, v in res.items():
            try:
                res[k] = sp.simplify(sp.simplify(v.subs(sp.tan(x), neg)).subs(neg, sp.tan(x)))
            except:
                pass
    return res


def esRegular(res: dict) -> bool:
    """
    Determina si una superficie parametrizada es regular

    Arguementos:
    res                 diccionario donde se guardan los resultados intermedios
    """
    res['du'] = sp.simplify(sp.diff(res['sup'], res['u']))
    res['dv'] = sp.simplify(sp.diff(res['sup'], res['v']))
    res['duXdv'] = sp.simplify(res['du'].cross(res['dv']))
    #NO SE HA PODIDO ENCONTRAR UNA MANERA PARA DETERMINAR SI UNA FUNCION ES DE CLASE INFINITO

    #Se intentan buscar valores que hagan que la superficie no sea regular, 
    #si salta una excepción, es demasiado complejo y se asume regular
    try:
        #Encuentro las posibles soluciones que harían que la superficie no sea regular e itero sobre ellas
        soluciones = sp.solve(sp.Eq(res['duXdv'], sp.Matrix([0, 0, 0]).T), (res['u'],res['v']), set=True)
        for sol in soluciones[1]:
            #Si la solucion son ambos símbolos, entonces estan en el dominio y la superficie no es regular
            if isinstance(sol[0], sp.Symbol) and isinstance(sol[1], sp.Symbol):
                return False
            #Si el primero es un símbolo, entonces busco las soluciones que hagan que solo considere la parte real 
            #de la solución que no es un símbolo y miro si estan en el dominio
            elif isinstance(sol[0], sp.Symbol):
                if sol[1].has(sp.I):
                    sols_im = sp.solve( sp.Eq(sp.im(sol[1]), 0), sol[0], set=True)
                    for sol_im in sols_im[1]:
                        if sol[1].subs({sol[0]: sol_im[0]}) in res['dom_v'] and sol[0].subs({sol[0]: sol_im[0]}) in res['dom_u']:
                            return False
                elif sol[1].is_number:
                    return not sol[1] in res['dom_v']
            #Si el segundo es un símbolo, entonces busco las soluciones que hagan que solo considere la parte real 
            #de la solución que no es un símbolo y miro si estan en el dominio
            elif isinstance(sol[1], sp.Symbol):
                if sol[0].has(sp.I):
                    sols_im = sp.solve( sp.Eq(sp.im(sol[0]), 0), sol[1], set=True)
                    for sol_im in sols_im[1]:
                        if sol[0].subs({sol[1]: sol_im[0]}) in res['dom_u'] and sol[1].subs({sol[1]: sol_im[0]}) in res['dom_v']:
                            return False
                elif sol[0].is_number:
                    return not sol[0] in res['dom_u']
            #Si ambos son números, miro si estan en el dominio
            elif sol[0].is_number and sol[1].is_number:
                return sol[0] in res['dom_u'] and sol[1] in res['dom_v']
            #Si no es ninguno de los casos anteriores, entonces es demasiado complicado y no se puede determinar si la superficie es regular
            else:
                return True
    except:
        return True
    return True


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
            res['du'] = sp.simplify(sp.diff(res['sup'], res['u']))
        if 'dv' not in res:
            res['dv'] = sp.simplify(sp.diff(res['sup'], res['v']))
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
                res['du'] = sp.simplify(sp.diff(res['sup'], res['u']))
            res['du_pt'] = sp.simplify(res['du'].subs({res['u']:res['u0'], res['v']:res['v0']}))
        if not 'dv_pt' in res:
            if not 'dv' in res:
                res['dv'] = sp.simplify(sp.diff(res['sup'], res['v']), res)
            res['dv_pt'] = sp.simplify(res['dv'].subs({res['u']:res['u0'], res['v']:res['v0']}))
        res['duXdv_pt'] = sp.simplify(res['du_pt'].cross(res['dv_pt']))
    res['norma_pt'] = sp.simplify(res['duXdv_pt'].norm())
    res['normal_pt'] = sp.simplify(res['duXdv_pt'].normalized())
    return res

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
            res['du'] = sp.simplify(sp.diff(res['sup'], res['u']))
        if 'dv' not in res:
            res['dv'] = sp.simplify(sp.diff(res['sup'], res['v']))
        res['duXdv'] = sp.simplify(res['du'].cross(res['dv']))
    x, y, z = sp.symbols('x, y, z')
    res['tangente'] = sp.simplify(sp.Eq(res['duXdv'].dot(sp.Matrix([x,y,z])), res['duXdv'].dot(res['sup'])))
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
                res['du'] = sp.simplify(sp.diff(res['sup'], res['u']))
            res['du_pt'] = sp.simplify(res['du'].subs({res['u']:res['u0'], res['v']:res['v0']}))
        if not 'dv_pt' in res:
            if not 'dv' in res:
                res['dv'] = sp.simplify(sp.diff(res['sup'], res['v']))
            res['dv_pt'] = sp.simplify(res['dv'].subs({res['u']:res['u0'], res['v']:res['v0']}))
        res['duXdv_pt'] = sp.simplify(res['du_pt'].cross(res['dv_pt']))

    x, y, z = sp.symbols('x, y, z', real = True)
    res['tangente_pt'] = sp.simplify(sp.Eq(res['duXdv_pt'].dot(sp.Matrix([x,y,z])), res['duXdv_pt'].dot(res['sup'].subs({res['u']:res['u0'], res['v']:res['v0']}))))
    return res

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
        res['du'] = sp.simplify(sp.diff(res['sup'], res['u']))
    if 'dv' not in res:
        res['dv'] = sp.simplify(sp.diff(res['sup'], res['v']))

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
            res['du'] = sp.simplify(sp.diff(res['sup'], res['u']))
        res['du_pt'] = sp.simplify(res['du'].subs({res['u']:res['u0'], res['v']:res['v0']}))
    if not 'dv_pt' in res:
        if not 'dv' in res:
            res['dv'] = sp.simplify(sp.diff(res['sup'], res['v']))
        res['dv_pt'] = sp.simplify(res['dv'].subs({res['u']:res['u0'], res['v']:res['v0']}))

    if not 'duXdv_pt' in res:
        res['duXdv_pt'] = sp.simplify(res['du_pt'].cross(res['dv_pt']))

    res['E_pt'] = sp.simplify(res['du_pt'].dot(res['du_pt']))
    res['F_pt'] = sp.simplify(res['du_pt'].dot(res['dv_pt']))
    res['G_pt'] = sp.simplify(res['dv_pt'].dot(res['dv_pt']))

    return res

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
        res['du'] = sp.simplify(sp.diff(res['sup'], res['u']))
    if 'dv' not in res:
        res['dv'] = sp.simplify(sp.diff(res['sup'], res['v']))
    if 'duu' not in res:
        res['duu'] = sp.simplify(sp.diff(res['du'], res['u']))
    if 'duv' not in res:
        res['duv'] = sp.simplify(sp.diff(res['du'], res['v']))
    if 'dvv' not in res:
        res['dvv'] = sp.simplify(sp.diff( res['dv'], res['v']))
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
        res['du'] = sp.simplify(sp.diff(res['sup'], res['u']))
    if 'dv' not in res:
        res['dv'] = sp.simplify(sp.diff(res['sup'], res['v']))
    if 'duu_pt' not in res:
        if 'duu' not in res:
            res['duu'] = sp.simplify(sp.diff(res['du'], res['u']))
        res['duu_pt'] = sp.simplify(res['duu'].subs({res['u']:res['u0'], res['v']:res['v0']}))
    if 'duv_pt' not in res:
        if 'duv' not in res:
            res['duv'] = sp.simplify(sp.diff(res['du'], res['v']))
        res['duv_pt'] = sp.simplify(res['duv'].subs({res['u']:res['u0'], res['v']:res['v0']}))
    if 'dvv_pt' not in res:
        if 'dvv' not in res:
            res['dvv'] = sp.simplify(sp.diff(res['dv'], res['v']))
        res['dvv_pt'] = sp.simplify(res['dvv'].subs({res['u']:res['u0'], res['v']:res['v0']}))
    if 'normal_pt' not in res:
        normal_pt_uv(res)

    res['e_pt'] = sp.simplify( res['normal_pt'].dot(res['duu_pt']))
    res['f_pt'] = sp.simplify( res['normal_pt'].dot(res['duv_pt']))
    res['g_pt'] = sp.simplify( res['normal_pt'].dot(res['dvv_pt']))
    
    return res

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
            if res['k1_pt'] == res['k2_pt']:
                res['clasif_pt'] = 'Planar'
            else:
                res['clasif_pt'] = 'Parabólico'
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

    denom = sp.simplify(res['E']*res['G'] - res['F']**2)
    res['W'] = sp.simplify(sp.Matrix([[res['e']*res['G']-res['f']*res['F'], 
                    res['f']*res['G']-res['g']*res['F']], 
                    [res['f']*res['E']-res['e']*res['F'], 
                    res['g']*res['E']-res['f']*res['F']]])/denom)
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

    denom = sp.simplify(res['E_pt']*res['G_pt'] - res['F_pt']**2)
    res['W_pt'] = sp.Matrix([[res['e_pt']*res['G_pt']-res['f_pt']*res['F_pt'], 
                    res['f_pt']*res['G_pt']-res['g_pt']*res['F_pt']], 
                    [res['f_pt']*res['E_pt']-res['e_pt']*res['F_pt'], 
                    res['g_pt']*res['E_pt']-res['f_pt']*res['F_pt']]])/denom
    return res

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
        res['coord_d1'] = autovalores[0][-1][0]
        res['coord_d2'] = autovalores[0][-1][1]
    elif autovalores[0][1] == 1:
        res['k1'] = autovalores[0][0]
        res['k2'] = autovalores[1][0]
        res['coord_d1'] = autovalores[0][-1][0]
        res['coord_d2'] = autovalores[1][-1][0]
    else:
        raise Exception("No se ha podido calcular los autovectores")

    res['d1'] = sp.simplify(res['coord_d1'][0]*res['du'] + res['coord_d1'][1]*res['dv'])
    res['d2'] = sp.simplify(res['coord_d2'][0]*res['du'] + res['coord_d2'][1]*res['dv'])
    return res
    
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
        res['k1_pt'] = autovalores[0][0]
        res['k2_pt'] = autovalores[0][0]
        res['coord_d1_pt'] = autovalores[0][-1][0]
        res['coord_d2_pt'] = autovalores[0][-1][1]
    elif autovalores[0][1] == 1:
        try:
            autovalores = sorted(autovalores, key=lambda x: x[0], reverse=True)
        except:
            pass
        res['k1_pt'] = autovalores[0][0]
        res['k2_pt'] = autovalores[1][0]
        res['coord_d1_pt'] = autovalores[0][-1][0]
        res['coord_d2_pt'] = autovalores[1][-1][0]
    else:
        raise Exception("No se ha podido calcular los autovectores")
    
    res['d1_pt'] = sp.simplify(res['coord_d1_pt'][0]*res['du_pt'] + res['coord_d1_pt'][1]*res['dv_pt'])
    res['d2_pt'] = sp.simplify(res['coord_d2_pt'][0]*res['du_pt'] + res['coord_d2_pt'][1]*res['dv_pt'])
    return res

"""
-------------------------------------------------------------------------------
PUNTOS UMBÍLICOS
-------------------------------------------------------------------------------
"""
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

"""
-------------------------------------------------------------------------------
DIRECCIONES ASINTÓTICAS
-------------------------------------------------------------------------------
"""
def dirAsin_pt_uv(res):
    """
    Calcula las direcciones asintóticas en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'e_pt' not in res:
        segundaFormaFundamental_pt_uv(res)

    if res['e_pt']==0 and res['f_pt']==0 and res['g_pt']==0:
        w1, w2 = sp.symbols('w_1, w_2', real=True)
        res['Dirs_asint'] = [sp.Matrix([w1, w2]).T]
    elif res['e_pt']==0:
        if res['f_pt'] == 0: res['Dirs_asint'] = [sp.Matrix([1, 0]).T]
        else: res['Dirs_asint'] = [sp.Matrix([1, 0]).T, sp.Matrix([-res['g_pt'], 2*res['f_pt']]).T]
    elif res['g_pt']==0:
        if res['f_pt'] == 0: res['Dirs_asint'] = [sp.Matrix([0, 1]).T]
        else: res['Dirs_asint'] = [sp.Matrix([0, 1]).T, sp.Matrix([-2*res['f_pt'], -res['e_pt'], ]).T]
    elif res['f_pt']**2- res['g_pt']*res['e_pt'] < 0:
        res['Dirs_asint'] = []
    else:
        raiz = sp.sqrt(res['f_pt']**2- res['g_pt']*res['e_pt'])
        res['Dirs_asint'] = [sp.Matrix([res['g_pt'], -res['f_pt']+raiz]).T, sp.Matrix([res['g_pt'], -res['f_pt']-raiz]).T]
        if res['Dirs_asint'][0] == res['Dirs_asint'][1]: del res['Dirs_asint'][1]
    return res

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
    denom = sp.simplify(res['E']*res['G'] - res['F']**2)
    res['W'] = sp.simplify(sp.Matrix([[res['e']*res['G']-res['f']*res['F'], 
                    res['f']*res['G']-res['g']*res['F']], 
                    [res['f']*res['E']-res['e']*res['F'], 
                    res['g']*res['E']-res['f']*res['F']]])/denom)

    autovalores = res['W'].eigenvects(simplify=True)

    if autovalores[0][1] == 2:
        res['k1'] = autovalores[0][0]
        res['k2'] = autovalores[0][0]
        res['coord_d1'] = autovalores[0][-1][0]
        res['coord_d2'] = autovalores[0][-1][1]
    elif autovalores[0][1] == 1:
        res['k1'] = autovalores[0][0]
        res['k2'] = autovalores[1][0]
        res['coord_d1'] = autovalores[0][-1][0]
        res['coord_d2'] = autovalores[1][-1][0]
    else:
        raise Exception("No se ha podido calcular los autovectores")
    
    res['d1'] = sp.simplify(res['coord_d1'][0]*res['du'] + res['coord_d1'][1]*res['dv'])
    res['d2'] = sp.simplify(res['coord_d2'][0]*res['du'] + res['coord_d2'][1]*res['dv'])
    return res

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
        res['coord_d1_pt'] = autovalores[0][-1][0]
        res['coord_d2_pt'] = autovalores[0][-1][1]
    elif autovalores[0][1] == 1:
        try:
            autovalores = sorted(autovalores, key=lambda x: x[0], reverse=True)
        except:
            pass
        res['k1_pt'] = autovalores[0][0]
        res['k2_pt'] = autovalores[1][0]
        res['coord_d1_pt'] = autovalores[0][-1][0]
        res['coord_d2_pt'] = autovalores[1][-1][0]
    else:
        raise Exception("No se ha podido calcular los autovectores")
    res['d1_pt'] = sp.simplify(res['coord_d1_pt'][0]*res['du_pt'] + res['coord_d1_pt'][1]*res['dv_pt'])
    res['d2_pt'] = sp.simplify(res['coord_d2_pt'][0]*res['du_pt'] + res['coord_d2_pt'][1]*res['dv_pt'])
    clasicPt_uv(res)
    umbilico_pt_uv(res)
    dirAsin_pt_uv(res)
    return res