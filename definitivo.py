import numpy as np
import sympy as sp

u, v = sp.symbols('u, v', real = True)

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
    Retorna la primera forma fundamental en forma de matriz de funciones 
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

    return sp.Matrix([[E, F], [F, G]])

print(primeraFormaFundamental([sp.ln(u+v+1), v**2+sp.sinh(-u+v), u**2+2*v], u, v))