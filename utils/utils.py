
def normalizaSimbolos(cadena: str) -> str:
    cadena = cadena.replace('√', 'sqrt')
    cadena = cadena.replace('π', 'pi')
    cadena = cadena.replace('sen', 'sin')
    cadena = cadena.replace('senh', 'sinh')
    cadena = cadena.replace('tg', 'tan')
    cadena = cadena.replace('tgh', 'tanh')

    return cadena
