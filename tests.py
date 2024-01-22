import unittest
from sympy import sympify
import sympy as sp
from app import app


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
    
    def test0(self):
        response = self.app.get('/grafica?superficie=[cos(u %2B v), sin(u - v), u - v]')
        self.assertEqual(response.status_code, 200)
        

    def test1(self):
        response = self.app.get('/plano_tangente?superficie=[u,v,u**2%2Bv**2]&u0=1&v0=1')
        self.assertEqual(response.status_code, 200)
        respuesta_esperada = '- 2*x - 2*y + z + 2'
        resta = sympify(response.get_data(as_text=True) + '-(' + respuesta_esperada + ')')
        self.assertEqual(resta, 0)

    def test2(self):
        sup = '[u, v, 0]'

        response = self.app.get(f"/vector_normal?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('0','0','1')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

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

        response = self.app.get(f"/curvatura_Gauss?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)
        respuesta_esperada = '0'
        resta = sympify(respuesta+'-('+respuesta_esperada+')')
        self.assertEqual(resta, 0)

        response = self.app.get(f"/curvatura_media?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)
        respuesta_esperada = '0'
        resta = sympify(respuesta+'-('+respuesta_esperada+')')
        self.assertEqual(resta, 0)

        response = self.app.get(f"/curvaturas_principales?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 2)
        respuesta_esperada = ('0','0')
        for i in range(2):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/plano_tangente?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta_esperada = 'z'
        resta = sympify(response.get_data(as_text=True) + '-(' + respuesta_esperada + ')')
        self.assertEqual(resta, 0)

        #TODO-hacer test direcciones principales
        response = self.app.get(f"/direcciones_principales?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        aux = response.get_data(as_text=True)[2:-2].replace(' ','').replace('(','').replace(')','').split(',')
        self.assertEqual(len(respuesta), 2)
        respuesta = [[aux[0], aux[1]], [aux[2], aux[3]]]
        respuesta_esperada = (('1', '0'),('0', '1'))
        resta1 = [
                    [sympify(respuesta[0][0]+'-('+respuesta_esperada[0][0]+')'), 
                    sympify(respuesta[0][1]+'-('+respuesta_esperada[0][1]+')') ], 
                    [sympify(respuesta[1][0]+'-('+respuesta_esperada[1][0]+')'), 
                    sympify(respuesta[1][1]+'-('+respuesta_esperada[1][1]+')') ]
                   ]
        resta2 = [
                    [sympify(respuesta[1][0]+'-('+respuesta_esperada[0][0]+')'), 
                    sympify(respuesta[1][1]+'-('+respuesta_esperada[0][1]+')') ], 
                    [sympify(respuesta[0][0]+'-('+respuesta_esperada[1][0]+')'), 
                    sympify(respuesta[0][1]+'-('+respuesta_esperada[1][1]+')') ]
                   ]
        
        response = self.app.get(f"/clasificacion_punto?superficie={sup}&u0=1&v0=2")
        self.assertEqual(response.status_code, 200)
        respuesta_esperada = 'Planar'
        resta = sympify(response.get_data(as_text=True) + '-(' + respuesta_esperada + ')')
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
        sup = '[a*cos(u)*cos(v), a*cos(u)*sin(v), a*sin(u)]'

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
        sup = '[a %2B b*cos(u))*cos(v), (a %2B b*cos(u))*sin(v), b*sin(u)]'

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

    @unittest.skip("Hay que comprobar como hace las simplificaciones")
    def test15(self):
        sup = '[u, u**2 %2B v, v]'

        response = self.app.get(f"/primera_forma_fundamental?superficie={sup}&u0=1&v0=1")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('5','2','2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/segunda_forma_fundamental?superficie={sup}&u0=1&v0=1")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('-2','0','0')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    @unittest.skip("Hay que comprobar como hace las simplificaciones")
    def test16(self):
        sup = '[cos(v), sin(v), u]'

        response = self.app.get(f"/vector_normal?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('-cos(v)','-sin(v)','0')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

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
        respuesta_esperada = ('0','0','1')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    @unittest.skip("Hay que comprobar como hace las simplificaciones")
    def test17(self):
        sup = '[cosh(u)*cos(v), cosh(u)*sin(v), sinh(u)]'

        response = self.app.get(f"/primera_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('cosh(2*u)','0','cosh(u)**2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/segunda_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('-1/sqrt(cosh(2*u))','0','cosh(u)**2/sqrt(cosh(2*u))')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    @unittest.skip("Hay que comprobar como hace las simplificaciones")
    def test18(self):
        sup = '[u, v, u**2 %2B v**2]'

        response = self.app.get(f"/vector_normal?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('-2*u/sqrt(4*u**2 + 4*v**2 + 1)','-2*v/sqrt(4*u**2 + 4*v**2 + 1)','1/sqrt(4*u**2 + 4*v**2 + 1)')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/primera_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('4*u**2 + 1','4*u*v','4*v**2 + 1')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/segunda_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('1*u/sqrt(4*u**2 + 4*v**2 + 1)','0','1*u/sqrt(4*u**2 + 4*v**2 + 1)')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    @unittest.skip("Hay que comprobar como hace las simplificaciones")
    def test19(self):
        sup = '[s*cos(t), s*sin(t), s**2]'

        response = self.app.get(f"/vector_normal?superficie={sup}&var1=s&var2=t")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('-2*s*cos(t)/sqrt(4*s**2 + 1)','-2*s*sin(t)/sqrt(4*s**2 + 1)','1/sqrt(4*s**2 + 1)')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/primera_forma_fundamental?superficie={sup}&var1=s&var2=t")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('4*s**2 + 1','0','s**2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/segunda_forma_fundamental?superficie={sup}&var1=s&var2=t")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('1/sqrt(4*s**2 + 1)','0','s**2/sqrt(4*s**2 + 1)')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    @unittest.skip("Hay que comprobar como hace las simplificaciones")
    def test20(self):
        sup = '[cos(u)*cos(v), -cos(u)*sin(v), 2*sin(u)]'

        response = self.app.get(f"/vector_normal?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('2*cos(u)*cos(v)/sqrt(1+3*cos(u)**2)','-2*cos(u)*sin(v)/sqrt(1+3*cos(u)**2)','sin(u)/sqrt(1+3*cos(u)**2)')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/primera_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('1+cos(u)**2','0','cos(u)**2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/segunda_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('-2/sqrt(1+3*cos(u)**2)','0','-2*cos(u)**2/sqrt(1+3*cos(u)**2)')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/curvaturas_principales?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('-2/(sqrt(1+3*cos(u)**2)**3)','-2/sqrt(1+3*cos(u)**2)')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

    @unittest.skip("Hay que comprobar como hace las simplificaciones")
    def test21(self):
        sup = '[u*cos(v), u*sin(v), (u**2)/2]'

        response = self.app.get(f"/vector_normal?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('-u*cos(v)/sqrt(1+u**2)','-u*sin(v)/sqrt(1+u**2)','1/sqrt(1+u**2)')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/primera_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('u**2+1','0','u**2')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)

        response = self.app.get(f"/segunda_forma_fundamental?superficie={sup}")
        self.assertEqual(response.status_code, 200)
        respuesta = response.get_data(as_text=True)[1:-1].split(',')
        self.assertEqual(len(respuesta), 3)
        respuesta_esperada = ('1/sqrt(1+u**2)','0','u**2/sqrt(1+u**2)')
        for i in range(3):
            resta = sympify(respuesta[i]+'-('+respuesta_esperada[i]+')')
            self.assertEqual(resta, 0)


if __name__ == "__main__":
    unittest.main()
