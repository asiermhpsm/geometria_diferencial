from flask import Flask, request, jsonify
import dash
from dash import Dash, html, dcc
import json

import sympy as sp
import numpy as np
import re

import plotly.graph_objects as go

from utils import *
from utils_graph_plotly import *


"""
-------------------------------------------------------------------------------
FUNCIONES AUXILIARES Y ATRIBUTOS GENERALES
-------------------------------------------------------------------------------
"""
OPCIONES_VAR = ['infinite', 'finite', 'real', 'extended_real', 'rational', 'irrational', 
                 'integer', 'noninteger', 'even', 'odd', 'prime', 'composite', 
                 'zero', 'nonzero', 'extended_nonzero', 'positive', 'nonnegative', 
                 'negative', 'nonpositive', 'extended_positive', 'extended_nonnegative',
                 'extended_negative', 'extended_nonpositive']

def procesar_solicitud(func, func_pt_uv, func_pt_xyz):
    """
    Procesa una solicitud
    """
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')
    const_str = request.args.getlist('const')
    func_str = request.args.getlist('func')
    
    if not superficie_str:
        # TODO: Devolver teoría
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str, const_str, func_str)
    except Exception as e:
        # TODO: ¿Qué hacer si hay un error?
        raise e
    
    resultados = {}

    #TODO- comprobar que punto es numerico
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        func_pt_uv(superficie, u, v, u0, v0, resultados)
        return convertir_a_string(resultados)

    #TODO- comprobar que punto es numerico
    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        func_pt_xyz(superficie, u, v, x0, y0, z0, resultados)
        return convertir_a_string(resultados)
    
    func(superficie, u, v, resultados)
    return convertir_a_string(resultados)

def normaliza_parametrizacion(var1, var2, sup, consts, funcs):
    """
    Transforma la parametrización de una superficie a una expresion sympy con sus variable correspondientes
    No se hacen comprobaciones de tipo

    Argumentos:
    var1                string con la primera variable de la parametrización
    var2                string con la segunda variable de la parametrización
    sup                 string con la parametrización de la superficie
    consts              lista de strings con constantes y su descripción
    func                lista de strings con funciones y su descripción
    """
    variables = {}

    opciones = {}
    if not var1:
        var1='u'
    elif '[' in var1:
        var1, opciones = extrae_opciones_var(var1)
    opciones['real'] = True
    u = sp.symbols(var1.replace(' ', ''), **opciones)
    variables[var1] = u

    opciones = {}
    if not var2:
        var2='v'
    elif '[' in var2:
        var2, opciones = extrae_opciones_var(var2)
    opciones['real'] = True
    v = sp.symbols(var2.replace(' ', ''), **opciones)
    variables[var2] = v

    #https://docs.sympy.org/latest/guides/assumptions.html#predicates
    #https://docs.sympy.org/latest/modules/core.html#module-sympy.core.assumptions
    for const in consts:
        nombre, opciones = extrae_opciones_var(const)
        opciones['real'] = True
        variables[nombre] = sp.symbols(nombre, **opciones)
    
    for func in funcs:
        if '(' not in func or ')' not in func:
            raise Exception(f'No se ha podido procesar las variables de las que depende {func}')
        partes  = func.replace(' ', '').strip('[]').split(')')
        definicion_func = list(re.split(r'[(),]', partes[0]))
        nombre_func = definicion_func[0]
        variables_func = [variables[var] for var in definicion_func[1:]]
        descripciones = partes[1].split(',')
        descripciones_dict = {}
        for descripcion in descripciones:
            if descripcion in OPCIONES_VAR:
                descripciones_dict[descripcion] = True
        descripciones_dict['real'] = True
        variables[nombre_func] = sp.Function(nombre_func, **descripciones_dict)(*variables_func)
        sup = re.sub(nombre_func+r'\(([\w,]+)\)', nombre_func, sup)

    try:
        superficie = extrae_superficie(sup.strip('[] '))
    except Exception as e:
        raise Exception(f"Error al procesar la superficie: {e}")
    
    if isinstance(superficie, list):
        return sp.Matrix([sp.sympify(elem, locals=variables) for elem in superficie]), u, v
    else:
        return sp.sympify(superficie, locals=variables), u, v
    
def extrae_opciones_var(string):
    partes  = string.replace(' ', '').strip('[]').split(',')
    opciones_dict = {}
    for opcion in partes[1:]:
        if opcion in OPCIONES_VAR:
            opciones_dict[opcion] = True
    return partes[0], opciones_dict

def extrae_superficie(string):
    string.replace(' ', '')
    coincidencias_lista = re.match(r'\[([^,\[\]]*),\s*([^,\[\]]*),\s*([^,\[\]]*)\]', string)
    if coincidencias_lista:
        return [coincidencias_lista.group(1), coincidencias_lista.group(2), coincidencias_lista.group(3)]
    else:
        if '[' in string or ']' in string:
            raise Exception(f"Error al procesar la superficie: {string}")
        return string

def sympy2latex(diccionario):
    return {k: sp.latex(v) for k, v in diccionario.items()}

def convertir_a_string(diccionario):
    def sustituir_derivadas(expr):
        patrones = [
            (r'Derivative\((\w+)\(([^),]+)\), (\w+)\)', r"\1'(\2)"),                             #Derivative(f(u), u) -> f'(u)
            (r'Derivative\((\w+)\(([^),]+)\), \(([^,]+), 2\)\)', r"\1''(\2)"),                   #Derivative(f(u), (u, 2)) -> f''(u)
            (r'Derivative\((\w+)\(([^,]+), ([^)]+)\), (\w+)\)', r'\1_\4(\2,\3)'),                #Derivative(f(u, v), u) -> f_u(u,v)
            (r'Derivative\((\w+)\(([^,]+), ([^)]+)\), (\w+), (\w+)\)', r'\1_\4\5(\2,\3)'),       #Derivative(f(u, v), u, v) -> f_uv(u,v)
            (r'Derivative\((\w+)\(([^,]+), ([^)]+)\), \(([^,]+), 2\)\)', r'\1_\4\4(\2,\3)'),     #Derivative(f(u, v), (u, 2)) -> f_uu(u,v)
        ]
        for patron, reemplazo in patrones:
            expr = re.sub(patron, reemplazo, expr)
        return expr
    def convertir_valor(valor):
        if isinstance(valor, (sp.Matrix, sp.MutableDenseMatrix, sp.ImmutableDenseMatrix)):
            return sustituir_derivadas(str(list(valor)))
        elif isinstance(valor, sp.Eq):
            return sustituir_derivadas(str(valor.lhs)) + ' = ' + sustituir_derivadas(str(valor.rhs))
        else:
            return sustituir_derivadas(str(valor))

    return {k: convertir_valor(v) for k, v in diccionario.items()}
    return {k: sp.latex(v) for k, v in diccionario.items()}

"""
-------------------------------------------------------------------------------
ENDPOINTS
-------------------------------------------------------------------------------
"""
app = Flask(__name__)

@app.route('/primera_forma_fundamental')
def primera_forma_fundamental():
    return jsonify(procesar_solicitud(primeraFormaFundamental, primeraFormaFundamental_pt_uv, primeraFormaFundamental_pt_xyz))

@app.route('/segunda_forma_fundamental')
def segunda_forma_fundamental():
    return jsonify(procesar_solicitud(segundaFormaFundamental, segundaFormaFundamental_pt_uv, segundaFormaFundamental_pt_xyz))

@app.route('/curvatura_Gauss')
def curvatura_Gauss():
    return jsonify(procesar_solicitud(curvaturaGauss, curvaturaGauss_pt_uv, curvaturaGauss_pt_xyz))

@app.route('/curvatura_media')
def curvatura_media():
    return jsonify(procesar_solicitud(curvaturaMedia, curvaturaMedia_pt_uv, curvaturaMedia_pt_xyz))

@app.route('/curvaturas_principales')
def curvaturas_principales():
    return jsonify(procesar_solicitud(curvaturasPrincipales, curvaturasPrincipales_pt_uv, curvaturasPrincipales_pt_xyz))

@app.route('/vector_normal')
def vector_normal():
    return jsonify(procesar_solicitud(normal, normal_pt_uv, normal_pt_xyz))

@app.route('/clasificacion_punto')
def clasificacion_punto():
    #TODO- como hacer con procesar_solicitud() ?
    superficie, u, v = procesar_solicitud()
    resultados = {}
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        return str(clasicPt_uv(superficie, u, v, u0, v0))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        return str(clasicPt_xyz(superficie, u, v, x0, y0, z0))
    
    raise Exception("No se ha definido correctamente el punto a clasificar")

@app.route('/plano_tangente')
def plano_tangente():
    return jsonify(procesar_solicitud(planoTangente, planoTangente_pt_uv, planoTangente_pt_xyz))

@app.route('/direcciones_principales')
def direcciones_principales():
    return jsonify(procesar_solicitud(dirPrinc, dirPrinc_pt_uv, dirPrinc_pt_xyz))

@app.route('/description')
def description():
    return jsonify(procesar_solicitud(descripccion, descripccion_pt_uv, descripccion_pt_xyz))

@app.route('/grafica')
def grafica():
    fig = go.Figure()


    fig = go.Figure(go.Surface(
        contours = {
            "x": {"show": True, "start": 1.5, "end": 2, "size": 0.04, "color":"white"},
            "z": {"show": True, "start": 0.5, "end": 0.8, "size": 0.05}
        },
        x = [1,2,3,4,5],
        y = [1,2,3,4,5],
        z = [
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0]
        ]))
    fig.update_layout(
        scene = {
            "xaxis": {"nticks": 20},
            "zaxis": {"nticks": 4},
            'camera_eye': {"x": 0, "y": -1, "z": 0.5},
            "aspectratio": {"x": 1, "y": 1, "z": 0.2},
        },
        clickmode='event+select'
        )
    return fig.to_html(include_mathjax="cdn")


    if '[' in request.args.get('superficie'):
        superficie, u, v = procesar_solicitud()
        fig = grafica_sup_param_plotly(superficie, u, v, 0, 2*sp.pi, 0, sp.pi, fig)
        fig.update_layout(
            scene=dict(
                aspectmode='data',
                aspectratio=dict(x=1, y=1, z=1)
            )
        )
        return render_template('grafica.html', plot=fig.to_html())
    else:
        return 'Superficie nivel'




if __name__ == '__main__':
    app.run(debug=True)