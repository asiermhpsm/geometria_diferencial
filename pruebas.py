def funcion_principal(funcion_parametro):
    # Aquí ejecutas la acción que quieras antes de llamar a la función parametro
    print("Ejecutando acción antes de llamar a la función parametro")
    
    if funcion_parametro is funcion_b:
        print('Voy a ejecutar la funcion B')

    # Llamas a la función parametro que se pasó como argumento
    funcion_parametro()
    
    # Aquí ejecutas la acción que quieras después de llamar a la función parametro
    print("Ejecutando acción después de llamar a la función parametro")

# Definimos algunas funciones que podríamos pasar como parámetro a funcion_principal
def funcion_a():
    print("Estoy en la función A")

def funcion_b():
    print("Estoy en la función B")

# Llamamos a funcion_principal y pasamos una función como parámetro
funcion_principal(funcion_b)
