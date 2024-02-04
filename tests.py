import unittest
from sympy import sympify
import sympy as sp
from app import app
import json

def comprueba(response, soluciones_esperadas):
    if response.status_code != 200:
        return False, f"No se ha obtenido el codigo de respuesta esperado: {response.status_code}"
    esCorrecto = True
    mensajeError = ''
    response = json.loads(response.get_data())
    for k, v in soluciones_esperadas.items():
        if 'tangente' in k:
            vector_tg_esperado = v.strip().split('=')
            vector_tg_respuesta = response[k].strip().split('=')
            if len(vector_tg_esperado)!=2 or len(vector_tg_respuesta)!=2:
                esCorrecto = False
                mensajeError = f"No se ha podido procesar el vector tangente\n\n"
            tg_esperado = vector_tg_esperado[0]+'-('+vector_tg_esperado[1]+')'
            tg_respuesta = vector_tg_respuesta[0]+'-('+vector_tg_respuesta[1]+')'
            resta = sp.simplify(sympify(tg_esperado + '-(' + tg_respuesta + ')'))
            if resta != 0:
                resta_2 = sp.simplify(sympify(tg_esperado + '+' + tg_respuesta))
                if resta_2 == 0:
                    continue
                esCorrecto = False
                mensajeError = mensajeError + f"La resta entre la respuesta obtenida de {k}\n{response[k]}\ny la respuesta esperada\n{v}\ndebería ser 0 pero da\n{resta}\n\n"
        elif '[' in v:
            vector_esperado = v.strip()[1:-1].split(',')
            vector_respuesta = response[k].strip()[1:-1].split(',')
            if len(vector_respuesta) != len(vector_esperado):
                esCorrecto = False
                mensajeError = f"No se ha podido procesar la respuesta {k}\n\n"
            for i in range(len(vector_respuesta)):
                resta = sp.simplify(sympify(vector_esperado[i] + '-(' + vector_respuesta[i] + ')'))
                if resta != 0:
                    esCorrecto = False
                    mensajeError = mensajeError + f"La resta entre los {i}º elementos de la respuesta obtenida de {k}\n{response[k]}\ny la respuesta esperada\n{v}\n debería ser 0 pero da\n{resta}\n\n"
        else:
            resta = sp.simplify(sympify(v + '-(' + response[k] + ')'))
            if resta != 0:
                esCorrecto = False
                mensajeError = mensajeError + f"La resta entre la respuesta obtenida de {k}\n{response[k]}\ny la respuesta esperada\n{v}\ndebería ser 0 pero da\n{resta}\n\n"

    return esCorrecto, mensajeError

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test1(self):
        sup = '[u, v, u**2 %2B v**2]'
        respuestas_esperadas={
            'normal' : '[-2*u/sqrt(4*u**2+4*v**2+1), -2*v/sqrt(4*u**2+4*v**2+1), 1/sqrt(4*u**2+4*v**2+1)]',
            'E' : '1+4*u**2',
            'F' : '4*u*v',
            'G' : '1+4*v**2',
            'e' : '2/sqrt(4*u**2+4*v**2+1)',
            'f' : '0',
            'g' : '2/sqrt(4*u**2+4*v**2+1)',
            'tangente' : '-2*u*x-2*v*y+z = -u**2 - v**2',
            'K' : '4/(4*u**2+4*v**2+1)**2',
            'H' : '(2+4*u**2+4*v**2)/(4*u**2+4*v**2+1)**(3/2)',
        }
        esCorrecto, mensaje = comprueba(self.app.get(f'/description?superficie={sup}'), respuestas_esperadas)
        if not esCorrecto:
            self.fail(mensaje)

    def test2(self):
        sup = '[u, v, 0]'
        respuestas_esperadas={
            'normal' : '[0,0,1]',
            'E' : '1',
            'F' : '0',
            'G' : '1',
            'e' : '0',
            'f' : '0',
            'g' : '0',
            'tangente' : 'z=0',
            'K' : '0',
            'H' : '0',
            'k1' : '0',
            'k2' : '0',
        }
        esCorrecto, mensaje = comprueba(self.app.get(f'/description?superficie={sup}'), respuestas_esperadas)
        if not esCorrecto:
            self.fail(mensaje)

    @unittest.skip("Hay que comprobar K y k2")
    def test3(self):
        sup = '[sin(u), cos(u), v]'
        respuestas_esperadas={
            'normal' : '[-sin(u), -cos(u), 0]',
            'E' : '1',
            'F' : '0',
            'G' : '1',
            'e' : '1',
            'f' : '0',
            'g' : '0',
            'tangente' : '-sin(u)*x -cos(u)*y = -1',
            'K' : '0',
            'H' : '0',
            'k1' : '0',
            'k2' : '0',
        }
        esCorrecto, mensaje = comprueba(self.app.get(f'/description?superficie={sup}'), respuestas_esperadas)
        if not esCorrecto:
            self.fail(mensaje)

    @unittest.skip("Hay que comprobar normal")
    def test4(self):
        sup = '[u*sin(v), u*cos(v), 0]'
        respuestas_esperadas={
            'normal' : '[0,0,u/abs(u)]',
            'E' : '1',
            'F' : '0',
            'G' : 'u^2',
            'e' : '0',
            'f' : '0',
            'g' : '0',
            'tangente' : 'u*z=0',
            'K' : '0',
            'H' : '0',
            'k1' : '0',
            'k2' : '0',
        }
        esCorrecto, mensaje = comprueba(self.app.get(f'/description?superficie={sup}'), respuestas_esperadas)
        if not esCorrecto:
            self.fail(mensaje)

    @unittest.skip("Hay que comprobar K y H")
    def test5(self):
        sup = '[u %2B v, u*v, u-v]'
        respuestas_esperadas={
            'normal' : '[(-u-v)/sqrt(2*u^2 + 2*v^2 + 4), 2/sqrt(2*u^2 + 2*v^2 + 4), (u-v)/sqrt(2*u^2 + 2*v^2 + 4)]',
            'E' : 'v^2 + 2',
            'F' : 'u*v',
            'G' : 'u^2+2',
            'e' : '0',
            'f' : '2/sqrt(2*u^2 + 2*v^2 + 4)',
            'g' : '0',
            'tangente' : '-(u+v)*x + 2*y + (u-v)*z = -2*u*v',
            'K' : '4/(2*u^2 + 2*v^2 + 4)',
            'H' : '2*u*v/(2*u^2 + 2*v^2 + 4)^(3/2)',
        }
        esCorrecto, mensaje = comprueba(self.app.get(f'/description?superficie={sup}'), respuestas_esperadas)
        if not esCorrecto:
            self.fail(mensaje)

    #TODO- test6
            
    def test7(self):
        sup = '[u*cos(v), u*sin(v), u]'
        respuestas_esperadas={
            'E' : '2',
            'F' : '0',
            'G' : 'u^2',
            'e' : '0',
            'f' : '0',
            'g' : 'u^2/(sqrt(2)*abs(u))',
            'tangente' : '-u*cos(v)*x - u*sin(v)*y + u*z = 0',
            'K' : '0',
            'H' : '1/(2*sqrt(2)*abs(u))',
            'k1' : '0',
            'k2' : '1/(sqrt(2)*abs(u))',
        }
        esCorrecto, mensaje = comprueba(self.app.get(f'/description?superficie={sup}'), respuestas_esperadas)
        if not esCorrecto:
            self.fail(mensaje)

    @unittest.skip("Hay que comprobar K, k1 y k2")
    def test8(self):
        sup = '[u*cos(v), u*sin(v), v*a]'
        respuestas_esperadas={
            'E' : '1',
            'F' : '0',
            'G' : 'u^2+a^2',
            'e' : '0',
            'f' : '-a/sqrt(u^2+a^2)',
            'g' : '0',
            'tangente' : 'a*sin(v)*x - a*cos(v)*y + u*z = a*v*u',
            'K' : 'a^4/(u^2+a^2)^3',
            'H' : '0',
            'k1' : 'sqrt(-a^4/(u^2+a^2)^3)',
            'k2' : '-sqrt(-a^4/(u^2+a^2)^3)',
        }
        esCorrecto, mensaje = comprueba(self.app.get(f'/description?superficie={sup}'), respuestas_esperadas)
        if not esCorrecto:
            self.fail(mensaje)







if __name__ == "__main__":
    unittest.main()
