import sympy as sp
import numpy as np

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
        print(sp.solve([sp.Eq(f, 0), 
                              sp.Eq(res['dx'], 0), 
                              sp.Eq(res['dy'], 0), 
                              sp.Eq(res['dz'], 0)], (x, y, z), set=True))
        return False if sp.solve([sp.Eq(f, 0), 
                              sp.Eq(res['dx'], 0), 
                              sp.Eq(res['dy'], 0), 
                              sp.Eq(res['dz'], 0)], (x, y, z), set=True)[1] else True
    except Exception:
        return False

def genera_malla_elipse(a, b, num_points: int):
    """
    Genera una malla de elipse con semiejes a y b
    Argumentos:
    a           semieje a
    b           semieje b
    num_points  resolución de la malla
    """
    t = np.linspace(0, 2 * np.pi, num_points)
    r = np.linspace(0, 0.98, num_points)
    T, R = np.meshgrid(t, r)
    X = a * R * np.cos(T)
    Y = b * R * np.sin(T)
    return X, Y

