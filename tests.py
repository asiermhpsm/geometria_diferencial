import unittest
from sympy import simplify, sympify
import sympy as sp
from app import app


u, v = sp.symbols('u, v', real = True)
x, y, z = sp.symbols('x, y z', real = True)
s, t = sp.symbols('s, t', real = True)

def str2exp(sup, var1=None, var2=None):
    if var1:
        u = sp.symbols(var1, real = True)
    else:
        u = sp.symbols('u', real = True)
        var1='u'

    if var2:
        v = sp.symbols(var2, real = True)
    else:
        v = sp.symbols('v', real = True)
        var2='v'

    if ',' in sup:
        elementos_str = sup[1:-1].split(',')
    else:
        elementos_str = sup
    superficie = [sp.simplify(sp.sympify(elem, locals={var1: u, var2: v})) for elem in elementos_str]
    
    return superficie


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    

    def test1(self):
        response = self.app.get('/plano_tangente?superficie=[u,v,u**2%2Bv**2]&u0=1&v0=1')
        self.assertEqual(response.status_code, 200)
        respuesta = sympify(response.get_data(as_text=True), locals={'x': x, 'y': y, 'z': z})
        respuesta_esperada = - 2*x - 2*y + z + 2
        if not respuesta.equals(respuesta_esperada):
            self.fail()

    def test2(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u,v,0]')
        self.assertEqual(response.status_code, 200)
        respuesta = str2exp(response.get_data(as_text=True))
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = (1,0,1)
        for i in range(3):
            if not respuesta[i].equals(respuesta_esperada[i]):
                self.fail()

    def test3(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[sin(u),cos(u), v]')
        self.assertEqual(response.status_code, 200)
        respuesta = str2exp(response.get_data(as_text=True))
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = (1,0,1)
        for i in range(3):
            if not respuesta[i].equals(respuesta_esperada[i]):
                self.fail()

    def test4(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u*cos(v),u*sin(v), 0]')
        self.assertEqual(response.status_code, 200)
        respuesta = str2exp(response.get_data(as_text=True))
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = (1,0,u**2)
        for i in range(3):
            if not respuesta[i].equals(respuesta_esperada[i]):
                self.fail()

    def test5(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u%2Bv, u*v, u-v]')
        self.assertEqual(response.status_code, 200)
        respuesta = str2exp(response.get_data(as_text=True))
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = (v**2+2, u*v, u**2+2)
        for i in range(3):
            if not respuesta[i].equals(respuesta_esperada[i]):
                self.fail()

    def test6(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u**2%2Bv, u-v**2, u]')
        self.assertEqual(response.status_code, 200)
        respuesta = str2exp(response.get_data(as_text=True))
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = (4*u**2+2, 2*u-2*v, 4*v**2+1)
        for i in range(3):
            if not respuesta[i].equals(respuesta_esperada[i]):
                self.fail()

    def test7(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u*cos(v), u*sin(v), u]')
        self.assertEqual(response.status_code, 200)
        respuesta = str2exp(response.get_data(as_text=True))
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = (2, 0, u**2)
        for i in range(3):
            if not respuesta[i].equals(respuesta_esperada[i]):
                self.fail()

    def test8(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u, 0, v]')
        self.assertEqual(response.status_code, 200)
        respuesta = str2exp(response.get_data(as_text=True))
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = (1,0,1)
        for i in range(3):
            if not respuesta[i].equals(respuesta_esperada[i]):
                self.fail()

    def test9(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[s, s**2, t]&var1=s&var2=t')
        self.assertEqual(response.status_code, 200)
        respuesta = str2exp(response.get_data(as_text=True))
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = (4*s**2+1, 0, 1)
        for i in range(3):
            print(respuesta[i], respuesta[i].subs([[s,1], [t, 1]]))
            print(respuesta_esperada[i], respuesta_esperada[i].subs([[s,1], [t, 1]]))
            if not respuesta[i].equals(respuesta_esperada[i]):
                self.fail()

if __name__ == "__main__":
    unittest.main()
