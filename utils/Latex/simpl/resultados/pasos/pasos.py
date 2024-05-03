from sympy import latex


def EscribeDerivadas(res):
    return [
        {
            'descripcion' : r'Cálculo de la derivada respecto a $x$: la derivada de $f(x,y,z)$ respecto a $x$ es',
            'paso' : str(res['dx']),
            'pasoLatex' : r'f_x(x,y,z)='+ latex(res['dx'])
        },{
            'descripcion' : r'Cálculo de la derivada respecto a $y$: la derivada de $f(x,y,z)$ respecto a $y$ es',
            'paso' : str(res['dy']),
            'pasoLatex' : r'f_y(x,y,z)='+ latex(res['dy'])
        },{
            'descripcion' : r'Cálculo de la derivada respecto a $z$: la derivada de $f(x,y,z)$ respecto a $z$ es',
            'paso' : str(res['dz']),
            'pasoLatex' : r'f_z(x,y,z)='+ latex(res['dz'])
        }
    ]

def EscribeSupNivel(res):
    return [
        {
            'descripcion' : r'Comprobar que es superficie de nivel: se trata de una superficie de nivel ya que el siguiente sistema no tiene solución real:',
            'paso' : '',
            'pasoLatex' : r'\left\{ \begin{array}{rcl} '+latex(res['sup'])+r' & = & 0 \\ '+latex(res['dx'])+r' & = & 0 \\ '+latex(res['dy'])+r' & = & 0 \\ '+latex(res['dz'])+r' & = & 0 \end{array} \right.'
        }
    ]

def EscribeGradiente(res):
    return [
        {
            'descripcion' : r'Cálculo del vector gradiente: el vector gradiente es',
            'paso' : '',
            'pasoLatex' : r'\nabla f = ' + latex(res['gradiente'])
        }
    ]

def EscribeVectNormal(res):
    return [
        {
            'descripcion' : r'Cálculo del vector normal: aplicando su fórmula, el vector normal es',
            'paso' : '',
            'pasoLatex' : r'\vec{n} = ' + latex(res['normal'])
        }
    ]

def EscribePlanoTang(res):
    return [
        {
            'descripcion' : r'Cálculo del plano tangente: aplicando su fórmula, el plano tangente es',
            'paso' : '',
            'pasoLatex' : latex(res['tangente'])
        }
    ]