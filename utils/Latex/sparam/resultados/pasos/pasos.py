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
            'pasoLatex' : r'\vec{n}=\frac{\vec{\varphi}_u \times \vec{\varphi}_v}{\|\vec{\varphi}_u \times \vec{\varphi}_v\|}='+ latex(res['normal'], mat_delim='(')
        }
    ]

def EscribePlanoTang(res):
    return [
        {
            'descripcion' : r'Cálculo del plano tangente: Aplicando su fórmula $(\vec{\varphi}_u(p) \times \vec{\varphi}_v(p)) \cdot ((x, y, z)-\varphi(p)) = 0$, el plano tangente es',
            'paso' : str(res['tangente']),
            'pasoLatex' : latex(res['tangente'])
        }
    ]

def EscribePFF(res):
    return [
        {
            'descripcion' : r'Cálculo de la primera forma fundamental: aplicando las fórmulas de cada una de sus componentes, la primera forma fundamental es',
            'paso' : '(' + str(res['E']) + ', ' + str(res['F']) + ', ' + str(res['G']) + ')',
            'pasoLatex' : r'\left[I\right]=\left(\begin{matrix} \vec{\varphi}_u \cdot \vec{\varphi}_u & \vec{\varphi}_u \cdot \vec{\varphi}_v \\ \vec{\varphi}_u \cdot \vec{\varphi}_v & \vec{\varphi}_v \cdot \vec{\varphi}_v \end{matrix}\right)=\left(\begin{matrix}'+latex(res['E'])+r' & '+latex(res['F'])+r' \\ '+latex(res['F'])+r' & '+latex(res['G'])+r'\end{matrix}\right)'
        }
    ]

def EscribeSFF(res):
    return [
        {
            'descripcion' : r'Cálculo de la segunda forma fundamental: aplicando las fórmulas de cada una de sus componentes, la segunda forma fundamental es',
            'paso' : '(' + str(res['e']) + ', ' + str(res['f']) + ', ' + str(res['g']) + ')',
            'pasoLatex' : r'\left[II\right]=\left(\begin{matrix} \vec{n}\cdot \vec{\varphi}_{uu} & \vec{n}\cdot \vec{\varphi}_{uv} \\ \vec{n}\cdot \vec{\varphi}_{uv} & \vec{n}\cdot \vec{\varphi}_{vv} \end{matrix}\right)=\left(\begin{matrix}'+latex(res['e'])+r' & '+latex(res['f'])+r' \\ '+latex(res['f'])+r' & '+latex(res['g'])+r'\end{matrix}\right)'
        }
    ]

def EscribeCurvGauss(res):
    return [
        {
            'descripcion' : r'Cálculo de la curvatura de Gauss: aplicando su fórmula, la curvatura de Gauss es',
            'paso' : str(res['K']),
            'pasoLatex' : r'K=\frac{eg-f^2}{EG-F^2}='+latex(res['K'])
        }
    ]

def EscribeCurvMedia(res):
    return [
        {
            'descripcion' : r'Cálculo de la curvatura media: aplicando su fórmula, la curvatura media es',
            'paso' : str(res['H']),
            'pasoLatex' : r'H=\frac{eG+gE-2fF}{2(EG-F^2)}='+latex(res['H'])
        }
    ]

def EscribeCurvsPrincipales(res):
    return [
        {
            'descripcion' : r'Cálculo de las curvaturas principales: aplicando su fórmula, las curvaturas principales son',
            'paso' : '(' + str(res['k1']) + ', ' + str(res['k2']) + ')',
            'pasoLatex' : r'\kappa_1, \kappa_2=H \pm \sqrt{H^2-K}='+latex(res['k1'])+r', '+latex(res['k2'])
        }
    ]

def EscribeWeingarten(res):
    return [
        {
            'descripcion' : r'Cálculo de la matriz de Weingarten: aplicando su fórmula, la matriz de Weingarten es',
            'paso' : str(res['W']),
            'pasoLatex' : r'\left[W\right]=\frac{1}{EG-F^2}\left(\begin{matrix}eG-fF & fG-gF \\ fG-gF & gE-fF\end{matrix}\right)='+latex(res['W'], mat_delim='(')
        }
    ]

def EscribeDirsPrincipales(res):
    return [
        {
            'descripcion' : r'Cálculo de las curvaturas principales: calculando los autovalores de la matriz de Weingarten, las curvaturas principales son',
            'paso' : '(' + str(res['k1']) + ', ' + str(res['k2']) + ')',
            'pasoLatex' : r'\kappa_1, \kappa_2='+latex(res['k1'])+r', '+latex(res['k2'])
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

