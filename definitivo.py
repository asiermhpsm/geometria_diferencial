import numpy as np
import sympy as sp

u, v = sp.symbols('u, v', real = True)
ecuaciones1 = [sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v), sp.sin(v)]
ecuaciones2 = [u+2*v, u+v, v-u]

def normal(ecuaciones, u, v):
    """
    Retorna la primera forma fundamental en forma de matriz de funciones 
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      lista de longitud 3 de funciones
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    
    """
    du_ecuaciones = [sp.diff(ecuaciones[i], u) for i in range(3)]
    dv_ecuaciones = [sp.diff(ecuaciones[i], v) for i in range(3)]
    return sp.Matrix(sp.Matrix(du_ecuaciones).cross(sp.Matrix(dv_ecuaciones))).normalized()

def primeraFormaFundamental(ecuaciones, u, v):
    """
    Retorna la primera forma fundamental en forma de (E, F, G)
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      lista de longitud 3 de funciones
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    
    """
    du_ecuaciones = [sp.diff(ecuaciones[i], u) for i in range(3)]
    dv_ecuaciones = [sp.diff(ecuaciones[i], v) for i in range(3)]

    E=sp.Matrix(du_ecuaciones).dot(sp.Matrix(du_ecuaciones))
    F=sp.Matrix(du_ecuaciones).dot(sp.Matrix(dv_ecuaciones))
    G=sp.Matrix(dv_ecuaciones).dot(sp.Matrix(dv_ecuaciones))

    return E, F, G

def segundoFormaFundamental(ecuaciones, u, v):
    """
    Retorna la segunda forma fundamental en forma de (e, f, g)
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      lista de longitud 3 de funciones
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    
    """
    du_ecuaciones = [sp.diff(ecuaciones[i], u) for i in range(3)]
    dv_ecuaciones = [sp.diff(ecuaciones[i], v) for i in range(3)]
    duu_ecuaciones = [sp.diff(du_ecuaciones[i], u) for i in range(3)]
    duv_ecuaciones = [sp.diff(du_ecuaciones[i], v) for i in range(3)]
    dvv_ecuaciones = [sp.diff(du_ecuaciones[i], v) for i in range(3)]

    e = sp.det(sp.Matrix([du_ecuaciones, dv_ecuaciones, duu_ecuaciones]).T) / (sp.Matrix(du_ecuaciones).cross(sp.Matrix(dv_ecuaciones))).norm()
    f = sp.det(sp.Matrix([du_ecuaciones, dv_ecuaciones, duv_ecuaciones]).T) / (sp.Matrix(du_ecuaciones).cross(sp.Matrix(dv_ecuaciones))).norm()
    g = sp.det(sp.Matrix([du_ecuaciones, dv_ecuaciones, dvv_ecuaciones]).T) / (sp.Matrix(du_ecuaciones).cross(sp.Matrix(dv_ecuaciones))).norm()
    
    return e, f, g

def curvaturaGauss(ecuaciones, u, v):
    """
    Retorna la curvatura de Gauss
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      lista de longitud 3 de funciones
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    
    """
    E, F, G = primeraFormaFundamental(ecuaciones, u, v)
    e, f, g = segundoFormaFundamental(ecuaciones, u, v)
    return sp.simplify((e*f - f**2) / (E*G - F**2))

def curvaturaMedia(ecuaciones, u, v):
    """
    Retorna la curvatura media
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      lista de longitud 3 de funciones
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    
    """
    E, F, G = primeraFormaFundamental(ecuaciones, u, v)
    e, f, g = segundoFormaFundamental(ecuaciones, u, v)
    return sp.simplify((e*G + g*E - 2*f*F) / (2*(E*G - F**2)))

def curvaturasPrincipales(ecuaciones, u, v):
    """
    Retorna las curvaturas principales como tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      lista de longitud 3 de funciones
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    
    """
    K = curvaturaGauss(ecuaciones, u, v)
    H = curvaturaMedia(ecuaciones, u, v)
    raiz = sp.sqrt(H**2 - K)
    return sp.simplify(H + raiz), sp.simplify(H - raiz)

def clasifPt(ecuaciones, u, v, u0, v0):
    """
    Imprime la clasificacion de una superficie en un punto descrito con u y v
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      lista de longitud 3 de funciones
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0              valor u del punto
    v0              valor v del punto
    """
    K = curvaturaGauss(ecuaciones, u, v)
    K0 = sp.N(K.subs([[u, u0],[v,v0]]))
    if K0 > 0:
        print('Eliptico')
    elif K0 < 0:
        print('Hiperbólitco')
    elif K0 == 0:
        print('Parabólico o planar')

clasifPt(ecuaciones1, u, v, 0, 0)