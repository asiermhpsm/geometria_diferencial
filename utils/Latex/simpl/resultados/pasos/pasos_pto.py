from sympy import latex


def EscribeDerivadas_pt(res):
    return [
        {
            'descripcion' : r'Cálculo de la derivada respecto a $x$: la derivada de $f(x,y,z)$ respecto a $x$ es',
            'paso' : str(res['dx']),
            'pasoLatex' : r'f_x(x,y,z)='+ latex(res['dx'])
        },{
            'descripcion' : r'Sustitución de la derivada respecto a $x$: la derivada de $f(x,y,z)$ respecto a $x$ en el punto $('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')$ es',
            'paso' : str(res['dx_pt']),
            'pasoLatex' : r'f_x('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')='+ latex(res['dx_pt'])
        },{
            'descripcion' : r'Cálculo de la derivada respecto a $y$: la derivada de $f(x,y,z)$ respecto a $y$ es',
            'paso' : str(res['dy']),
            'pasoLatex' : r'f_y(x,y,z)='+ latex(res['dy'])
        },{
            'descripcion' : r'Sustitución de la derivada respecto a $y$: la derivada de $f(x,y,z)$ respecto a $y$ en el punto $('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')$ es',
            'paso' : str(res['dy_pt']),
            'pasoLatex' : r'f_y('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')='+ latex(res['dy_pt'])
        
        },{
            'descripcion' : r'Cálculo de la derivada respecto a $z$: la derivada de $f(x,y,z)$ respecto a $z$ es',
            'paso' : str(res['dz']),
            'pasoLatex' : r'f_z(x,y,z)='+ latex(res['dz'])
        },{
            'descripcion' : r'Sustitución de la derivada respecto a $z$: la derivada de $f(x,y,z)$ respecto a $z$ en el punto $('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')$ es',
            'paso' : str(res['dz_pt']),
            'pasoLatex' : r'f_z('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')='+ latex(res['dz_pt'])
        }
    ]

def EscribeGradiente_pt(res):
    print(res)
    return [
        {
            'descripcion' : r'Cálculo del vector gradiente: el vector gradiente en el punto $('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')$ es',
            'paso' : '',
            'pasoLatex' : r'\nabla f = ' + latex(res['gradiente_pt'])
        }
    ]

def EscribeVectNormal_pt(res):
    return [
        {
            'descripcion' : r'Cálculo del vector normal: aplicando su fórmula, el vector normal en el punto $('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')$ es',
            'paso' : '',
            'pasoLatex' : r'\vec{n} = ' + latex(res['normal_pt'])
        }
    ]

def EscribePlanoTang_pt(res):
    return [
        {
            'descripcion' : r'Cálculo del plano tangente: aplicando su fórmula, el plano tangente en el punto $('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')$ es',
            'paso' : '',
            'pasoLatex' : latex(res['tangente_pt'])
        }
    ]