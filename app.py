from flask import Flask, request, jsonify

import sympy as sp
import re

import plotly.graph_objects as go

import utils.utils as utils
import utils.calc as calc
import utils.graph as graph
import utils.toLatex as tx
from utils.graph import *


"""
-------------------------------------------------------------------------------
FUNCIONES AUXILIARES Y ATRIBUTOS GENERALES
-------------------------------------------------------------------------------
"""
#Opciones que pueden describir a una variable, constante o función
OPCIONES_VAR = ['infinite', 'finite', 'real', 'extended_real', 'rational', 'irrational', 
                 'integer', 'noninteger', 'even', 'odd', 'prime', 'composite', 
                 'zero', 'nonzero', 'extended_nonzero', 'positive', 'nonnegative', 
                 'negative', 'nonpositive', 'extended_positive', 'extended_nonnegative',
                 'extended_negative', 'extended_nonpositive']

def procesar_solicitud(func: callable, func_pt_uv: callable, func_pt_xyz: callable, dict2latex: callable) -> dict:
    """
    Procesa una solicitud
    Argumentos:
    func                funcion a ejecutar sin punto especifico
    func_pt_uv          funcion a ejecutar con punto especifico en función de u, v
    func_pt_xyz         funcion a ejecutar con punto especifico en función de x, y, z
    dict2latex          funcion que convierte el resultado a latex
    """
    #Se obtiene los parametros de la solicitud
    var1 = request.args.get('var1', None)
    dom_var1_str = request.args.get('dom_var1', None)
    var2 = request.args.get('var2', None)
    dom_var2_str = request.args.get('dom_var2', None)
    superficie_str  = request.args.get('superficie', None)
    const_str = request.args.getlist('const')
    func_str = request.args.getlist('func')
    
    if not superficie_str:
        # TODO: Devolver teoría
        raise Exception("No se ha encontrado la parametrización de la superficie")

    #Se consigue la parametrización de la superficie convertida a objeto sympy
    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str, const_str, func_str)
    except Exception as e:
        # TODO: ¿Qué hacer si hay un error?
        raise e
    
    #Se extraen los dominios de las variables
    dom_u = extrae_dominio(dom_var1_str)
    dom_v = extrae_dominio(dom_var2_str)
    
    resultados = {
        'sup' : superficie,
        'u' : u,
        'v' : v
    }
    
    #Se comprueba si la superficie es regular
    if not utils.esRegular(superficie, u, v, dom_u, dom_v, resultados):
        raise Exception("La superficie parametrizada no es regular")
    
    #Se obtiene el punto a clasificar si hubiese y se devuelve los resultados
    u0 = obtiene_valor_pt('u0')
    v0 = obtiene_valor_pt('v0')
    if u0!=None and v0!=None :
        resultados['u0'] = u0
        resultados['v0'] = v0
        func_pt_uv(resultados)
        return dict2latex(resultados)

    x0 = obtiene_valor_pt('x0')
    y0 = obtiene_valor_pt('y0')
    z0 = obtiene_valor_pt('z0')
    if x0!=None and y0!=None and z0!=None:
        resultados['x0'] = x0
        resultados['y0'] = y0
        resultados['z0'] = z0
        func_pt_xyz(resultados)
        return dict2latex(resultados)
    
    if func_pt_uv is calc.clasicPt_uv:
        raise Exception("No se ha definido correctamente el punto a clasificar")
    
    func(resultados)
    return dict2latex(resultados)

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
    #Se obtiene la primera variable de la parametrización, por defecto es 'u'. Siempre real
    if not var1:
        var1='u'
    elif '[' in var1:
        var1, opciones = extrae_opciones_var(var1)
    opciones['real'] = True
    u = sp.symbols(var1.replace(' ', ''), **opciones)
    variables[var1] = u

    #Se obtiene la segunda variable de la parametrización, por defecto es 'v'. Siempre real
    opciones = {}
    if not var2:
        var2='v'
    elif '[' in var2:
        var2, opciones = extrae_opciones_var(var2)
    opciones['real'] = True
    v = sp.symbols(var2.replace(' ', ''), **opciones)
    variables[var2] = v

    #Se obtiene la descripción de las constantes
    #La lista debe ser de la forma ["[a, positive]", "[b]", "c, real", ...]
    for const in consts:
        nombre, opciones = extrae_opciones_var(const)
        opciones['real'] = True
        variables[nombre] = sp.symbols(nombre, **opciones)
    
    #Se obtiene la descripción de las funciones.
    #La lista debe ser de la forma ["[f(x,y), positive]", "[g(x)]", "h(a,x), real", ...]
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

    #Se obtiene la superficie parametrizada a expresion sympy
    superficie = sup.strip('[] ').split(',')
    if len(superficie) == 3:
        try:
            return sp.Matrix([sp.sympify(elem, locals=variables) for elem in superficie]), u, v
        except Exception as e:
            raise Exception(f"Error al procesar la superficie: {e}")
    else:
        raise Exception(f"Error al procesar la superficie: {sup}")

def extrae_dominio(dom_var) -> tuple:
    """
    Extrae el dominio de una variable
    Argumentos:
    dom_var             string con el dominio de la variable
    """
    dominio = sp.S.Reals
    if dom_var!=None:
        lista_dom_var = dom_var.replace(' ', '').split(',')
        if len(lista_dom_var) != 2:
            raise Exception(f"Error al procesar el dominio: {dom_var}")
        
        if '[' in lista_dom_var[0]:
            if ']' in lista_dom_var[1]:
                dominio = sp.Interval(sp.sympify(lista_dom_var[0].strip('[]')), sp.sympify(lista_dom_var[1].strip('[]')))
            elif ')' in lista_dom_var[1]:
                dominio = sp.Interval.Ropen(sp.sympify(lista_dom_var[0].strip('[]')), sp.sympify(lista_dom_var[1].strip('()')))
            else:
                raise Exception(f"Error al procesar el dominio: {dom_var}")
        elif '(' in lista_dom_var[0]:
            if ']' in lista_dom_var[1]:
                dominio = sp.Interval.Lopen(sp.sympify(lista_dom_var[0].replace(' ', '').strip('()')), sp.sympify(lista_dom_var[1].replace(' ', '').strip('[]')))
            elif ')' in lista_dom_var[1]:
                dominio = sp.Interval.open(sp.sympify(lista_dom_var[0].replace(' ', '').strip('()')), sp.sympify(lista_dom_var[1].replace(' ', '').strip('()')))
            else:
                raise Exception(f"Error al procesar el dominio: {dom_var}")  
    return dominio

def extrae_opciones_var(string: str) -> tuple:
    """
    Extrae el nombre de una variable y sus opciones
    Argumentos:
    string              string con el nombre de la variable y sus opciones
    """
    partes  = string.replace(' ', '').strip('[]').split(',')
    opciones_dict = {}
    for opcion in partes[1:]:
        if opcion in OPCIONES_VAR:
            opciones_dict[opcion] = True
    return partes[0], opciones_dict

def obtiene_valor_pt(string: str):
    """
    Obtiene el valor de un punto pasado a objeto sympy
    Argumentos:
    string              string con el nombre del argumento de la API con el punto
    """
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
    return jsonify(procesar_solicitud(calc.primeraFormaFundamental, calc.primeraFormaFundamental_pt_uv, calc.primeraFormaFundamental_pt_xyz, tx.res_PFF))

@app.route('/segunda_forma_fundamental')
def segunda_forma_fundamental():
    return jsonify(procesar_solicitud(calc.segundaFormaFundamental, calc.segundaFormaFundamental_pt_uv, calc.segundaFormaFundamental_pt_xyz, tx.res_SFF))

@app.route('/curvatura_Gauss')
def curvatura_Gauss():
    return jsonify(procesar_solicitud(calc.curvaturaGauss, calc.curvaturaGauss_pt_uv, calc.curvaturaGauss_pt_xyz, tx.res_curv_Gauss))

@app.route('/curvatura_media')
def curvatura_media():
    return jsonify(procesar_solicitud(calc.curvaturaMedia, calc.curvaturaMedia_pt_uv, calc.curvaturaMedia_pt_xyz, tx.res_curv_media))

@app.route('/curvaturas_principales')
def curvaturas_principales():
    return jsonify(procesar_solicitud(calc.curvaturasPrincipales, calc.curvaturasPrincipales_pt_uv, calc.curvaturasPrincipales_pt_xyz, tx.res_curv_media))

@app.route('/vector_normal')
def vector_normal():
    return jsonify(procesar_solicitud(calc.normal, calc.normal_pt_uv, calc.normal_pt_xyz, tx.res_normal))

@app.route('/clasificacion_punto')
def clasificacion_punto():
    #TODO- ¿como tranformar a Latex?
    return jsonify(procesar_solicitud(calc.clasicPt_uv, calc.clasicPt_uv, calc.clasicPt_xyz))

@app.route('/punto_umbilico')
def punto_umbilico():
    #TODO- ¿como tranformar a Latex?
    return jsonify(procesar_solicitud(calc.umbilico, calc.umbilico_pt_uv, calc.umbilico_pt_xyz))

@app.route('/plano_tangente')
def plano_tangente():
    return jsonify(procesar_solicitud(calc.planoTangente, calc.planoTangente_pt_uv, calc.planoTangente_pt_xyz, tx.res_tangente))

@app.route('/weingarten')
def weingarten():
    return jsonify(procesar_solicitud(calc.weingarten, calc.weingarten_pt_uv, calc.planoTangenteweingarten_pt_xyzpt_xyz, tx.res_Weingarten))

@app.route('/direcciones_principales')
def direcciones_principales():
    return jsonify(procesar_solicitud(calc.dirPrinc, calc.dirPrinc_pt_uv, calc.dirPrinc_pt_xyz, tx.res_dirs_princ))

@app.route('/description')
def description():
    return jsonify(procesar_solicitud(calc.descripccion, calc.descripccion_pt_uv, calc.descripccion_pt_xyz))

@app.route('/grafica')
def grafica():
    #Ejemplo: 
    # http://127.0.0.1:5000/grafica?superficie=[cos(u)*cos(v),%20cos(u)*sin(v),%20sin(u)]&dom_var1=(-pi/2,pi/2)&dom_var2=(0,2*pi)
    # http://127.0.0.1:5000/grafica?superficie=[cos(u)*cos(v),%20cos(u)*sin(v),%20sin(u)]&dom_var1=(-pi/2,pi/2)&dom_var2=(0,2*pi)&u0=0.5&v0=0.5
    if '[' in request.args.get('superficie'):
        var1 = request.args.get('var1', None)
        dom_var1_str = request.args.get('dom_var1', None)
        var2 = request.args.get('var2', None)
        dom_var2_str = request.args.get('dom_var2', None)
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
        
        #Se extraen los dominios de las variables
        dom_u = extrae_dominio(dom_var1_str)
        if not isinstance(dom_u, sp.Interval):
            dom_u = sp.Interval(-5, 5)
        dom_v = extrae_dominio(dom_var2_str)
        if not isinstance(dom_v, sp.Interval):
            dom_v = sp.Interval(-5, 5)
        
        if not utils.esRegular(superficie, u, v, dom_u, dom_v, {}):
            raise Exception("La superficie parametrizada no es regular")

        u0 = obtiene_valor_pt('u0')
        v0 = obtiene_valor_pt('v0')
        if u0!=None and v0!=None :
            fig = graph.desc_punto(superficie, u, v, u0, v0,
                                   limite_inf_u=dom_u.start, limite_sup_u=dom_u.end,
                                   limite_inf_v=dom_v.start, limite_sup_v=dom_v.end)
            return fig.to_html(include_mathjax="cdn")

        x0 = obtiene_valor_pt('x0')
        y0 = obtiene_valor_pt('y0')
        z0 = obtiene_valor_pt('z0')
        if x0!=None and y0!=None and z0!=None:
            fig = graph.anade_descr_pt_xyz(superficie, u, v, x0, y0, z0,
                                   limite_inf_u=dom_u.start, limite_sup_u=dom_u.end,
                                   limite_inf_v=dom_v.start, limite_sup_v=dom_v.end)
            return fig.to_html(include_mathjax="cdn")
        
        fig = sup_param(superficie, u, v, 
                        limite_inf_u=dom_u.start, limite_sup_u=dom_u.end, 
                        limite_inf_v=dom_v.start, limite_sup_v=dom_v.end)
        return fig.to_html(include_mathjax="cdn")
    else:
        return 'Superficie nivel'




if __name__ == '__main__':
    app.run(debug=True)