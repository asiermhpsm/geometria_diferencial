import sympy as sp
from .utils import xyz_to_uv

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

def simplifica_trig(expr, u, dom):
    """
    Simplifica una expresión trigonométrica dado un dominio de una variable. Solo simplifica senos, cosenos y tangentes simples
    Argumentos:
    expr        expresión
    u           variable
    dom         dominio de la variable
    """
    if not isinstance(dom, sp.Interval):
        return expr
    n = sp.Symbol('n', integer=True)

    #Coseno positivo
    sol = sp.solve([
        -sp.pi/2+2*sp.pi*n <= dom.start,
        dom.end <= sp.pi/2+2*sp.pi*n ], n)
    if sol != False:
        aux = sp.symbols('aux', positive=True)
        expr = sp.simplify(sp.simplify(expr.subs(sp.cos(u), aux)).subs(aux, sp.cos(u)))
    #Coseno negativo
    sol = sp.solve([
        sp.pi/2+2*sp.pi*n <= dom.start,
        dom.end <= 3*sp.pi/2+2*sp.pi*n ], n)
    if sol != False:
        aux = sp.symbols('aux', negative=True)
        expr = sp.simplify(sp.simplify(expr.subs(sp.cos(u), aux)).subs(aux, sp.cos(u)))
    #Seno positivo
    sol = sp.solve([
        2*sp.pi*n <= dom.start,
        dom.end <= sp.pi+2*sp.pi*n ], n)
    if sol != False:
        aux = sp.symbols('aux', positive=True)
        expr = sp.simplify(sp.simplify(expr.subs(sp.sin(u), aux)).subs(aux, sp.sin(u)))
    #Seno negativo
    sol = sp.solve([
        sp.pi+2*sp.pi*n <= dom.start,
        dom.end <= 2*sp.pi+2*sp.pi*n ], n)
    if sol != False:
        aux = sp.symbols('aux', negative=True)
        expr = sp.simplify(sp.simplify(expr.subs(sp.sin(u), aux)).subs(aux, sp.sin(u)))
    #Tangente positiva
    sol = sp.solve([
        0+sp.pi*n <= dom.start,
        dom.end <= sp.pi/2+sp.pi*n ], n)
    if sol != False:
        aux = sp.symbols('aux', positive=True)
        expr = sp.simplify(sp.simplify(expr.subs(sp.tan(u), aux)).subs(aux, sp.tan(u)))
    #Tangente negativa
    sol = sp.solve([
        -sp.pi/2+sp.pi*n <= dom.start,
        dom.end <= 0+sp.pi*n ], n)
    if sol != False:
        aux = sp.symbols('aux', negative=True)
        expr = sp.simplify(sp.simplify(expr.subs(sp.tan(u), aux)).subs(aux, sp.tan(u)))

    return expr

def simp_trig_uv(expr, res : dict ={}):
        if isinstance(res['dom_u'], sp.Interval):
            expr = simplifica_trig(expr, res['u'], res['dom_u'])
        if  isinstance(res['dom_v'], sp.Interval):
            expr = simplifica_trig(expr, res['v'], res['dom_v'])
        return expr

def simplifica(f, res : dict ={}) -> sp.Expr:
    """
    Simplifica una expresión simbólica o una matriz simbólica
    Argumentos:
    f       función
    res     diccionario con todos los resultados calculados hasta el momento
    """
    
    if 'cond' in res:
        return sp.simplify(simp_trig_uv(simplifica_cond(f, res['cond']), res))
    elif 'dom_u' in res or 'dom_v' in res:
        return sp.simplify(simp_trig_uv(f, res))
    else:
        return sp.simplify(f)

def esRegular(res: dict) -> bool:
    """
    Determina si una superficie parametrizada es regular

    Arguementos:
    res                 diccionario donde se guardan los resultados intermedios
    """
    res['du'] = simplifica(sp.diff(res['sup'], res['u']), res)
    res['dv'] = simplifica(sp.diff(res['sup'], res['v']), res)
    res['duXdv'] = simplifica(res['du'].cross(res['dv']), res)
    #NO SE HA PODIDO ENCONTRAR UNA MANERA PARA DETERMINAR SI UNA FUNCION ES DE CLASE INFINITO

    #Encuentro las posibles soluciones que harían que la superficie no sea regular e itero sobre ellas
    soluciones = sp.solve(sp.Eq(res['duXdv'], sp.Matrix([0, 0, 0])), (res['u'],res['v']), set=True)
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
            return False
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
            res['du'] = simplifica(sp.diff(res['sup'], res['u']), res)
        if 'dv' not in res:
            res['dv'] = simplifica(sp.diff(res['sup'], res['v']), res)
        res['duXdv'] = simplifica(res['du'].cross(res['dv']), res)
    res['norma'] = simplifica(res['duXdv'].norm(), res)
    res['normal'] = simplifica(res['duXdv'].normalized(), res)
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
                res['du'] = simplifica(sp.diff(res['sup'], res['u']), res)
            res['du_pt'] = simplifica(res['du'].subs({res['u']:res['u0'], res['v']:res['v0']}), res)
        if not 'dv_pt' in res:
            if not 'dv' in res:
                res['dv'] = simplifica(sp.diff(res['sup'], res['v']), res)
            res['dv_pt'] = simplifica(res['dv'].subs({res['u']:res['u0'], res['v']:res['v0']}), res)
        res['duXdv_pt'] = simplifica(res['du_pt'].cross(res['dv_pt']), res)
    res['norma_pt'] = simplifica(res['duXdv_pt'].norm(), res)
    res['normal_pt'] = simplifica(res['duXdv_pt'].normalized(), res)
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
            res['du'] = simplifica(sp.diff(res['sup'], res['u']), res)
        if 'dv' not in res:
            res['dv'] = simplifica(sp.diff(res['sup'], res['v']), res)
        res['duXdv'] = simplifica(res['du'].cross(res['dv']), res)
    x, y, z = sp.symbols('x, y, z')
    res['tangente'] = simplifica(sp.Eq(res['duXdv'].dot(sp.Matrix([x,y,z])), res['duXdv'].dot(res['sup'])), res)
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
                res['du'] = simplifica(sp.diff(res['sup'], res['u']), res)
            res['du_pt'] = simplifica(res['du'].subs({res['u']:res['u0'], res['v']:res['v0']}), res)
        if not 'dv_pt' in res:
            if not 'dv' in res:
                res['dv'] = simplifica(sp.diff(res['sup'], res['v']), res)
            res['dv_pt'] = simplifica(res['dv'].subs({res['u']:res['u0'], res['v']:res['v0']}), res)
        res['duXdv_pt'] = simplifica(res['du_pt'].cross(res['dv_pt']), res)

    x, y, z = sp.symbols('x, y, z', real = True)
    res['tangente_pt'] = simplifica(sp.Eq(res['duXdv_pt'].dot(sp.Matrix([x,y,z])), res['duXdv_pt'].dot(res['sup'].subs({res['u']:res['u0'], res['v']:res['v0']}))), res)
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
        res['du'] = simplifica(sp.diff(res['sup'], res['u']), res)
    if 'dv' not in res:
        res['dv'] = simplifica(sp.diff(res['sup'], res['v']), res)

    res['E'] = simplifica(res['du'].dot(res['du']), res)
    res['F'] = simplifica(res['du'].dot(res['dv']), res)
    res['G'] = simplifica(res['dv'].dot(res['dv']), res)

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
            res['du'] = simplifica(sp.diff(res['sup'], res['u']), res)
        res['du_pt'] = simplifica(res['du'].subs({res['u']:res['u0'], res['v']:res['v0']}), res)
    if not 'dv_pt' in res:
        if not 'dv' in res:
            res['dv'] = simplifica(sp.diff(res['sup'], res['v']), res)
        res['dv_pt'] = simplifica(res['dv'].subs({res['u']:res['u0'], res['v']:res['v0']}), res)

    res['E_pt'] = simplifica(res['du_pt'].dot(res['du_pt']), res)
    res['F_pt'] = simplifica(res['du_pt'].dot(res['dv_pt']), res)
    res['G_pt'] = simplifica(res['dv_pt'].dot(res['dv_pt']), res)

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
        res['du'] = simplifica(sp.diff(res['sup'], res['u']), res)
    if 'dv' not in res:
        res['dv'] = simplifica(sp.diff(res['sup'], res['v']), res)
    if 'duu' not in res:
        res['duu'] = simplifica(sp.diff(res['du'], res['u']), res)
    if 'duv' not in res:
        res['duv'] = simplifica(sp.diff(res['du'], res['v']), res)
    if 'dvv' not in res:
        res['dvv'] = simplifica(sp.diff( res['dv'], res['v']), res)
    if 'normal' not in res:
        normal(res)

    res['e'] = simplifica( res['normal'].dot(res['duu']), res)
    res['f'] = simplifica( res['normal'].dot(res['duv']), res)
    res['g'] = simplifica( res['normal'].dot(res['dvv']), res)
    
    return res

def segundaFormaFundamental_pt_uv(res : dict ={}) -> dict:
    """
    Retorna en forma de Matrix(e, f, g) la segunda forma fundamental en un punto  descrito por u, v
    No se hacen comprobaciones de tipo

    Argumentos:
    res          diccionario con todos los resultados calculados hasta el momento
    """
    if 'du' not in res:
        res['du'] = simplifica(sp.diff(res['sup'], res['u']), res)
    if 'dv' not in res:
        res['dv'] = simplifica(sp.diff(res['sup'], res['v']), res)
    if 'duu_pt' not in res:
        if 'duu' not in res:
            res['duu'] = simplifica(sp.diff(res['du'], res['u']), res)
        res['duu_pt'] = simplifica(res['duu'].subs({res['u']:res['u0'], res['v']:res['v0']}), res)
    if 'duv_pt' not in res:
        if 'duv' not in res:
            res['duv'] = simplifica(sp.diff(res['du'], res['v']), res)
        res['duv_pt'] = simplifica(res['duv'].subs({res['u']:res['u0'], res['v']:res['v0']}), res)
    if 'dvv_pt' not in res:
        if 'dvv' not in res:
            res['dvv'] = simplifica(sp.diff(res['dv'], res['v']), res)
        res['dvv_pt'] = simplifica(res['dvv'].subs({res['u']:res['u0'], res['v']:res['v0']}), res)
    if 'normal_pt' not in res:
        normal_pt_uv(res)

    res['e_pt'] = simplifica( res['normal_pt'].dot(res['duu_pt']), res)
    res['f_pt'] = simplifica( res['normal_pt'].dot(res['duv_pt']), res)
    res['g_pt'] = simplifica( res['normal_pt'].dot(res['dvv_pt']), res)
    
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
    res['K'] = simplifica((res['e']*res['g'] - res['f']**2)/(res['E']*res['G'] - res['F']**2), res)
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

    res['K_pt'] = simplifica((res['e_pt']*res['g_pt'] - res['f_pt']**2)/(res['E_pt']*res['G_pt'] - res['F_pt']**2), res)
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
    res['H'] = simplifica((res['e']*res['G'] + res['g']*res['E'] - 2*res['f']*res['F'])
                                  /(2*(res['E']*res['G'] - res['F']**2)), res)
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
    
    res['H_pt'] = simplifica((res['e_pt']*res['G_pt'] + res['g_pt']*res['E_pt'] - 2*res['f_pt']*res['F_pt'])
                                     /(2*(res['E_pt']*res['G_pt'] - res['F_pt']**2)), res)
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
    raiz = simplifica(sp.sqrt(res['H']**2 - res['K']), res)
    res['k1'] = simplifica(res['H'] + raiz, res)
    res['k2'] = simplifica(res['H'] - raiz, res)
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
    raiz = simplifica(sp.sqrt(res['H_pt']**2 - res['K_pt']), res)
    res['k1_pt'] = simplifica(res['H_pt'] + raiz, res)
    res['k2_pt'] = simplifica(res['H_pt'] - raiz, res)
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
            if simplifica(res['k1_pt']-res['k2_pt']) == 0:
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

    denom = simplifica(res['E']*res['G'] - res['F']**2, res)
    res['W'] = simplifica(sp.Matrix([[res['e']*res['G']-res['f']*res['F'], 
                    res['f']*res['G']-res['g']*res['F']], 
                    [res['f']*res['E']-res['e']*res['F'], 
                    res['g']*res['E']-res['f']*res['F']]])/denom, res)
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

    denom = simplifica(res['E_pt']*res['G_pt'] - res['F_pt']**2, res)
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
        res['coord_d1'] = autovalores[0][-1][0]
        res['coord_d2'] = autovalores[0][-1][1]
    elif autovalores[0][1] == 1:
        res['k1'] = autovalores[0][0]
        res['k2'] = autovalores[1][0]
        res['coord_d1'] = autovalores[0][-1][0]
        res['coord_d2'] = autovalores[1][-1][0]
    else:
        raise Exception("No se ha podido calcular los autovectores")

    res['d1'] = simplifica(res['coord_d1'][0]*res['du'] + res['coord_d1'][1]*res['dv'], res)
    res['d2'] = simplifica(res['coord_d2'][0]*res['du'] + res['coord_d2'][1]*res['dv'], res)
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
        pos_k1 = 0 if autovalores[0][0] >= autovalores[1][0] else 1
        pos_k2 = 1 if pos_k1 == 0 else 0
        res['k1_pt'] = autovalores[pos_k1][0]
        res['k2_pt'] = autovalores[pos_k2][0]
        res['coord_d1_pt'] = autovalores[pos_k1][-1][0]
        res['coord_d2_pt'] = autovalores[pos_k2][-1][0]
    else:
        raise Exception("No se ha podido calcular los autovectores")
    
    res['d1_pt'] = simplifica(res['coord_d1_pt'][0]*res['du_pt'] + res['coord_d1_pt'][1]*res['dv_pt'], res)
    res['d2_pt'] = simplifica(res['coord_d2_pt'][0]*res['du_pt'] + res['coord_d2_pt'][1]*res['dv_pt'], res)
    return res

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
    denom = simplifica(res['E']*res['G'] - res['F']**2, res)
    W = simplifica(sp.Matrix([[res['e']*res['G']-res['f']*res['F'], 
                    res['f']*res['G']-res['g']*res['F']], 
                    [res['f']*res['E']-res['e']*res['F'], 
                    res['g']*res['E']-res['f']*res['F']]])/denom, res)
    res['W'] = sp.simplify(W)
    autovalores = W.eigenvects(simplify=True)

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
    
    res['d1'] = simplifica(res['coord_d1'][0]*res['du'] + res['coord_d1'][1]*res['dv'], res)
    res['d2'] = simplifica(res['coord_d2'][0]*res['du'] + res['coord_d2'][1]*res['dv'], res)
    umbilico(res)
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
        pos_k1 = 0 if autovalores[0][0] >= autovalores[1][0] else 1
        pos_k2 = 1 if pos_k1 == 0 else 0
        res['k1_pt'] = autovalores[pos_k1][0]
        res['k2_pt'] = autovalores[pos_k2][0]
        res['coord_d1_pt'] = autovalores[pos_k1][-1][0]
        res['coord_d2_pt'] = autovalores[pos_k2][-1][0]
    else:
        raise Exception("No se ha podido calcular los autovectores")
    res['d1_pt'] = simplifica(res['coord_d1_pt'][0]*res['du_pt'] + res['coord_d1_pt'][1]*res['dv_pt'], res)
    res['d2_pt'] = simplifica(res['coord_d2_pt'][0]*res['du_pt'] + res['coord_d2_pt'][1]*res['dv_pt'], res)
    clasicPt_uv(res)
    umbilico_pt_uv(res)
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