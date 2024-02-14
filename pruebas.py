import re

def extraer_funciones(string):
    string.replace(' ', '')

    coincidencias_funciones = re.findall(r'([a-zA-Z0-9]+)\(([\w,]+)\)', string)
    print(coincidencias_funciones)
    funciones = {}
    for coincidencia in coincidencias_funciones:
        funcion = coincidencia[0]
        variables  = set(coincidencia[1].split(','))
        string = re.sub(funcion+r'\(([\w,]+)\)', funcion, string)
        if funcion not in funciones:
            funciones[funcion] = variables
        elif funciones[funcion] != variables:
            raise Exception(f'Hay una inconsistencia de variables para la función {funcion}: se ha encontrado que esta definido a la vez por {funciones[funcion]} y por {variables}')

    coincidencias_lista = re.match(r'\[([^,\[\]]*),\s*([^,\[\]]*),\s*([^,\[\]]*)\]', string)
    if coincidencias_lista:
        return [coincidencias_lista.group(1), coincidencias_lista.group(2), coincidencias_lista.group(3)], funciones
    else:
        return string, funciones

# Ejemplos de uso
string1 = "[u+v, u-v + g(u,v), f(u)]"
string2 = "u+v"

print("Para el string '{}':".format(string1))
elementos1, funciones1 = extraer_funciones(string1)
print("Elementos extraídos:", elementos1)
print("Funciones extraídas:", funciones1)

print("\nPara el string '{}':".format(string2))
elementos2, funciones2 = extraer_funciones(string2)
print("Elementos extraídos:", elementos2)
print("Funciones extraídas:", funciones2)

for var in {'u', 'v'}:
    print(var)
