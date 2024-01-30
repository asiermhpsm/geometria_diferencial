import sympy as sp

u = sp.symbols('u')

W = sp.Matrix([[1, 0], [0, u**2]])

res = W.eigenvects(simplify=True)

k1 = res[0][0]
autovct1 = res[0][-1][0]

print(k1)
print(autovct1)

k2 = res[1][0]
autovct2 = res[1][-1][0]

print(k2)
print(autovct2)