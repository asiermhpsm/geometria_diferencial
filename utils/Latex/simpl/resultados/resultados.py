from .pasos.pasos import *
from .pasos.pasos_pto import *
from sympy import latex


def res_vect_normal(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular el vector normal de la superficie implicita',
                'paso' : '',
                'pasoLatex' : latex(res['sup']) + r' = 0'
            }
        ] +
        EscribeDerivadas(res) +
        EscribeSupNivel(res) +
        EscribeGradiente(res) +
        EscribeVectNormal(res)
    )

def res_plano_tangente(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular el plano tangente de la superficie implicita',
                'paso' : '',
                'pasoLatex' : latex(res['sup']) + r' = 0'
            }
        ] +
        EscribeDerivadas(res) +
        EscribeSupNivel(res) +
        EscribeGradiente(res) +
        EscribePlanoTang(res)
    )

def res_analisis_completo(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a realizar un análisis completo de la superficie implicita',
                'paso' : '',
                'pasoLatex' : latex(res['sup']) + r' = 0'
            }
        ] +
        EscribeDerivadas(res) +
        EscribeSupNivel(res) +
        EscribeGradiente(res) +
        EscribePlanoTang(res) +
        EscribeVectNormal(res)
    )


def res_vect_normal_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular el vector normal en el punto $('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')$ de la superficie implicita',
                'paso' : '',
                'pasoLatex' : latex(res['sup']) + r' = 0'
            }
        ] +
        EscribeDerivadas_pt(res) +
        EscribeSupNivel(res) +
        EscribeGradiente_pt(res) +
        EscribeVectNormal_pt(res)
    )

def res_plano_tangente_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a calcular el plano tangente en el punto $('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')$ de la superficie implicita',
                'paso' : '',
                'pasoLatex' : latex(res['sup']) + r' = 0'
            }
        ] +
        EscribeDerivadas_pt(res) +
        EscribeSupNivel(res) +
        EscribeGradiente_pt(res) +
        EscribePlanoTang_pt(res)
    )

def res_analisis_completo_pt(res):
    return (
        [
            {
                'descripcion' : r'Enunciado: Se va a realizar un análisis completo en el punto $('+latex(res['x0'])+r', '+latex(res['y0'])+r', '+latex(res['z0'])+r')$ de la superficie implicita',
                'paso' : '',
                'pasoLatex' : latex(res['sup']) + r' = 0'
            }
        ] +
        EscribeDerivadas_pt(res) +
        EscribeSupNivel(res) +
        EscribeGradiente_pt(res) +
        EscribePlanoTang_pt(res) +
        EscribeVectNormal_pt(res)
        
    )