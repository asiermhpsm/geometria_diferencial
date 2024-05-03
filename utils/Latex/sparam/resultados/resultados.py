from .pasos.pasos import *
from .pasos.pasos_pto import *
from sympy import latex

def saca_dominio(res):
    return r'$\{('+latex(res['u'])+r','+latex(res['v'])+r'): '+latex(res['cond'])+r'\}$' if 'cond' in res else r'$('+latex(res['u'])+r','+latex(res['v'])+r') \in '+latex(res['dom_u'])+r' \times '+latex(res['dom_v']) +r'$'

'''
------------------------------------------------------------------------------------------------------------------------------------------------------
Resultados genéricos
------------------------------------------------------------------------------------------------------------------------------------------------------
'''
def res_analisis_completo(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a realizar un análisis completo en el dominio '+saca_dominio(res)+r' de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden(res) +
        EscribeDerivadasSegundoOrden(res) +
        EscribeProdVect(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect(res) +
        EscribeVectNormal(res) +
        EscribePlanoTang(res) +
        EscribePFF(res) +
        EscribeSFF(res) +
        EscribeWeingarten(res) +
        EscribeDirsPrincipales(res) +
        EscribeCurvGauss(res) +
        EscribeCurvMedia(res) +
        EscribePuntosUmbilicos(res)
    )

def res_curv_Gauss(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular la curvatura de Gauss en el dominio '+saca_dominio(res)+r' de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden(res) +
        EscribeDerivadasSegundoOrden(res) +
        EscribeProdVect(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect(res) +
        EscribeVectNormal(res) +
        EscribePFF(res) +
        EscribeSFF(res) +
        EscribeCurvGauss(res)
    )

def res_curv_media(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular la curvatura media en el dominio '+saca_dominio(res)+r' de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden(res) +
        EscribeDerivadasPrimerOrden(res) +
        EscribeDerivadasSegundoOrden(res) +
        EscribeProdVect(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect(res) +
        EscribeVectNormal(res) +
        EscribePFF(res) +
        EscribeSFF(res) +
        EscribeCurvMedia(res)
    )

def res_curvs_principales(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se van a calcular las curvaturas principales en el dominio '+saca_dominio(res)+r' de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden(res) +
        EscribeDerivadasSegundoOrden(res) +
        EscribeProdVect(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect(res) +
        EscribeVectNormal(res) +
        EscribePFF(res) +
        EscribeSFF(res) +
        EscribeCurvGauss(res) +
        EscribeCurvMedia(res) +
        EscribeCurvsPrincipales(res)
    )

def res_dirs_principales(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se van a calcular las direcciones principales en el dominio '+saca_dominio(res)+r' de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden(res) +
        EscribeDerivadasSegundoOrden(res) +
        EscribeProdVect(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect(res) +
        EscribeVectNormal(res) +
        EscribePFF(res) +
        EscribeSFF(res) +
        EscribeWeingarten(res) +
        EscribeDirsPrincipales(res)
    )

def res_PFF(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular la primera forma fundamental en el dominio '+saca_dominio(res)+r' de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden(res) +
        EscribeProdVect(res) +
        EscribeSupRegular(res) +
        EscribePFF(res)
    )

def res_plano_tangente(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular el plano tangente en el dominio '+saca_dominio(res)+r' de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden(res) +
        EscribeProdVect(res) +
        EscribeSupRegular(res) +
        EscribePlanoTang(res)
    )

def res_ptos_umbilicos(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se van a calcular los puntos umbílicos en el dominio '+saca_dominio(res)+r' de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden(res) +
        EscribeDerivadasSegundoOrden(res) +
        EscribeProdVect(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect(res) +
        EscribeVectNormal(res) +
        EscribePFF(res) +
        EscribeSFF(res) +
        EscribeCurvGauss(res) +
        EscribeCurvMedia(res) +
        EscribeCurvsPrincipales(res) +
        EscribePuntosUmbilicos(res)
    )

def res_SFF(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular la segunda forma fundamental en el dominio '+saca_dominio(res)+r' de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden(res) +
        EscribeDerivadasSegundoOrden(res) +
        EscribeProdVect(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect(res) +
        EscribeVectNormal(res) +
        EscribeSFF(res)
    )

def res_vect_normal(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular el vector normal en el dominio '+saca_dominio(res)+r' de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden(res) +
        EscribeProdVect(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect(res) +
        EscribeVectNormal(res)
    )

def res_Weingarten(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se van a calcular la matriz de Weingarten en el dominio '+saca_dominio(res)+r' de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden(res) +
        EscribeDerivadasSegundoOrden(res) +
        EscribeProdVect(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect(res) +
        EscribeVectNormal(res) +
        EscribePFF(res) +
        EscribeSFF(res) +
        EscribeWeingarten(res)
    )


'''
------------------------------------------------------------------------------------------------------------------------------------------------------
Resultados en puntos
------------------------------------------------------------------------------------------------------------------------------------------------------
'''

def res_analisis_completo_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a realizar un análisis completo en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeDerivadasSegundoOrden_pt(res) +
        EscribeProdVect_pt(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect_pt(res) +
        EscribeVectNormal_pt(res) +
        EscribePlanoTang_pt(res) +
        EscribePFF_pt(res) +
        EscribeSFF_pt(res) +
        EscribeWeingarten_pt(res) +
        EscribeDirsPrincipales_pt(res) +
        EscribeCurvGauss_pt(res) +
        EscribeCurvMedia_pt(res) +
        EscribePuntosUmbilicos_pt(res)
    )

def res_curv_Gauss_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular la curvatura de Gauss en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeDerivadasSegundoOrden_pt(res) +
        EscribeProdVect_pt(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect_pt(res) +
        EscribeVectNormal_pt(res) +
        EscribePFF_pt(res) +
        EscribeSFF_pt(res) +
        EscribeCurvGauss_pt(res)
    )

def res_curv_media_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular la curvatura media en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeDerivadasSegundoOrden_pt(res) +
        EscribeProdVect_pt(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect_pt(res) +
        EscribeVectNormal_pt(res) +
        EscribePFF_pt(res) +
        EscribeSFF_pt(res) +
        EscribeCurvMedia_pt(res)
    )

def res_curvs_principales_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se van a calcular las curvaturas principales en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeDerivadasSegundoOrden_pt(res) +
        EscribeProdVect_pt(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect_pt(res) +
        EscribeVectNormal_pt(res) +
        EscribePFF_pt(res) +
        EscribeSFF_pt(res) +
        EscribeCurvGauss_pt(res) +
        EscribeCurvMedia_pt(res) +
        EscribeCurvsPrincipales_pt(res)
    )

def res_dirs_principales_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se van a calcular las direcciones principales en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeDerivadasSegundoOrden_pt(res) +
        EscribeProdVect_pt(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect_pt(res) +
        EscribeVectNormal_pt(res) +
        EscribePFF_pt(res) +
        EscribeSFF_pt(res) +
        EscribeWeingarten_pt(res) +
        EscribeDirsPrincipales_pt(res)
    )

def res_PFF_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular la primera forma fundamental en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeProdVect_pt(res) +
        EscribeSupRegular(res) +
        EscribePFF_pt(res)
    )

def res_plano_tangente_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular el plano tangente en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeProdVect_pt(res) +
        EscribeSupRegular(res) +
        EscribePlanoTang_pt(res)
    )

def res_ptos_umbilicos_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se van a calcular los puntos umbílicos en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeDerivadasSegundoOrden_pt(res) +
        EscribeProdVect_pt(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect_pt(res) +
        EscribeVectNormal_pt(res) +
        EscribePFF_pt(res) +
        EscribeSFF_pt(res) +
        EscribeCurvGauss_pt(res) +
        EscribeCurvMedia_pt(res) +
        EscribeCurvsPrincipales_pt(res)+
        EscribePuntosUmbilicos_pt(res)
    )

def res_SFF_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular la segunda forma fundamental en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeDerivadasSegundoOrden_pt(res) +
        EscribeProdVect_pt(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect_pt(res) +
        EscribeVectNormal_pt(res) +
        EscribeSFF_pt(res)
    )

def res_vect_normal_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular el vector normal en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeProdVect_pt(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect_pt(res) +
        EscribeVectNormal_pt(res)
    )

def res_Weingarten_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se van a calcular la matriz de Weingarten en el punto $\varphi('+latex(res['u0'])+r','+latex(res['v0'])+r')$ de la superficie parametrizada',
                'paso' : '',
                'pasoLatex' : r'\varphi('+latex(res['u'])+r' ,'+latex(res['v'])+r') = '+latex(res['sup'], mat_delim='(')
            }
        ] +
        EscribeDerivadasPrimerOrden_pt(res) +
        EscribeDerivadasSegundoOrden_pt(res) +
        EscribeProdVect_pt(res) +
        EscribeSupRegular(res) +
        EscribeNormProdVect_pt(res) +
        EscribeVectNormal_pt(res) +
        EscribePFF_pt(res) +
        EscribeSFF_pt(res) +
        EscribeWeingarten_pt(res)
    )







'''
import sympy as sp
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
funcs = [res_analisis_completo, res_curv_Gauss, res_curv_media, res_curvs_principales, res_dirs_principales, res_PFF, res_plano_tangente, res_ptos_umbilicos, res_SFF, res_vect_normal, res_Weingarten]
for f in funcs:
    print(r'\section{Resultados de ' + f.__name__ + r'}')
    res = f(resultado)
    for r in res:
        print(r['descripcion'])
        print('$$'+r['pasoLatex']+'$$')
    print(r'\newpage')


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
funcs = [res_analisis_completo_pt, res_curv_Gauss_pt, res_curv_media_pt, res_curvs_principales_pt, res_dirs_principales_pt, res_PFF_pt, res_plano_tangente_pt, res_ptos_umbilicos_pt, res_SFF_pt, res_vect_normal_pt, res_Weingarten_pt]
for f in funcs:
    print(r'\section{Resultados de ' + f.__name__ + r'}')
    res = f(resultado)
    for i, r in enumerate(res):
        print(f'Paso {i}: '+r['descripcion'])
        print('$$'+r['pasoLatex']+'$$')
    print(r'\newpage')'''