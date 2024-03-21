import sympy as sp

# Definir las variables
x, y, z = sp.symbols('x y z')

# Definir una expresión que contenga estas variables
expresion = x**2 + 2*y

# Obtener las variables libres en la expresión
variables_libres = expresion.free_symbols

# Calcular el número de variables en la expresión
num_variables = len(variables_libres)

# Imprimir el resultado
print("La expresión tiene", num_variables, "variable(s):", variables_libres)
variables_libres.remove(z)
print(variables_libres)