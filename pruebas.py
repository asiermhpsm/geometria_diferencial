from sympy import symbols, Matrix, diff

# Definir las variables y las expresiones
u, v = symbols('u v')
expresiones = [u**2, v**3, u + v]

# Crear el vector de funciones como una Matrix de SymPy
vec_funciones = Matrix(expresiones)

# Calcular el vector de derivadas
vec_derivadas = diff(vec_funciones, v)

# Imprimir el resultado
print(vec_derivadas)
