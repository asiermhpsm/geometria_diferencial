import sympy as sp


def normal(ecuaciones, u, v):
    """
    Retorna el vector normal de una superficie
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    du_ecuaciones = [sp.diff(ecuaciones[i], u) for i in range(3)]
    dv_ecuaciones = [sp.diff(ecuaciones[i], v) for i in range(3)]
    res = sp.simplify( sp.Matrix(sp.Matrix(du_ecuaciones).cross(sp.Matrix(dv_ecuaciones))).normalized() )
    return [elem for elem in res]

def normal_pt(ecuaciones, u, v, u0, v0):
    """
    Retorna el vector normal de una superficie en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0              valor u del punto
    v0              valor v del punto
    """
    du_ecuaciones = [sp.diff(ecuaciones[i], u) for i in range(3)]
    dv_ecuaciones = [sp.diff(ecuaciones[i], v) for i in range(3)]

    du_ecuaciones_pt = [sp.N(du_ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_ecuaciones_pt = [sp.N(dv_ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    du_ecuaciones_X_dv_ecuaciones_pt = sp.Matrix(sp.Matrix(du_ecuaciones_pt).cross(sp.Matrix(dv_ecuaciones_pt))).normalized()

    return [elem for elem in sp.Matrix(du_ecuaciones_X_dv_ecuaciones_pt)]

def primeraFormaFundamental(ecuaciones, u, v):
    """
    Retorna la primera forma fundamental en forma de (E, F, G)
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    du_ecuaciones = [sp.diff(ecuaciones[i], u) for i in range(3)]
    dv_ecuaciones = [sp.diff(ecuaciones[i], v) for i in range(3)]

    E=sp.simplify(sp.Matrix(du_ecuaciones).dot(sp.Matrix(du_ecuaciones)))
    F=sp.simplify(sp.Matrix(du_ecuaciones).dot(sp.Matrix(dv_ecuaciones)))
    G=sp.simplify(sp.Matrix(dv_ecuaciones).dot(sp.Matrix(dv_ecuaciones)))

    return E, F, G

def primeraFormaFundamental_pt(ecuaciones, u, v, u0, v0):
    """
    Retorna la primera forma fundamental en un punto en forma de tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0              valor u del punto
    v0              valor v del punto
    """
    du_ecuaciones = [sp.diff(ecuaciones[i], u) for i in range(3)]
    dv_ecuaciones = [sp.diff(ecuaciones[i], v) for i in range(3)]

    du_ecuaciones_pt = [sp.N(du_ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_ecuaciones_pt = [sp.N(dv_ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    E_pt=sp.Matrix(du_ecuaciones_pt).dot(sp.Matrix(du_ecuaciones_pt))
    F_pt=sp.Matrix(du_ecuaciones_pt).dot(sp.Matrix(dv_ecuaciones_pt))
    G_pt=sp.Matrix(dv_ecuaciones_pt).dot(sp.Matrix(dv_ecuaciones_pt))

    return E_pt, F_pt, G_pt

def segundoFormaFundamental(ecuaciones, u, v):
    """
    Retorna la segunda forma fundamental en forma de tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    du_ecuaciones = [sp.diff(ecuaciones[i], u) for i in range(3)]
    dv_ecuaciones = [sp.diff(ecuaciones[i], v) for i in range(3)]
    duu_ecuaciones = [sp.diff(du_ecuaciones[i], u) for i in range(3)]
    duv_ecuaciones = [sp.diff(du_ecuaciones[i], v) for i in range(3)]
    dvv_ecuaciones = [sp.diff(dv_ecuaciones[i], v) for i in range(3)]

    e = sp.simplify(sp.det(sp.Matrix([du_ecuaciones, dv_ecuaciones, duu_ecuaciones]).T) / (sp.Matrix(du_ecuaciones).cross(sp.Matrix(dv_ecuaciones))).norm())
    f = sp.simplify(sp.det(sp.Matrix([du_ecuaciones, dv_ecuaciones, duv_ecuaciones]).T) / (sp.Matrix(du_ecuaciones).cross(sp.Matrix(dv_ecuaciones))).norm())
    g = sp.simplify(sp.det(sp.Matrix([du_ecuaciones, dv_ecuaciones, dvv_ecuaciones]).T) / (sp.Matrix(du_ecuaciones).cross(sp.Matrix(dv_ecuaciones))).norm())
    
    return e, f, g

def segundoFormaFundamental_pt(ecuaciones, u, v, u0, v0):
    """
    Retorna la segunda forma fundamental en un punto en forma de tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0              valor u del punto
    v0              valor v del punto
    """
    du_ecuaciones = [sp.diff(ecuaciones[i], u) for i in range(3)]
    dv_ecuaciones = [sp.diff(ecuaciones[i], v) for i in range(3)]
    duu_ecuaciones = [sp.diff(du_ecuaciones[i], u) for i in range(3)]
    duv_ecuaciones = [sp.diff(du_ecuaciones[i], v) for i in range(3)]
    dvv_ecuaciones = [sp.diff(dv_ecuaciones[i], v) for i in range(3)]

    du_ecuaciones_pt = [sp.N(du_ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_ecuaciones_pt = [sp.N(dv_ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    duu_ecuaciones_pt = [sp.N(duu_ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    duv_ecuaciones_pt = [sp.N(duv_ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dvv_ecuaciones_pt = [sp.N(dvv_ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    e_pt = sp.det(sp.Matrix([du_ecuaciones_pt, dv_ecuaciones_pt, duu_ecuaciones_pt]).T) / (sp.Matrix(du_ecuaciones_pt).cross(sp.Matrix(dv_ecuaciones_pt))).norm()
    f_pt = sp.det(sp.Matrix([du_ecuaciones_pt, dv_ecuaciones_pt, duv_ecuaciones_pt]).T) / (sp.Matrix(du_ecuaciones_pt).cross(sp.Matrix(dv_ecuaciones_pt))).norm()
    g_pt = sp.det(sp.Matrix([du_ecuaciones_pt, dv_ecuaciones_pt, dvv_ecuaciones_pt]).T) / (sp.Matrix(du_ecuaciones_pt).cross(sp.Matrix(dv_ecuaciones_pt))).norm()
    
    return e_pt, f_pt, g_pt

def curvaturaGauss(ecuaciones, u, v):
    """
    Retorna la curvatura de Gauss
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    E, F, G = primeraFormaFundamental(ecuaciones, u, v)
    e, f, g = segundoFormaFundamental(ecuaciones, u, v)
    return sp.simplify((e*g - f**2) / (E*G - F**2))

def curvaturaGauss_pt(ecuaciones, u, v, u0, v0):
    """
    Retorna la curvatura de Gauss en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0              valor u del punto
    v0              valor v del punto
    """
    E_pt, F_pt, G_pt = primeraFormaFundamental_pt(ecuaciones, u, v, u0, v0)
    e_pt, f_pt, g_pt = segundoFormaFundamental_pt(ecuaciones, u, v, u0, v0)
    return (e_pt*g_pt - f_pt**2) / (E_pt*G_pt - F_pt**2)

def curvaturaMedia(ecuaciones, u, v):
    """
    Retorna la curvatura media
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    E, F, G = primeraFormaFundamental(ecuaciones, u, v)
    e, f, g = segundoFormaFundamental(ecuaciones, u, v)
    return sp.simplify((e*G + g*E - 2*f*F) / (2*(E*G - F**2)))

def curvaturaMedia_pt(ecuaciones, u, v, u0, v0):
    """
    Retorna la curvatura media en un punto
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0              valor u del punto
    v0              valor v del punto
    """
    E_pt, F_pt, G_pt = primeraFormaFundamental_pt(ecuaciones, u, v, u0, v0)
    e_pt, f_pt, g_pt = segundoFormaFundamental_pt(ecuaciones, u, v, u0, v0)
    return (e_pt*G_pt + g_pt*E_pt - 2*f_pt*F_pt) / (2*(E_pt*G_pt - F_pt**2))

def curvaturasPrincipales(ecuaciones, u, v):
    """
    Retorna las curvaturas principales como tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    """
    K = curvaturaGauss(ecuaciones, u, v)
    H = curvaturaMedia(ecuaciones, u, v)
    raiz = sp.sqrt(H**2 - K)
    return sp.simplify(H + raiz), sp.simplify(H - raiz)

def curvaturasPrincipales_pt(ecuaciones, u, v, u0, v0):
    """
    Retorna las curvaturas principales en un punto como tupla
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0              valor u del punto
    v0              valor v del punto
    """
    K_pt = curvaturaGauss_pt(ecuaciones, u, v, u0, v0)
    H_pt = curvaturaMedia_pt(ecuaciones, u, v, u0, v0)
    raiz = sp.sqrt(H_pt**2 - K_pt)
    return H_pt + raiz, H_pt - raiz

def clasicfPt(ecuaciones, u, v, u0, v0):
    """
    Imprime la clasificacion de una superficie en un punto descrito con u y v
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0              valor u del punto
    v0              valor v del punto
    """
    K_pt = curvaturaGauss_pt(ecuaciones, u, v, u0, v0)
    if K_pt > 0:
        print('Eliptico')
    elif K_pt < 0:
        print('Hiperbólitco')
    elif K_pt == 0:
        print('Parabólico o planar')

def planoTangentePt(ecuaciones, u, v, u0, v0):
    """
    Imprime la clasificacion de una superficie en un punto descrito con u y v
    No se hacen comprobaciones de tipo

    Argumentos:
    ecuaciones      parametrizacion de superficie (lista de longitud 3 con funciones)
    u               primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    v               segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
    u0              valor u del punto
    v0              valor v del punto
    """
    x, y, z = sp.symbols('x, y, z', real = True)
    xyz = [x,y,z]
    ecuaciones_pt = [sp.N(ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    du_ecuaciones = [sp.diff(ecuaciones[i], u) for i in range(3)]
    dv_ecuaciones = [sp.diff(ecuaciones[i], v) for i in range(3)]

    du_ecuaciones_pt = [sp.N(du_ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]
    dv_ecuaciones_pt = [sp.N(dv_ecuaciones[i].subs([[u, u0],[v,v0]])) for i in range(3)]

    return sp.Matrix( sp.Matrix(du_ecuaciones_pt).cross(sp.Matrix(dv_ecuaciones_pt)) ).dot( sp.Matrix( [(xyz[i] - ecuaciones_pt[i]) for i in range(3)]) )

def dirPrinc(ecuaciones, u, v, u0, v0):
    a, b = sp.symbols('u, v', real = True)

    k1_pt, k2_pt = curvaturasPrincipales_pt(ecuaciones, u, v, u0, v0)
    print('Curvaturas:', k1_pt, k2_pt)
    E_pt, F_pt, G_pt = primeraFormaFundamental_pt(ecuaciones, u, v, u0, v0)
    print('1a forma: ', E_pt, F_pt, G_pt)
    e_pt, f_pt, g_pt = segundoFormaFundamental_pt(ecuaciones, u, v, u0, v0)
    print('2a forma', e_pt, f_pt, g_pt)


    ec1 = sp.Eq(sp.simplify(e_pt-k1_pt*E_pt)*a, sp.simplify(f_pt-k1_pt*F_pt)*b)
    ec2 = sp.Eq(sp.simplify(f_pt-k1_pt*F_pt)*a, sp.simplify(g_pt-k1_pt*G_pt)*b)
    solucion1 = sp.solve((ec1, ec2), (a, b))

    ec1 = sp.Eq(sp.simplify(e_pt-k2_pt*E_pt)*a, sp.simplify(f_pt-k2_pt*F_pt)*b)
    ec2 = sp.Eq(sp.simplify(f_pt-k2_pt*F_pt)*a, sp.simplify(g_pt-k2_pt*G_pt)*b)
    solucion2 = sp.solve((ec1, ec2), (a, b))

    return solucion1, solucion2
