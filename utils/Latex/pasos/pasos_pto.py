from sympy import latex

def EscribeDerivadasPrimerOrden_pt(res):
    return [
        r'''Cálculo de la derivada parcial respecto a $'''+ latex(res['u']) + r'''$: la derivada parcial respecto a $'''+ latex(res['u']) + r'''$ es
$$\varphi_{'''+ latex(res['u']) + r'''}='''+ latex(res['du'], mat_delim='(') + r'''$$''',
        r'''Sustitución en el punto de la derivada parcial respecto a $'''+ latex(res['u']) + r'''$: la derivada parcial respecto a $'''+ latex(res['u']) + r'''$ en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\varphi_{'''+ latex(res['u']) + r'''}('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')='''+ latex(res['du_pt'], mat_delim='(') + r'''$$''',

        r'''Cálculo de la derivada parcial respecto a $'''+ latex(res['v']) + r'''$: la derivada parcial respecto a $'''+ latex(res['v']) + r'''$ es
$$\varphi_{'''+ latex(res['v']) + r'''}='''+ latex(res['dv'], mat_delim='(') + r'''$$''',
        r'''Sustitución en el punto de la derivada parcial respecto a $'''+ latex(res['v']) + r'''$: la derivada parcial respecto a $'''+ latex(res['v']) + r'''$ en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\varphi_{'''+ latex(res['v']) + r'''}('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')='''+ latex(res['dv_pt'], mat_delim='(') + r'''$$'''
    ]

def EscribeDerivadasSegundoOrden_pt(res):
    return [
        r'''Cálculo de la derivada parcial respecto a $'''+ latex(res['u'])+latex(res['u']) + r'''$: la derivada parcial respecto a $'''+ latex(res['u'])+latex(res['u']) + r'''$ es
$$\varphi_{'''+ latex(res['u'])+latex(res['u']) + r'''}='''+ latex(res['duu'], mat_delim='(') + r'''$$''',
        r'''Sustitución en el punto de la derivada parcial respecto a $'''+ latex(res['u'])+latex(res['u']) + r'''$: la derivada parcial respecto a $'''+ latex(res['u'])+latex(res['u']) + r'''$ en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\varphi_{'''+ latex(res['u'])+latex(res['u']) + r'''}('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')='''+ latex(res['duu_pt'], mat_delim='(') + r'''$$''',

        r''''Cálculo de la derivada parcial respecto a $'''+ latex(res['u'])+latex(res['v']) + r'''$: la derivada parcial respecto a $'''+ latex(res['u'])+latex(res['v']) + r'''$ es
$$\varphi_{'''+ latex(res['u'])+latex(res['v']) + r'''}='''+ latex(res['duu'], mat_delim='(') + r'''$$''',
        r'''Sustitución en el punto de la derivada parcial respecto a $'''+ latex(res['u'])+latex(res['v']) + r'''$: la derivada parcial respecto a $'''+ latex(res['u'])+latex(res['v']) + r'''$ en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\varphi_{'''+ latex(res['u'])+latex(res['v']) + r'''}('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')='''+ latex(res['duv_pt'], mat_delim='(') + r'''$$''',

        r'''Cálculo de la derivada parcial respecto a $'''+ latex(res['v'])+latex(res['v']) + r'''$: la derivada parcial respecto a $'''+ latex(res['v'])+latex(res['v']) + r'''$ es
$$\varphi_{'''+ latex(res['v'])+latex(res['v']) + r'''}='''+ latex(res['duu'], mat_delim='(') + r'''$$''',
        r'''Sustitución en el punto de la derivada parcial respecto a $'''+ latex(res['v'])+latex(res['v']) + r'''$: la derivada parcial respecto a $'''+ latex(res['v'])+latex(res['v']) + r'''$ en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\varphi_{'''+ latex(res['v'])+latex(res['v']) + r'''}('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')='''+ latex(res['duu_pt'], mat_delim='(') + r'''$$''',
    ]

def EscribeProdVect_pt(res):
    return [
        r'''Cálculo del producto vectorial de las derivadas parciales: el producto vectorial de las derivadas parciales de primer orden en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\varphi_{'''+ latex(res['u']) + r'''}\times\varphi_{'''+ latex(res['v']) + r'''}='''+ latex(res['duXdv_pt'], mat_delim='(') + r'''$$'''
    ]


def EscribeNormProdVect_pt(res):
    return [
        r'''Cálculo de la norma del producto vectorial: la norma del producto vectorial de las derivadas parciales de primer orden en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\|\varphi_{'''+ latex(res['u']) + r'''}\times\varphi_{'''+ latex(res['v']) + r'''}\|='''+ latex(res['norma_pt']) + r'''$$'''
    ]

def EscribeVectNormal_pt(res):
    return [
        r'''Aplicación de la fórmula del vector normal: Aplicando su fórmula, el vector normal en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\Vec{n} ='''+ latex(res['normal_pt'], mat_delim='(') + r'''$$'''
    ]

def EscribePlanoTang_pt(res):
    return[
        r'''Cálculo del afín plano tangente: Aplicando su fórmula, el plano afín tangente en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$'''+ latex(res['tangente_pt']) + r'''$$'''
    ]

def EscribePFF_pt(res):
    return [
        r'''Cálculo de la primera forma fundamental: aplicando las fórmulas de cada una de sus componenetes, la primera forma fundamental en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\left[I\right]=\left(\begin{matrix}'''+latex(res['E_pt'])+r''' & '''+latex(res['F_pt'])+r''' \\ '''+latex(res['F_pt'])+r''' & '''+latex(res['G_pt'])+r'''\end{matrix}\right)$$'''
    ]

def EscribeSegundaFF_pt(res):
    return [
        r'''Cálculo de la segunda forma fundamental: aplicando las fórmulas de cada una de sus componenetes, la segunda forma fundamental en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\left[II\right]=\left(\begin{matrix}'''+latex(res['e_pt'])+r''' & '''+latex(res['f_pt'])+r''' \\ '''+latex(res['f_pt'])+r''' & '''+latex(res['g_pt'])+r'''\end{matrix}\right)$$'''
    ]

def EscribeCurvGauss_pt(res):
    return [
        r'''Cálculo de la curvatura de Gauss: aplicando su fórmula, la curvatura de Gauss en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$K='''+latex(res['K_pt'])+r'''$$'''
    ]

def EscribeCurvMedia_pt(res):
    return [
        r'''Cálculo de la curvatura media: aplicando su fórmula, la curvatura media en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$H='''+latex(res['H_pt'])+r'''$$'''
    ]

def EscribeCurvsPrincipales_pt(res):
    return [
        r'''Cálculo de las curvaturas principales: aplicando su fórmula, las curvaturas principales en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ son
$$(\kappa_1, \kappa_2)=\left(\begin{matrix}'''+latex(res['k1_pt'])+r''' , & '''+latex(res['k2_pt'])+r'''\end{matrix}\right)$$'''
    ]

def EscribeWeingarten_pt(res):
    return [
        r'''Cálculo de la matriz de Weingarten: aplicando su fórmula, la matriz de Weingarten en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\left[W\right]='''+latex(res['W_pt'], mat_delim='(')+r'''$$'''
    ]

def EscribeDirsPrincipales_pt(res):
    return [
        r'''Cálculo de  autovalores: calculando los autovalores de la matriz de Weingarten, se tiene que las direcciones principales en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ son
$$(\kappa_1, \kappa_2)=\left(\begin{matrix}'''+latex(res['k1_pt'])+r''' , & '''+latex(res['k2_pt'])+r'''\end{matrix}\right)$$''',
        r'''Cálculo del primer autovector: usando el primer autovector, se tiene que el espacio propio asociado a $\kappa_1$ en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\left[W\right]_{\kappa_1} = '''+latex(res['coord_d1_pt'], mat_delim='(')+r'''$$''',
        r'''Cálculo del segundo autovector: usando el segundo autovector, se tiene que el espacio propio asociado a $\kappa_2$ en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$\left[W\right]_{\kappa_2} = '''+latex(res['coord_d2_pt'], mat_delim='(')+r'''$$''',
        r'''Cálculo de las direcciones principales: los autovectores calculados representan las coordenadas de las direcciones principales en la base $\{\varphi_{'''+ latex(res['u']) + r'''}, \varphi_{'''+ latex(res['v']) + r'''}\}$. Por lo tanto se debe hacer un cambio a la base canónica.
$$$$''',
        r'''Cálculo de la primera dirección principal: realizando un cambio de base la primera dirección principal en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$d_1 = '''+latex(res['d1_pt'], mat_delim='(')+r'''$$''',
        r'''Cálculo de la segunda dirección principal: realizando un cambio de base la segunda dirección principal en el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ es
$$d_2 = '''+latex(res['d2_pt'], mat_delim='(')+r'''$$'''
    ]

def EscribePuntosUmbilicos_pt(res):
    if res['umbilico_pt']:
        return [
            r'''Comparación de curvaturas principales: ya que se cumple que $\kappa_1=\kappa_2$, el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ \textbf{es umbílico}
$$$$'''
        ]
    else:
        return [
            r'''Comparación de curvaturas principales: ya que no se cumple que $\kappa_1=\kappa_2$, el punto $\varphi('''+latex(res['u0'])+r''','''+latex(res['v0'])+r''')$ \textbf{no es umbílico}
$$$$'''
        ]
    
def EscribeClasificacionPt(res):
    #TODO: Implementar
    return 
    



'''

import sympy as sp
x, y, z, u, v = sp.symbols('x y z u v', real=True)
resultado ={
  "E_pt": 1,
  "F_pt": 0,
  "G_pt": 1,
  "H_pt": 1,
  "K_pt": 0,
  "W_pt": sp.Matrix([[0, 0], [0, 2]]),
  "coord_d1_pt": sp.Matrix([[0], [1]]),
  "coord_d2_pt": sp.Matrix([[1], [0]]),
  "d1_pt": sp.Matrix([[0, 1, 0]]),
  "d2_pt": sp.Matrix([[1, 0, 0]]),
  "dom_u": sp.Reals,
  "dom_v": sp.Reals,
  "du": sp.Matrix([[1, 0, 0]]),
  "duXdv": sp.Matrix([[0, -2*v, 1]]),
  "duXdv_pt": sp.Matrix([[0, 0, 1]]),
  "du_pt": sp.Matrix([[1, 0, 0]]),
  "duu": sp.Matrix([[0, 0, 0]]),
  "duu_pt": sp.Matrix([[0, 0, 0]]),
  "duv": sp.Matrix([[0, 0, 0]]),
  "duv_pt": sp.Matrix([[0, 0, 0]]),
  "dv": sp.Matrix([[0, 1, 2*v]]),
  "dv_pt": sp.Matrix([[0, 1, 0]]),
  "dvv": sp.Matrix([[0, 0, 2]]),
  "dvv_pt": sp.Matrix([[0, 0, 2]]),
  "e_pt": 0,
  "f_pt": 0,
  "g_pt": 2,
  "k1_pt": 2,
  "k2_pt": 0,
  "norma_pt": 1,
  "normal_pt": sp.Matrix([[0, 0, 1]]),
  "sup": sp.Matrix([[u, v, v**2 + y**2]]),
  "tangente_pt": sp.Eq(z, y**2),
  "u": u,
  "u0": 0,
  "umbilico_pt": False,
  "v": v,
  "v0": 0
}


funcs = [EscribeDerivadasPrimerOrden_pt, EscribeDerivadasSegundoOrden_pt, EscribeProdVect_pt, EscribeNormProdVect_pt, EscribeVectNormal_pt, EscribePlanoTang_pt, EscribePFF_pt, EscribeSegundaFF_pt, EscribeCurvGauss_pt, EscribeCurvMedia_pt, EscribeCurvsPrincipales_pt, EscribeWeingarten_pt, EscribeDirsPrincipales_pt, EscribePuntosUmbilicos_pt]
for func in funcs:
    res = func(resultado)
    for r in res:
        print(r)
    print()
'''
