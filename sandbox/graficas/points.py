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
    x = float(sp.N(parametrizacion[0].subs([[u, u0],[v,v0]])))
    y = float(sp.N(parametrizacion[1].subs([[u, u0],[v,v0]])))
    z = float(sp.N(parametrizacion[2].subs([[u, u0],[v,v0]])))
    return x, y, z

def xy_to_uv(parametrizacion, u, v, x0, y0):
    """
    Dado un 'x', 'y' consigo su valor u y v de una superficie parametrizada
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    x0                  valor x del punto
    y0                  valor y del punto
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    eq1 = sp.Eq(parametrizacion[0], x0)
    eq2 = sp.Eq(parametrizacion[1], y0)

    soluciones = sp.solve((eq1, eq2), (u, v))
    
    if not soluciones:
        raise('El punto dado no esta en la superficie.')

    return soluciones

def xyz_to_uv(parametrizacion, u, v, x0, y0, z0):
    """
    Dado un x,y,z consigo un valor u y v de una superficie parametrizada
    No se hacen comprobaciones de tipo

    Argumentos:
    parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
    x0                  valor x del punto
    y0                  valor y del punto
    z0                  valor z del punto
    u                   primera variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    v                   segunda variable de parametrizacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    soluciones = xy_to_uv(parametrizacion, u, v, x0, y0)
    if isinstance(soluciones, list):
        for sol in soluciones:
            if float(parametrizacion[2].subs([[u, sol[0]],[v,sol[1]]])) == z0:
                return sol
    elif isinstance(soluciones, dict):
        sol = tuple(valor for clave, valor in soluciones.items())
        if float(parametrizacion[2].subs([[u, sol[0]],[v,sol[1]]])) == z0:
            return sol

    raise('El punto dado no esta en la superficie.')
