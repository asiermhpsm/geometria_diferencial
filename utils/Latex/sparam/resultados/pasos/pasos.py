from sympy import latex


def EscribeDerivadasPrimerOrden(res):
    return [
        {
            'descripcion' : r'Cálculo de la derivada parcial respecto a $'+ latex(res['u']) + r'$: la derivada parcial respecto a $'+ latex(res['u']) + r'$ es',
            'paso' : str(res['du']),
            'pasoLatex' : r'\varphi_{'+ latex(res['u']) + r'}='+ latex(res['du'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo de la derivada parcial respecto a $'+ latex(res['v']) + r'$: la derivada parcial respecto a $'+ latex(res['v']) + r'$ es',
            'paso' : str(res['dv']),
            'pasoLatex' : r'\varphi_{'+ latex(res['v']) + r'}='+ latex(res['dv'], mat_delim='(')
        }
    ]
    
def EscribeDerivadasSegundoOrden(res):
    return [
        {
            'descripcion' : r'Cálculo de la derivada parcial respecto a $'+ latex(res['u'])+latex(res['u']) + r'$: la derivada parcial respecto a $'+ latex(res['u'])+latex(res['u']) + r'$ es',
            'paso' : str(latex(res['duu'], mat_delim='(')),
            'pasoLatex' : r'\varphi_{'+ latex(res['u'])+latex(res['u']) + r'}='+ latex(res['duu'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo de la derivada parcial respecto a $'+ latex(res['u'])+latex(res['v']) + r'$: la derivada parcial respecto a $'+ latex(res['u'])+latex(res['v']) + r'$ es',
            'paso' : str(latex(res['duv'], mat_delim='(')),
            'pasoLatex' : r'\varphi_{'+ latex(res['u'])+latex(res['v']) + r'}='+ latex(res['duv'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo de la derivada parcial respecto a $'+ latex(res['v'])+latex(res['v']) + r'$: la derivada parcial respecto a $'+ latex(res['v'])+latex(res['v']) + r'$ es',
            'paso' : str(latex(res['dvv'], mat_delim='(')),
            'pasoLatex' : r'\varphi_{'+ latex(res['v'])+latex(res['v']) + r'}='+ latex(res['dvv'], mat_delim='(')
        }
    ]

def EscribeProdVect(res):
    return[
        {
            'descripcion' : r'Cálculo del producto vectorial de las derivadas parciales: el producto vectorial de las derivadas parciales de primer orden es',
            'paso' : str(latex(res['duXdv'], mat_delim='(')),
            'pasoLatex' : r'\varphi_{'+ latex(res['u']) + r'}\times\varphi_{'+ latex(res['v']) + r'}='+ latex(res['duXdv'], mat_delim='(')
        }
    ]

def EscribeSupRegular(res):
    return [
        {
            'descripcion' : r'Comprobación de superficie regular: asumiendo que la superficie es suave, la superficie es regular ya que se cumple que $\varphi_{'+ latex(res['u']) + r'}\times\varphi_{'+ latex(res['v']) + r'}\neq 0$ para todo $('+ latex(res['u']) + r','+ latex(res['v']) + r')\in'+ latex(res['dom_u']) + r'\times'+ latex(res['dom_v']) + r'$',
            'paso' : '',
            'pasoLatex' : ''
        }
    ]

def EscribeNormProdVect(res):
    return [
        {
            'descripcion' : r'Cálculo de la norma del producto vectorial: la norma del producto vectorial de las derivadas parciales de primer orden es',
            'paso' : str(res['norma']),
            'pasoLatex' : r'\|\varphi_{'+ latex(res['u']) + r'}\times\varphi_{'+ latex(res['v']) + r'}\|='+ latex(res['norma'])
        }
    ]

def EscribeVectNormal(res):
    return [
        {
            'descripcion' : r'Aplicación de la fórmula del vector normal: aplicando su fórmula, el vector normal es',
            'paso' : str(res['normal']),
            'pasoLatex' : r'\Vec{n}='+ latex(res['normal'], mat_delim='(')
        }
    ]

def EscribePlanoTang(res):
    return [
        {
            'descripcion' : r'Cálculo del plano tangente: Aplicando su fórmula, el plano afín tangente es',
            'paso' : str(res['tangente']),
            'pasoLatex' : latex(res['tangente'])
        }
    ]

def EscribePFF(res):
    return [
        {
            'descripcion' : r'Cálculo de la primera forma fundamental: aplicando las fórmulas de cada una de sus componenetes, la primera forma fundamental es',
            'paso' : '(' + str(res['E']) + ', ' + str(res['F']) + ', ' + str(res['G']) + ')',
            'pasoLatex' : r'\left[I\right]=\left(\begin{matrix}'+latex(res['E'])+r' & '+latex(res['F'])+r' \\ '+latex(res['F'])+r' & '+latex(res['G'])+r'\end{matrix}\right)'
        }
    ]

def EscribeSFF(res):
    return [
        {
            'descripcion' : r'Cálculo de la segunda forma fundamental: aplicando las fórmulas de cada una de sus componenetes, la segunda forma fundamental es',
            'paso' : '(' + str(res['e']) + ', ' + str(res['f']) + ', ' + str(res['g']) + ')',
            'pasoLatex' : r'\left[II\right]=\left(\begin{matrix}'+latex(res['e'])+r' & '+latex(res['f'])+r' \\ '+latex(res['f'])+r' & '+latex(res['g'])+r'\end{matrix}\right)'
        }
    ]

def EscribeCurvGauss(res):
    return [
        {
            'descripcion' : r'Cálculo de la curvatura de Gauss: aplicando su fórmula, la curvatura de Gauss es',
            'paso' : str(res['K']),
            'pasoLatex' : r'K='+latex(res['K'])
        }
    ]

def EscribeCurvMedia(res):
    return [
        {
            'descripcion' : r'Cálculo de la curvatura media: aplicando su fórmula, la curvatura media es',
            'paso' : str(res['H']),
            'pasoLatex' : r'H='+latex(res['H'])
        }
    ]

def EscribeCurvsPrincipales(res):
    return [
        {
            'descripcion' : r'Cálculo de las curvaturas principales: aplicando su fórmula, las curvaturas principales son',
            'paso' : '(' + str(res['k1']) + ', ' + str(res['k2']) + ')',
            'pasoLatex' : r'(\kappa_1, \kappa_2)=\left(\begin{matrix}'+latex(res['k1'])+r' & '+latex(res['k2'])+r'\end{matrix}\right)'
        }
    ]

def EscribeWeingarten(res):
    return [
        {
            'descripcion' : r'Cálculo de la matriz de Weingarten: aplicando su fórmula, la matriz de Weingarten es',
            'paso' : str(res['W']),
            'pasoLatex' : r'\left[W\right]='+latex(res['W'], mat_delim='(')
        }
    ]

def EscribeDirsPrincipales(res):
    return [
        {
            'descripcion' : r'Cálculo de las curvaturas principales: calculando los autovalores de la matriz de Weingarten, las curvaturas principales son',
            'paso' : '(' + str(res['k1']) + ', ' + str(res['k2']) + ')',
            'pasoLatex' : r'(\kappa_1, \kappa_2)=\left(\begin{matrix}'+latex(res['k1'])+r' & '+latex(res['k2'])+r'\end{matrix}\right)'
        },{
            'descripcion' : r'Cálculo del primer autovector: usando el primer autovector, se tiene que el espacio propio asociado a $\kappa_1$ es',
            'paso' : str(res['coord_d1']),
            'pasoLatex' : r'\left[W\right]_{\kappa_1}='+latex(res['coord_d1'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo del segundo autovector: usando el segundo autovector, se tiene que el espacio propio asociado a $\kappa_2$ es',
            'paso' : str(res['coord_d2']),
            'pasoLatex' : r'\left[W\right]_{\kappa_2}='+latex(res['coord_d2'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo de las direcciones principales: los autovectores calculados representan las coordenadas de las direcciones principales en la base $\{\varphi_{'+ latex(res['u']) + r'}, \varphi_{'+ latex(res['v']) + r'}\}$. Por lo tanto se debe hacer un cambio a la base canónica.',
            'paso' : '',
            'pasoLatex' : ''
        },{
            'descripcion' : r'Cálculo de la primera dirección principal: realizando un cambio de base la primera dirección principal es',
            'paso' : str(res['d1']),
            'pasoLatex' : r'd_1='+latex(res['d1'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo de la segunda dirección principal: realizando un cambio de base la segunda dirección principal es',
            'paso' : str(res['d2']),
            'pasoLatex' : r'd_2='+latex(res['d2'], mat_delim='(')
        }
    ]

def EscribePuntosUmbilicos(res):
    ptos_uv = r'\{'
    ptos_sup = r'\{'
    for ui, vi in res['umbilico']:
        ptos_uv = ptos_uv + f'({latex(ui)},{latex(vi)}), '
        ptos_sup = ptos_sup + latex(res['sup'].subs({res['u']: ui, res['v']: vi}), mat_delim='(') + ', '
    ptos_uv = ptos_uv.strip(', ') + r'\}'
    ptos_sup = ptos_sup.strip(', ') + r'\}'
    return [
        {
            'descripcion' : r'Cálculo de puntos con curvaturas iguales: resolviendo la ecuación $\kappa_1=\kappa_2$, las curvaturas principales son iguales cuando',
            'paso' : ptos_uv,
            'pasoLatex' : r'('+latex(res['u'])+r', '+latex(res['v'])+r')\in '+ptos_uv
        },
        {
            'descripcion' : r'Cálculo de los puntos umbílicos: sustituyendo el resultado anterior en la superficie, los puntos umbílicos son aquellos de la forma',
            'paso' : ptos_sup,
            'pasoLatex' : r'(x,y,z))\in '+ptos_sup
        }
    ]




"""import sympy as sp
u, v, = sp.symbols('u v', real=True)
x, y, z = sp.symbols('x y z', real=True)
resultado = {
  "E": 4*u**2 + 1,
  "F": 4*u*v,
  "G": 4*v**2 + 1,
  "H": 2*(2*u**2 + 2*v**2 + 1)/(4*u**2 + 4*v**2 + 1)**(3/2),
  "K": 4/(16*u**4 + 32*u**2*v**2 + 8*u**2 + 16*v**4 + 8*v**2 + 1),
  "W": sp.Matrix([[2*(4*v**2 + 1)/(4*u**2 + 4*v**2 + 1)**(3/2), -8*u*v/(4*u**2 + 4*v**2 + 1)**(3/2)], [-8*u*v/(4*u**2 + 4*v**2 + 1)**(3/2), 2*(4*u**2 + 1)/(4*u**2 + 4*v**2 + 1)**(3/2)]]),
  "coord_d1": sp.Matrix([[2*u*v*(4*u**2 + 4*v**2 + 1)/(-4*u**4 - u**2 + 4*v**4 + v**2 + sp.sqrt(16*u**8 + 64*u**6*v**2 + 8*u**6 + 96*u**4*v**4 + 24*u**4*v**2 + u**4 + 64*u**2*v**6 + 24*u**2*v**4 + 2*u**2*v**2 + 16*v**8 + 8*v**6 + v**4))], [1]]),
  "coord_d2": sp.Matrix([[2*u*v*(-4*u**2 - 4*v**2 - 1)/(4*u**4 + u**2 - 4*v**4 - v**2 + sp.sqrt(16*u**8 + 64*u**6*v**2 + 8*u**6 + 96*u**4*v**4 + 24*u**4*v**2 + u**4 + 64*u**2*v**6 + 24*u**2*v**4 + 2*u**2*v**2 + 16*v**8 + 8*v**6 + v**4))], [1]]),
  "d1": sp.Matrix([[2*u*v*(4*u**2 + 4*v**2 + 1)/(-4*u**4 - u**2 + 4*v**4 + v**2 + sp.sqrt(16*u**8 + 64*u**6*v**2 + 8*u**6 + 96*u**4*v**4 + 24*u**4*v**2 + u**4 + 64*u**2*v**6 + 24*u**2*v**4 + 2*u**2*v**2 + 16*v**8 + 8*v**6 + v**4)), 1, 4*u**2*v*(4*u**2 + 4*v**2 + 1)/(-4*u**4 - u**2 + 4*v**4 + v**2 + sp.sqrt(16*u**8 + 64*u**6*v**2 + 8*u**6 + 96*u**4*v**4 + 24*u**4*v**2 + u**4 + 64*u**2*v**6 + 24*u**2*v**4 + 2*u**2*v**2 + 16*v**8 + 8*v**6 + v**4)) + 2*v]]),
  "d2": sp.Matrix([[-2*u*v*(4*u**2 + 4*v**2 + 1)/(4*u**4 + u**2 - 4*v**4 - v**2 + sp.sqrt(16*u**8 + 64*u**6*v**2 + 8*u**6 + 96*u**4*v**4 + 24*u**4*v**2 + u**4 + 64*u**2*v**6 + 24*u**2*v**4 + 2*u**2*v**2 + 16*v**8 + 8*v**6 + v**4)), 1, -4*u**2*v*(4*u**2 + 4*v**2 + 1)/(4*u**4 + u**2 - 4*v**4 - v**2 + sp.sqrt(16*u**8 + 64*u**6*v**2 + 8*u**6 + 96*u**4*v**4 + 24*u**4*v**2 + u**4 + 64*u**2*v**6 + 24*u**2*v**4 + 2*u**2*v**2 + 16*v**8 + 8*v**6 + v**4)) + 2*v]]),
  "dom_u": sp.Interval.open(-2, 2),
  "dom_v": sp.Interval.open(-2, 2),
  "du": sp.Matrix([[1, 0, 2*u]]),
  "duXdv": sp.Matrix([[-2*u, -2*v, 1]]),
  "duu": sp.Matrix([[0, 0, 2]]),
  "duv": sp.Matrix([[0, 0, 0]]),
  "dv": sp.Matrix([[0, 1, 2*v]]),
  "dvv": sp.Matrix([[0, 0, 2]]),
  "e": 2/sp.sqrt(4*u**2 + 4*v**2 + 1),
  "f": 0,
  "g": 2/sp.sqrt(4*u**2 + 4*v**2 + 1),
  "k1": sp.sqrt(4*(2*u**2 + 2*v**2 + 1)**2/(4*u**2 + 4*v**2 + 1)**3 - 4/(16*u**4 + 32*u**2*v**2 + 8*u**2 + 16*v**4 + 8*v**2 + 1)) + 2*(2*u**2 + 2*v**2 + 1)/(4*u**2 + 4*v**2 + 1)**(3/2),
  "k2": -sp.sqrt(4*(2*u**2 + 2*v**2 + 1)**2/(4*u**2 + 4*v**2 + 1)**3 - 4/(16*u**4 + 32*u**2*v**2 + 8*u**2 + 16*v**4 + 8*v**2 + 1)) + 2*(2*u**2 + 2*v**2 + 1)/(4*u**2 + 4*v**2 + 1)**(3/2),
  "norma": sp.sqrt(4*u**2 + 4*v**2 + 1),
  "normal": sp.Matrix([[-2*u/sp.sqrt(4*u**2 + 4*v**2 + 1), -2*v/sp.sqrt(4*u**2 + 4*v**2 + 1), 1/sp.sqrt(4*u**2 + 4*v**2 + 1)]]),
  "sup": sp.Matrix([[u, v, u**2 + v**2]]),
  "tangente": sp.Eq(u**2 + v**2, 2*u*x + 2*v*y - z),
  "u": u,
  "umbilico": {(0, v)},
  "v": v
}


funcs = [EscribeDerivadasPrimerOrden, EscribeDerivadasSegundoOrden, EscribeProdVect, EscribeSupRegular, EscribeNormProdVect, EscribeSupRegular, EscribeVectNormal, EscribePlanoTang, EscribePFF, EscribeSFF, EscribeCurvGauss, EscribeCurvMedia, EscribeCurvsPrincipales, EscribeWeingarten, EscribeDirsPrincipales, EscribePuntosUmbilicos]
for f in funcs:
    print(r'\section{Resultados de ' + f.__name__ + r'}')
    res = f(resultado)
    for r in res:
        print(r['descripcion'])
        print('$$'+r['pasoLatex']+'$$')
    print(r'\newpage')"""