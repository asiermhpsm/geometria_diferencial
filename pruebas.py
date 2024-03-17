import utils.calc_param as calc_imp
import sympy as sp

u, v = sp.symbols('u v', real=True)

res = {
    'sup' : sp.Matrix([u, v, sp.sqrt(1 - u**2 - v**2)]),
    'u' : u,
    'v' : v
}

res = calc_imp.descripccion(res)

def simplifica_cond(f, cond: sp.Expr) -> sp.Expr:
    aux_neg = sp.symbols('aux_neg', negative=True)
    sust = sp.simplify(f.subs(cond.lhs - cond.rhs, aux_neg).subs(cond.lhs, aux_neg + cond.rhs))
    return sp.simplify(sust.subs(aux_neg, cond.lhs - cond.rhs))

cond = u**2+v**2 < 1
for k, v in res.items():
    if not isinstance(v, list):
        print(k)
        sp.pprint(v)
        sp.pprint(simplifica_cond(v, cond))
        print()
    else:
        print(k)
        print(v)
        print()

