import sympy as sp

def uv_to_xyz(parametrizacion: sp.Matrix, u: sp.Symbol, v: sp.Symbol, u0, v0):
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

def xyz_to_uv(parametrizacion: sp.Matrix, u: sp.Symbol, v: sp.Symbol, x0, y0, z0):
    """
    Dado un x,y,z devuelve su valor u y v de una superficie parametrizada. Se devuelve la primera solucion que se encuentre
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie
    u                   primera variable de parametrizacion
    v                   segunda variable de parametrizacion
    x0                  valor x del punto
    y0                  valor y del punto
    z0                  valor z del punto
    """
    punto = (x0, y0, z0)
    ecuaciones = [sp.Eq(s, p) for s, p in zip(parametrizacion, punto)]
    soluciones = sp.solve(ecuaciones, (u, v))
    if not soluciones:
        raise('El punto dado no esta en la superficie.')
    
    #TODO: devuelvo todas las soluciones o solo una
    if isinstance(soluciones, dict):
        return soluciones[u] ,soluciones[v]
    else:
        return soluciones[0]

def esRegular(parametrizacion: sp.Matrix, u: sp.Symbol, v: sp.Symbol, dom_u=sp.S.Reals, dom_v=sp.S.Reals, res: dict ={}) -> bool:
    """
    Determina si una superficie parametrizada es regular

    Arguementos:
    parametrizacion     parametrizacion de superficie
    u                   primera variable de parametrizacion
    v                   segunda variable de parametrizacion
    dom_u               dominio de u
    dom_v               dominio de v
    res                 diccionario donde se guardan los resultados intermedios
    """
    res['du'] = sp.diff(parametrizacion, u)
    res['dv'] = sp.diff(parametrizacion, v)
    res['duXdv'] = sp.simplify(res['du'].cross(res['dv']))
    res['dom_u'] = dom_u
    res['dom_v'] = dom_v
    #NO SE HA PODIDO ENCONTRAR UNA MANERA PARA DETERMINAR SI UNA FUNCION ES DE CLASE INFINITO

    #Encuentro las posibles soluciones que harían que la superficie no sea regular e itero sobre ellas
    soluciones = sp.solve(sp.Eq(res['duXdv'], sp.Matrix([0, 0, 0])), (u,v), set=True)
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
                    if sol[1].subs({sol[0]: sol_im[0]}) in dom_v and sol[0].subs({sol[0]: sol_im[0]}) in dom_u:
                        return False
            elif sol[1].is_number:
                return not sol[1] in dom_v
        #Si el segundo es un símbolo, entonces busco las soluciones que hagan que solo considere la parte real 
        #de la solución que no es un símbolo y miro si estan en el dominio
        elif isinstance(sol[1], sp.Symbol):
            if sol[0].has(sp.I):
                sols_im = sp.solve( sp.Eq(sp.im(sol[0]), 0), sol[1], set=True)
                for sol_im in sols_im[1]:
                    if sol[0].subs({sol[1]: sol_im[0]}) in dom_u and sol[1].subs({sol[1]: sol_im[0]}) in dom_v:
                        return False
            elif sol[0].is_number:
                return not sol[0] in dom_u
        #Si ambos son números, miro si estan en el dominio
        if sol[0].is_number and sol[1].is_number:
            return sol[0] in dom_u and sol[1] in dom_v
        #Si no es ninguno de los casos anteriores, entonces es demasiado complicado y no se puede determinar si la superficie es regular
        else:
            return False
    return True

def esSupNivel(f: sp.Expr, x: sp.Symbol, y: sp.Symbol, z: sp.Symbol, res : dict ={}) -> bool:
    """
    Determina si una función es una superficie de nivel
    Argumentos:
    f       función
    x       primera variable
    y       segunda variable
    z       tercera variable
    res     diccionario donde se guardan los resultados intermedios
    """
    res['dx'] = sp.diff(f, x)
    res['dy'] = sp.diff(f, y)
    res['dz'] = sp.diff(f, z)
    try:
        return False if sp.solve([sp.Eq(f, 0), 
                              sp.Eq(res['dx'], 0), 
                              sp.Eq(res['dy'], 0), 
                              sp.Eq(res['dz'], 0)], (x, y, z), set=True)[1] else True
    except Exception:
        return False


#TODO- El cono es superficie de nivel?
"""x, y, z = sp.symbols('x y z', real=True)
p,q,r = sp.symbols('p q r', positive=True)
print(esSupNivel((x/p)**2 + (y/q)**2 - (z/r)**2, x, y, z))"""

