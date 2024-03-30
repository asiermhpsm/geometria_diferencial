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
expresion = "ab * x + 2.3 * y < 2,2 "
resultado = verificar_y_extraer(expresion)
if resultado:
    a, b, r = resultado
    print("La expresión es válida. a =", a, ", b =", b, ", r =", r)
else:
    print("La expresión no tiene el formato correcto.")


a = sp.pi
b = 2
c = a/b
print(c)