import re
import sympy as sp

def verificar_y_extraer(expresion):
    # Definimos el patrón de la expresión regular
    expresion = expresion.replace(" ", "")
    patron = r"([-+]?\d*[\.,]?\d+|\w+)\*x([-+]\d*[\.,]?\d+|\w+)\*y<([-+]?\d*[\.,]?\d+|\w+)"
    
    # Intentamos hacer coincidir el patrón con la expresión
    coincidencia = re.match(patron, expresion)
    
    if coincidencia:
        # Si hay coincidencia, extraemos los valores de a, b y r
        a = coincidencia.group(1)
        b = coincidencia.group(2)
        r = coincidencia.group(3)
        return a, b, r
    else:
        # Si no hay coincidencia, retornamos None
        return None

# Ejemplo de uso
expresion = "ab * x^2 + 2.3 * y^2 < 2.2 "
expresion = "1*u^2+2*v^2<3"
resultado = verificar_y_extraer(expresion)
if resultado:
    a, b, r = resultado
    print("La expresión es válida. a =", a, ", b =", b, ", r =", r)
else:
    print("La expresión no tiene el formato correcto.")



u, v = sp.symbols('u v', real=True)
sy_expresion = sp.sympify(expresion, locals={'u': u, 'v': v})
if isinstance(sy_expresion, sp.StrictLessThan):
    expr = sy_expresion.lhs - sy_expresion.rhs
    a = expr.coeff(u**2)
    b = expr.coeff(v**2)
    r = expr - a*u**2 - b*v**2
    if r.is_constant():
        a = a/-r
        b = b/-r
        r = 1
        print(a, b, r)




