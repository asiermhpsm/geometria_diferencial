from sympy import latex

def EscribeDerivadasPrimerOrden_pt(res):
    return [
        {
            'descripcion' : r'Cálculo de la derivada parcial respecto a $'+ latex(res['u']) + r'$: la derivada parcial respecto a $'+ latex(res['u']) + r'$ es',
            'paso' : str(res['du']),
            'pasoLatex' : r'\varphi_{'+ latex(res['u']) + r'}='+ latex(res['du'], mat_delim='(')
        },{
            'descripcion' : r'Sustitución en el punto de la derivada parcial respecto a $'+ latex(res['u']) + r'$: la derivada parcial respecto a $'+ latex(res['u']) + r'$ en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['du_pt']),
            'pasoLatex' : r'\varphi_{'+ latex(res['u']) + r'}('+latex(res['u0'])+','+latex(res['v0'])+')='+ latex(res['du_pt'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo de la derivada parcial respecto a $'+ latex(res['v']) + r'$: la derivada parcial respecto a $'+ latex(res['v']) + r'$ es',
            'paso' : str(res['dv']),
            'pasoLatex' : r'\varphi_{'+ latex(res['v']) + r'}='+ latex(res['dv'], mat_delim='(')
        },{
            'descripcion' : r'Sustitución en el punto de la derivada parcial respecto a $'+ latex(res['v']) + r'$: la derivada parcial respecto a $'+ latex(res['v']) + r'$ en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['dv_pt']),
            'pasoLatex' : r'\varphi_{'+ latex(res['v']) + r'}('+latex(res['u0'])+','+latex(res['v0'])+')='+ latex(res['dv_pt'], mat_delim='(')
        }
    ]

def EscribeDerivadasSegundoOrden_pt(res):
    return [
        {
            'descripcion' : r'Cálculo de la derivada parcial respecto a $'+ latex(res['u'])+latex(res['u']) + r'$: la derivada parcial respecto a $'+ latex(res['u'])+latex(res['u']) + r'$ es',
            'paso' : str(res['duu']),
            'pasoLatex' : r'\varphi_{'+ latex(res['u'])+latex(res['u']) + r'}='+ latex(res['duu'], mat_delim='(')
        },{
            'descripcion' : r'Sustitución en el punto de la derivada parcial respecto a $'+ latex(res['u'])+latex(res['u']) + r'$: la derivada parcial respecto a $'+ latex(res['u'])+latex(res['u']) + r'$ en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['duu_pt']),
            'pasoLatex' : r'\varphi_{'+ latex(res['u'])+latex(res['u']) + r'}('+latex(res['u0'])+','+latex(res['v0'])+')='+ latex(res['duu_pt'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo de la derivada parcial respecto a $'+ latex(res['u'])+latex(res['v']) + r'$: la derivada parcial respecto a $'+ latex(res['u'])+latex(res['v']) + r'$ es',
            'paso' : str(res['duv']),
            'pasoLatex' : r'\varphi_{'+ latex(res['u'])+latex(res['v']) + r'}='+ latex(res['duv'], mat_delim='(')
        },{
            'descripcion' : r'Sustitución en el punto de la derivada parcial respecto a $'+ latex(res['u'])+latex(res['v']) + r'$: la derivada parcial respecto a $'+ latex(res['u'])+latex(res['v']) + r'$ en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['duv_pt']),
            'pasoLatex' : r'\varphi_{'+ latex(res['u'])+latex(res['v']) + r'}('+latex(res['u0'])+','+latex(res['v0'])+')='+ latex(res['duv_pt'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo de la derivada parcial respecto a $'+ latex(res['v'])+latex(res['v']) + r'$: la derivada parcial respecto a $'+ latex(res['v'])+latex(res['v']) + r'$ es',
            'paso' : str(res['dvv']),
            'pasoLatex' : r'\varphi_{'+ latex(res['v'])+latex(res['v']) + r'}='+ latex(res['dvv'], mat_delim='(')
        },{
            'descripcion' : r'Sustitución en el punto de la derivada parcial respecto a $'+ latex(res['v'])+latex(res['v']) + r'$: la derivada parcial respecto a $'+ latex(res['v'])+latex(res['v']) + r'$ en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['dvv_pt']),
            'pasoLatex' : r'\varphi_{'+ latex(res['v'])+latex(res['v']) + r'}('+latex(res['u0'])+','+latex(res['v0'])+')='+ latex(res['dvv_pt'], mat_delim='(')
        }
    ]

def EscribeProdVect_pt(res):
    return [
        {
            'descripcion' : r'Cálculo del producto vectorial de las derivadas parciales: el producto vectorial de las derivadas parciales de primer orden en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['duXdv_pt']),
            'pasoLatex' : r'\varphi_{'+ latex(res['u']) + r'}\times\varphi_{'+ latex(res['v']) + r'}='+ latex(res['duXdv_pt'], mat_delim='(')
        }
    ]

def EscribeNormProdVect_pt(res):
    return [
        {
            'descripcion' : r'Cálculo de la norma del producto vectorial: la norma del producto vectorial de las derivadas parciales de primer orden en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['norma_pt']),
            'pasoLatex' : r'\|\varphi_{'+ latex(res['u']) + r'}\times\varphi_{'+ latex(res['v']) + r'}\|='+ latex(res['norma_pt'])
        }
    ]

def EscribeVectNormal_pt(res):
    return [
        {
            'descripcion' : r'Aplicación de la fórmula del vector normal: aplicando su fórmula, el vector normal en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['normal_pt']),
            'pasoLatex' : r'\Vec{n}='+ latex(res['normal_pt'], mat_delim='(')
        }
    ]

def EscribePlanoTang_pt(res):
    return [
        {
            'descripcion' : r'Cálculo del plano tangente: aplicando su fórmula, el plano afín tangente en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['tangente_pt']),
            'pasoLatex' : latex(res['tangente_pt'])
        }
    ]

def EscribePFF_pt(res):
    return [
        {
            'descripcion' : r'Cálculo de la primera forma fundamental: aplicando las fórmulas de cada una de sus componenetes, la primera forma fundamental en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : '(' + str(res['E_pt']) + ', ' + str(res['F_pt']) + ', ' + str(res['G_pt']) + ')',
            'pasoLatex' : r'\left[I\right]=\left(\begin{matrix}'+latex(res['E_pt'])+r' & '+latex(res['F_pt'])+r' \\ '+latex(res['F_pt'])+r' & '+latex(res['G_pt'])+r'\end{matrix}\right)'
        }
    ]

def EscribeSFF_pt(res):
    return [
        {
            'descripcion' : r'Cálculo de la segunda forma fundamental: aplicando las fórmulas de cada una de sus componenetes, la segunda forma fundamental en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : '(' + str(res['e_pt']) + ', ' + str(res['f_pt']) + ', ' + str(res['g_pt']) + ')',
            'pasoLatex' : r'\left[II\right]=\left(\begin{matrix}'+latex(res['e_pt'])+r' & '+latex(res['f_pt'])+r' \\ '+latex(res['f_pt'])+r' & '+latex(res['g_pt'])+r'\end{matrix}\right)'
        }
    ]

def EscribeCurvGauss_pt(res):
    return [
        {
            'descripcion' : r'Cálculo de la curvatura de Gauss: aplicando su fórmula, la curvatura de Gauss en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['K_pt']),
            'pasoLatex' : r'K='+ latex(res['K_pt'])
        }
    ]

def EscribeCurvMedia_pt(res):
    return [
        {
            'descripcion' : r'Cálculo de la curvatura media: aplicando su fórmula, la curvatura media en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['H_pt']),
            'pasoLatex' : r'H='+ latex(res['H_pt'])
        }
    ]

def EscribeCurvsPrincipales_pt(res):
    return [
        {
            'descripcion' : r'Cálculo de las curvaturas principales: aplicando su fórmula, las curvaturas principales en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ son',
            'paso' : '(' + str(res['k1_pt']) + ', ' + str(res['k2_pt']) + ')',
            'pasoLatex' : r'(\kappa_1, \kappa_2)=\left(\begin{matrix}'+latex(res['k1_pt'])+r' , & '+latex(res['k2_pt'])+r'\end{matrix}\right)'
        }
    ]

def EscribeWeingarten_pt(res):
    return [
        {
            'descripcion' : r'Cálculo de la matriz de Weingarten: aplicando su fórmula, la matriz de Weingarten en el punto $\varphi('+latex(res['u0'])+','+latex(res['v0'])+')$ es',
            'paso' : str(res['W_pt']),
            'pasoLatex' : r'\left[W\right]='+ latex(res['W_pt'], mat_delim='(')
        }
    ]

def EscribeDirsPrincipales_pt(res):
    return [
        {
            'descripcion' : r'Cálculo de  autovalores: calculando los autovalores de la matriz de Weingarten, se tiene que las direcciones principales en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ son',
            'paso' : '(' + str(res['k1_pt']) + ', ' + str(res['k2_pt']) + ')',
            'pasoLatex' : r'(\kappa_1, \kappa_2)=\left(\begin{matrix}'+latex(res['k1_pt'])+r' , & '+latex(res['k2_pt'])+r'\end{matrix}\right)'
        },{
            'descripcion' : r'Cálculo del primer autovector: usando el primer autovector, se tiene que el espacio propio asociado a $\kappa_1$ en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ es',
            'paso' : str(res['coord_d1_pt']),
            'pasoLatex' : r'\left[W\right]_{\kappa_1} = '+ latex(res['coord_d1_pt'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo del segundo autovector: usando el segundo autovector, se tiene que el espacio propio asociado a $\kappa_2$ en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ es',
            'paso' : str(res['coord_d2_pt']),
            'pasoLatex' : r'\left[W\right]_{\kappa_2} = '+ latex(res['coord_d2_pt'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo de las direcciones principales: los autovectores calculados representan las coordenadas de las direcciones principales en la base $\{\varphi_{'+ latex(res['u']) + r'}, \varphi_{'+ latex(res['v']) + r'}\}$. Por lo tanto se debe hacer un cambio a la base canónica.',
            'paso' : '',
            'pasoLatex' : ''
        },{
            'descripcion' : r'Cálculo de la primera dirección principal: realizando un cambio de base la primera dirección principal en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ es',
            'paso' : str(res['d1_pt']),
            'pasoLatex' : r'd_1 = '+ latex(res['d1_pt'], mat_delim='(')
        },{
            'descripcion' : r'Cálculo de la segunda dirección principal: realizando un cambio de base la segunda dirección principal en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ es',
            'paso' : str(res['d2_pt']),
            'pasoLatex' : r'd_2 = '+ latex(res['d2_pt'], mat_delim='(')
        }
    ]

def EscribePuntosUmbilicos_pt(res):
    if res['umbilico_pt']:
        return [
            {
                'descripcion' : r'Comparación de curvaturas principales: ya que se cumple que $\kappa_1=\kappa_2$, el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ es umbílico',
                'paso' : '',
                'pasoLatex' : ''
            }
        ]
    else:
        return [
            {
                'descripcion' : r'Comparación de curvaturas principales: ya que no se cumple que $\kappa_1=\kappa_2$, el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ no es umbílico',
                'paso' : '',
                'pasoLatex' : ''
            }
        ]
    
def EscribeClasificacionPt(res):
    if res['clasif_pt'] == 'Eliptico':
        return [
            {
                'descripcion' : r'Clasificación del punto: ya que $\kappa_1 \kappa_2 > 0$, el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ es un punto elíptico',
                'paso' : '',
                'pasoLatex' : ''
            }
        ]
    elif res['clasif_pt'] == 'Hiperbolico':
        return [
            {
                'descripcion' : r'Clasificación del punto: ya que $\kappa_1 \kappa_2 < 0$, el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ es un punto hiperbólico',
                'paso' : '',
                'pasoLatex' : ''
            }
        ]
    elif res['clasif_pt'] == 'Planar':
        return [
            {
                'descripcion' : r'Clasificación del punto: ya que $\kappa_1 \kappa_2 = 0$ y $\kappa_1 = \kappa_2$, el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ es un punto planar',
                'paso' : '',
                'pasoLatex' : ''
            }
        ]
    else:
        return [
            {
                'descripcion' : r'Clasificación del punto: ya que $\kappa_1 \kappa_2 = 0$ y $\kappa_1 \neq \kappa_2$, el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ es un punto parabólico',
                'paso' : '',
                'pasoLatex' : ''
            }
        ]

def EscribeDireccionesAsintóticasPt(res):
    dirs = ''
    for dir in res['Dirs_asint']:
        dirs += latex(dir, mat_delim='(') + r', '
    dirs = dirs.strip(', ')
    if res['e_pt']==0 and res['f_pt']==0 and res['g_pt']==0:
        return [
            {
                'descripcion' : r'Calcular las direcciones principales: buscando los vectores que cumplan que $II( \vec{w}, \vec{w})=0$ se tiene que \textbf{todas las direcciones son asintóticas}',
                'paso' : str(res['Dirs_asint']),
                'pasoLatex' : ''
            }
        ]
    elif res['e_pt']==0 or res['g_pt']==0:
        return [
            {
                'descripcion' : r'Calcular las direcciones principales: buscando los vectores que cumplan que $II( \vec{w}, \vec{w})=0$ se tiene que las direcciones asintóticas son',
                'paso' : str(res['Dirs_asint']),
                'pasoLatex' : r'\{'+dirs+r' \}'
            }
        ]
    elif res['f_pt']**2- res['g_pt']*res['e_pt'] < 0:
        return [
            {
                'descripcion' : r'Calcular las direcciones principales: buscando los vectores que cumplan que $II( \vec{w}, \vec{w})=0$ se tiene que no existen direcciones asintóticas',
                'paso' : str(res['Dirs_asint']),
                'pasoLatex' : ''
            }
        ]
    else:
        return [
            {
                'descripcion' : r'Calcular las direcciones principales: buscando los vectores que cumplan que $II( \vec{w}, \vec{w})=0$ se tiene que las direcciones asintóticas son',
                'paso' : str(res['Dirs_asint']),
                'pasoLatex' : r'\{'+dirs+r' \}'
            }
        ]
    




"""
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


funcs = [EscribeDerivadasPrimerOrden_pt, EscribeDerivadasSegundoOrden_pt, EscribeProdVect_pt, EscribeNormProdVect_pt, EscribeVectNormal_pt, EscribePlanoTang_pt, EscribePFF_pt, EscribeSFF_pt, EscribeCurvGauss_pt, EscribeCurvMedia_pt, EscribeCurvsPrincipales_pt, EscribeWeingarten_pt, EscribeDirsPrincipales_pt, EscribePuntosUmbilicos_pt]
for f in funcs:
    print(r'\section{Resultados de ' + f.__name__ + r'}')
    res = f(resultado)
    for r in res:
        print(r['descripcion'])
        print('$$'+r['pasoLatex']+'$$')
    print(r'\newpage')
"""
