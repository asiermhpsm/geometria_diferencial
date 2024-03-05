import utils.toLatex as tx
import utils.calc as calc
import sympy as sp

a, b, c, d = sp.symbols('a b c d', real=True)
E = 1 + a**2/c**2
F = a*b/c**2
G = 1 + b**2/c**2
print(sp.simplify(E*G-F**2))
print(sp.simplify(sp.sqrt(E*G-F**2)))

u, v = sp.symbols('u, v', real=True)
r = sp.Symbol('r', real=True, positive=True)
res = {
    'sup': sp.Matrix([u, v, sp.sqrt(1-u**2-v**2)]).T,
    'u' : u,
    'v' : v
}

res = calc.descripccion(res)

def sympy2latex(diccionario: dict) -> dict:
    return {k: sp.latex(v) for k, v in diccionario.items()}

#res = sympy2latex(res)

#print(tx.imprime_resultados(tx.res_curv_Gauss(res)))


"""from utils.graph import ejemplo_sup, sup_param
u, v = sp.symbols('u, v', real=True)
fig = sup_param(sp.Matrix([u, v, sp.sqrt(1-u**2-v**2)]).T, u,v, -1,1,-1,1)
fig.show()
#ejemplo_sup()"""
