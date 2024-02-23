from flask import Flask, request, jsonify

import sympy as sp
import re

import plotly.graph_objects as go

import utils.calc as calc
import utils.graph as graph
from utils.graph import *


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

def procesar_solicitud(func: callable, func_pt_uv: callable, func_pt_xyz: callable) -> dict:
    """
    Procesa una solicitud
    """
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie', None)
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
    
    resultados = {
        'sup' : superficie,
        'u' : u,
        'v' : v
    }

    u0 = obtiene_valor_pt('u0')
    v0 = obtiene_valor_pt('v0')
    if u0!=None and v0!=None :
        resultados['u0'] = u0
        resultados['v0'] = v0
        func_pt_uv(resultados)
        return convertir_a_string(resultados)

    x0 = obtiene_valor_pt('x0')
    y0 = obtiene_valor_pt('y0')
    z0 = obtiene_valor_pt('z0')
    if x0!=None and y0!=None and z0!=None:
        resultados['x0'] = x0
        resultados['y0'] = y0
        resultados['z0'] = z0
        func_pt_xyz(resultados)
        return convertir_a_string(resultados)
    
    if func_pt_uv is calc.clasicPt_uv:
        raise Exception("No se ha definido correctamente el punto a clasificar")
    
    func(resultados)
    return convertir_a_string(resultados)

def normaliza_parametrizacion(var1: str, var2: str, sup: str, consts: list, funcs: list) -> tuple:
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

    
    superficie = sup.strip('[] ').split(',')
    if len(superficie) == 3:
        try:
            return sp.Matrix([sp.sympify(elem, locals=variables) for elem in superficie]), u, v
        except Exception as e:
            raise Exception(f"Error al procesar la superficie: {e}")
    elif len(superficie) == 1:
        try:
            return sp.sympify(superficie, locals=variables), u, v
        except Exception as e:
            raise Exception(f"Error al procesar la superficie: {e}")
    else:
        raise Exception(f"Error al procesar la superficie: {sup}")
   
def extrae_opciones_var(string: str) -> tuple:
    partes  = string.replace(' ', '').strip('[]').split(',')
    opciones_dict = {}
    for opcion in partes[1:]:
        if opcion in OPCIONES_VAR:
            opciones_dict[opcion] = True
    return partes[0], opciones_dict

def sympy2latex(diccionario: dict) -> dict:
    return {k: sp.latex(v) for k, v in diccionario.items()}

def convertir_a_string(diccionario: dict) -> dict:
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

def obtiene_valor_pt(string: str):
    pt = request.args.get(string, None)
    pt = sp.sympify(pt) if pt else None
    if pt != None and not pt.is_number:
        pt = None
    return pt

"""
-------------------------------------------------------------------------------
ENDPOINTS
-------------------------------------------------------------------------------
"""
app = Flask(__name__)

@app.route('/primera_forma_fundamental')
def primera_forma_fundamental():
    return jsonify(procesar_solicitud(calc.primeraFormaFundamental, calc.primeraFormaFundamental_pt_uv, calc.primeraFormaFundamental_pt_xyz))

@app.route('/segunda_forma_fundamental')
def segunda_forma_fundamental():
    return jsonify(procesar_solicitud(calc.segundaFormaFundamental, calc.segundaFormaFundamental_pt_uv, calc.segundaFormaFundamental_pt_xyz))

@app.route('/curvatura_Gauss')
def curvatura_Gauss():
    return jsonify(procesar_solicitud(calc.curvaturaGauss, calc.curvaturaGauss_pt_uv, calc.curvaturaGauss_pt_xyz))

@app.route('/curvatura_media')
def curvatura_media():
    return jsonify(procesar_solicitud(calc.curvaturaMedia, calc.curvaturaMedia_pt_uv, calc.curvaturaMedia_pt_xyz))

@app.route('/curvaturas_principales')
def curvaturas_principales():
    return jsonify(procesar_solicitud(calc.curvaturasPrincipales, calc.curvaturasPrincipales_pt_uv, calc.curvaturasPrincipales_pt_xyz))

@app.route('/vector_normal')
def vector_normal():
    return jsonify(procesar_solicitud(calc.normal, calc.normal_pt_uv, calc.normal_pt_xyz))

@app.route('/clasificacion_punto')
def clasificacion_punto():
    return jsonify(procesar_solicitud(calc.clasicPt_uv, calc.clasicPt_uv, calc.clasicPt_xyz))

@app.route('/plano_tangente')
def plano_tangente():
    return jsonify(procesar_solicitud(calc.planoTangente, calc.planoTangente_pt_uv, calc.planoTangente_pt_xyz))

@app.route('/direcciones_principales')
def direcciones_principales():
    return jsonify(procesar_solicitud(calc.dirPrinc, calc.dirPrinc_pt_uv, calc.dirPrinc_pt_xyz))

@app.route('/description')
def description():
    return jsonify(procesar_solicitud(calc.descripccion, calc.descripccion_pt_uv, calc.descripccion_pt_xyz))

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
        fig = sup_param(superficie, u, v, 0, 2*sp.pi, 0, sp.pi, fig)
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