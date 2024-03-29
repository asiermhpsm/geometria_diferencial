import sympy as sp

# Definir símbolos
x, y = sp.symbols('x y')

# Definir expresiones
expresion1 = x**2
expresion2 = 2*x + 1

# Comparar las expresiones
rel = sp.GreaterThan(expresion1, expresion2)  # Gt significa "Greater Than" (Mayor que)
print(rel)

# Evaluar la relación
resultado = rel.simplify()

# Mostrar el resultado
if resultado:
    print("expresion1 es mayor que expresion2")
else:
    print("expresion1 NO es mayor que expresion2")
