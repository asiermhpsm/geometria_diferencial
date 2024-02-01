import sympy as sp

u, v = sp.symbols('u, v')
dominio_u = (0, 2*sp.pi)
dominio_v = (0, 2*sp.pi)

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
    ecuaciones.append(dominio_u[0] <= u)
    ecuaciones.append(u <= dominio_u[1])
    print(ecuaciones)
    soluciones = sp.solve(ecuaciones, (u, v), dict=False)
    if not soluciones:
        raise('El punto dado no esta en la superficie.')
    print(soluciones)
    return soluciones

xyz_to_uv([u**2, v**4, 0], u, v, 0, 0, 0)
xyz_to_uv([u**2, v**4, 0], u, v, 1, 1, 0)
xyz_to_uv([sp.cos(u), sp.sin(v), 0], u, v, 0, 0, 0)


"""from sympy import symbols, Eq, solve
from sympy.solvers.inequalities import solve_univariate_inequality

# Definir la variable
x = symbols('x')

# Definir la ecuación
ecuacion = Eq(x**2 - 4, 0)

# Resolver la ecuación en el dominio [0, 5]
soluciones = solve(ecuacion, x, domain=(0, 5))

print(f"Soluciones en el dominio [0, 5]: {soluciones}")"""
