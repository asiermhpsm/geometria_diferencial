import utils.toLatex as tx
import utils.calc as calc
import sympy as sp

u, v = sp.symbols('u, v', real=True)
res = {
    'sup': sp.Matrix([sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v) , sp.sin(u)]).T,
    'u' : u,
    'v' : v
}

res = calc.descripccion(res)

def sympy2latex(diccionario: dict) -> dict:
    return {k: sp.latex(v) for k, v in diccionario.items()}

#res = sympy2latex(res)

print(tx.imprime_resultados(tx.res_normal(res)))


"""from utils.graph import ejemplo_sup
ejemplo_sup()"""
