import sympy as sp

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

def singularidades(f: sp.Expr, x: sp.Symbol, y: sp.Symbol, intervalX: tuple =None, intervalY: tuple =None) -> set:
    def argumentos(lista: list, exp: sp.Expr):
        for elem in exp.args:
            lista.append(elem)
            argumentos(lista, elem)

    def candidatos_sing(func: sp.Expr, res: set):
        inv = sp.simplify(1/func)
        try:
            soluciones = set(sp.solve(sp.Eq(inv, 0), (x,y)))
        except Exception:
            return
        for sol in soluciones:
            if sol[0].has(sp.I) and sol[1].has(sp.I):
                raise Exception(f'No se ha podido calcular las singularidades de la funcion {f}')
            elif sol[0].has(sp.I):
                if sol[1].is_number:
                    res.add( (sp.re(sol[0]), sol[1]) )
                elif isinstance(sol[1], sp.Symbol):
                    sol_im = sp.solve( sp.Eq(sp.im(sol[0]), 0), sol[1])
                    res.add( ( sol[0].subs({sol[1]: sol_im[0]}), sol[1].subs({sol[1]: sol_im[0]}) ) )
                else:
                    raise Exception(f'No se ha podido calcular las singularidades de la funcion {f}')
            elif sol[1].has(sp.I):
                if sol[0].is_number:
                    res.add( (sol[0], sp.re(sol[1])) )
                elif isinstance(sol[0], sp.Symbol):
                    sol_im = sp.solve( sp.Eq(sp.im(sol[1]), 0), sol[0])
                    res.add( ( sol[0].subs({sol[0]: sol_im[0]}), sol[1].subs({sol[0]: sol_im[0]}) ) )
                else:
                    raise Exception(f'No se ha podido calcular las singularidades de la funcion {f}')
            else:
                res.add(sol)

    res = set()
    funcs = [f]
    argumentos(funcs, f)
    for func in funcs:
        candidatos_sing(func, res)

    #Comprueba que las singularidades estén en el intervalo 
    if intervalX!=None and intervalY!=None:
        intervalX = sp.Interval(intervalX[0], intervalX[1])
        intervalY = sp.Interval(intervalY[0], intervalY[1])
        borrar = []
        for sol in res:
            if sol[0].is_number and sol[1].is_number:
                if not (intervalX.contains(sol[0]) and intervalY.contains(sol[1]) ):
                    borrar.append(sol)
                continue
            elif isinstance(sol[0], sp.Symbol):
                var = sol[0]
                func = sol[1]
                interval_esperado = intervalY
            elif isinstance(sol[1], sp.Symbol):
                var = sol[1]
                func = sol[0]
                interval_esperado = intervalX
            else:
                continue
            dominio_var = intervalX if var==x else intervalY
            interval_img = sp.Interval(sp.minimum(func, var, dominio_var), sp.maximum(func, var, dominio_var))
            if interval_img.intersect(interval_esperado).is_empty:
                borrar.append(sol)
        res.difference_update(borrar)
    return res

def continua(f: sp.Expr, x: sp.Symbol, y: sp.Symbol, intervalX: tuple =None, intervalY: tuple =None) -> bool:
    sings = singularidades(f, x, y, intervalX, intervalY)
    if not sings:
        return True
    for sing in sings:
        if isinstance(sing[0], sp.Symbol):
            val_x = intervalX[0] if intervalX!=None else 1
            val_y = intervalY[0] if intervalY!=None else 1
            sing = (sing[0].subs({sing[0]:val_x}), sing[1].subs({sing[0]:val_x}))
        elif isinstance(sing[1], sp.Symbol):
            val_x = intervalX[0] if intervalX!=None else 1
            val_y = intervalY[0] if intervalY!=None else 1
            sing = (sing[0].subs({sing[1]:val_y}), sing[1].subs({sing[1]:val_y}))
        
        try:
            lim = sp.limit(sp.limit(f, y, sing[1], '+'), x, sing[0], '+')
        except Exception:
            print(f'No se ha podido establecer si la función {f} es continua en {sing}')
            return False
        if lim==sp.oo or -lim==sp.oo:
            return False
        
        try:
            if sp.limit(sp.limit(f, y, sing[1], '+'), x, sing[0], '-')!=lim or sp.limit(sp.limit(f, y, sing[1], '-'), x, sing[0], '+')!=lim or sp.limit(sp.limit(f, y, sing[1], '-'), x, sing[0], '-')!=lim:
                return False
        except Exception:
            print(f'No se ha podido establecer si la función {f} es continua en {sing}')
            return False
        
        if lim.is_number:
            return True
        
        print(f'No se ha podido establecer si la función {f} es continua en {sing}')
        return False
    return True

def claseN(f: sp.Expr, x: sp.Symbol, y: sp.Symbol, n: int, intervalX: tuple =None, intervalY: tuple =None) -> bool:
    if n == 0:
        return continua(f, x, y, intervalX, intervalX)
    elif not continua(f, x, y, intervalX, intervalX):
        return False
    return claseN(sp.diff(f, x), x, y, n-1, intervalX, intervalY) and claseN(sp.diff(f, y), x, y, n-1, intervalX, intervalY)

def esRegular(parametrizacion: sp.Matrix, u: sp.Symbol, v: sp.Symbol, res: dict ={}) -> bool:
    #TODO: ¿no es regular cuando todo es 0 o si algun punto es 0?
    if not all(esClaseInf(f, u, v) for f in parametrizacion):
        return False
    
    if not isinstance(parametrizacion, sp.Matrix):
        parametrizacion = sp.Matrix(parametrizacion)
    if 'duXdv' not in res:
        if 'du' not in res:
            res['du'] = sp.diff(parametrizacion, u)
        if 'dv' not in res:
            res['dv'] = sp.diff(parametrizacion, v)
        res['duXdv'] = res['du'].cross(res['dv'])
    return res['duXdv']!=0
    return False if sp.solve(sp.Eq(res['duXdv'], sp.Matrix([0, 0, 0]))) else True   

def esSupNivel(f: sp.Expr, x: sp.Symbol, y: sp.Symbol, z: sp.Symbol, res : dict ={}) -> bool:
    res['dx'] = sp.diff(f, x)
    res['dy'] = sp.diff(f, y)
    res['dz'] = sp.diff(f, z)
    return False if sp.solve([sp.Eq(f, 0), 
                              sp.Eq(res['dx'], 0), 
                              sp.Eq(res['dy'], 0), 
                              sp.Eq(res['dz'], 0)], (x, y, z)) else True



#TODO: no funciona bien
def esClaseInf(f: sp.Expr, u: sp.Symbol, v: sp.Symbol, intervalU: tuple =None, intervalV: tuple =None):
    #TODO-separa demasiado, por ejemplo sin(x)/x da False por que separa en sin(x) OK y 1/x no OK
    def terminoClaseInf(term):
        return term == 0 or any(isinstance(term, func) for func in 
                                [sp.exp, sp.sin, sp.cos, sp.cosh, sp.sinh, sp.asin, sp.acos, sp.atan, sp.acot, sp.sinh, sp.cosh, sp.sech, sp.asinh])
    
    if not continua(f, u, v, intervalU, intervalV):
        return False
    elif len(f.args)==1:
        if terminoClaseInf(f):
            return True
        else:
            return esClaseInf(sp.diff(f, u), u, v, intervalU, intervalV) and esClaseInf(sp.diff(f, v), u, v, intervalU, intervalV)
    else:
        return all(esClaseInf(term, u, v, intervalU, intervalV) for term in f.args)
