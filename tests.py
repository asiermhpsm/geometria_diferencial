import unittest
from sympy import sympify
import sympy as sp
from app import app


u, v = sp.symbols('u, v', real = True)
x, y, z = sp.symbols('x, y z', real = True)
s, t = sp.symbols('s, t', real = True)
a= sp.symbols('a', real = True)

def str2exp(sup, var1=None, var2=None, consts=None):
    variables = {}

    if var1:
        u = sp.symbols(var1, real = True)
    else:
        u = sp.symbols('u', real = True)
        var1='u'
    variables[var1] = u

    if var2:
        v = sp.symbols(var2, real = True)
    else:
        v = sp.symbols('v', real = True)
        var2='v'
    variables[var2] = v

    if consts:
        variables.update(consts)

    elementos_str = sup[1:-1].split(',')
    return [sp.sympify(elem, locals=variables) for elem in elementos_str]


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    

    def test1(self):
        response = self.app.get('/plano_tangente?superficie=[u,v,u**2%2Bv**2]&u0=1&v0=1')

        self.assertEqual(response.status_code, 200)

        respuesta_esperada = '- 2*x - 2*y + z + 2'
        resta = sympify(response.get_data(as_text=True) + '-(' + respuesta_esperada + ')')
        self.assertEqual(resta, 0)

    def test2(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u,v,0]')
        self.assertEqual(response.status_code, 200)

        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)

        respuesta_esperada = ('1','0','1')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    def test3(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[sin(u),cos(u), v]')
        self.assertEqual(response.status_code, 200)

        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)

        respuesta_esperada = ('1','0','1')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    def test4(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u*cos(v),u*sin(v), 0]')
        self.assertEqual(response.status_code, 200)

        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)

        respuesta_esperada = ('1','0','u**2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    def test5(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u%2Bv, u*v, u-v]')
        self.assertEqual(response.status_code, 200)

        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)

        respuesta_esperada = ('v**2+2', 'u*v', 'u**2+2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    def test6(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u**2%2Bv, u-v**2, u]')
        self.assertEqual(response.status_code, 200)

        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)

        respuesta_esperada = ('4*u**2+2', '2*u-2*v', '4*v**2+1')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    def test7(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u*cos(v), u*sin(v), u]')
        self.assertEqual(response.status_code, 200)

        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)

        respuesta_esperada = ('2', '0', 'u**2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    def test8(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u*cos(v), u*sin(v), v*a]')
        self.assertEqual(response.status_code, 200)

        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)

        respuesta_esperada = ('1', '0', 'a**2+u**2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    def test9(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[u, 0, v]')
        self.assertEqual(response.status_code, 200)

        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)

        respuesta_esperada = ('1','0','1')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    def test10(self):
        response = self.app.get('/primera_forma_fundamental?superficie=[s, s**2, t]&var1=s&var2=t')
        self.assertEqual(response.status_code, 200)

        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)

        respuesta_esperada = ('4*s**2+1', '0', '1')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    def test11(self):
        sup = '[u, v, 0]'

        response = self.app.get(f"/primera_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('1','0','1')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/segunda_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('0','0','0')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    @unittest.skip("Hay que comprobar como hace las simplificaciones")
    def test12(self):
        sup = '[cos(s), sin(s), t]'

        response = self.app.get(f"/primera_forma_fundamental?superficie={sup}&var1=s&var2=t")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('1','0','1')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/segunda_forma_fundamental?superficie={sup}&var1=s&var2=t")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('-1','0','0')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    @unittest.skip("Hay que comprobar como hace las simplificaciones")
    def test13(self):
        sup = 'a*cos(u)*cos(v), a*cos(u)*sin(v), a*sin(u)'

        response = self.app.get(f"/primera_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('a**2','0','a**2*cos(u)**2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/segunda_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('a','0','a*cos(u)**2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    @unittest.skip("Hay que comprobar como hace las simplificaciones")
    def test14(self):
        sup = '(a%2Bb*cos(u))*cos(v), (a%2Bb*cos(u))*sin(v), b*sin(u)'

        response = self.app.get(f"/primera_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('b**2','0','(a+b*cos(u))**2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/segunda_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('b','0','cos(u)*(a+b*cos(u))')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

if __name__ == "__main__":
    unittest.main()
