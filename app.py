from flask import Flask, request, jsonify

import sympy as sp
import re

import plotly.graph_objects as go

import utils.utils as utils
import utils.calc_param as calcp
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
    #TODO: manera de devolve los resultados
    dict2latex = aLatex

    #Se obtiene los parametros de la solicitud
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie', None)
    const_str = request.args.getlist('const')
    func_str = request.args.getlist('func')
    cond_str = request.args.get('cond', None)
    dom_var1_str = request.args.get('dom_var1', None)
    dom_var2_str = request.args.get('dom_var2', None)
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    
    if not superficie_str:
        # TODO: Devolver teoría
        raise Exception("No se ha encontrado la parametrización de la superficie")

    #Se consigue la parametrización de la superficie convertida a objeto sympy
    try:
        superficie, u, v, cond = normaliza_parametrizacion(var1, var2, superficie_str, const_str, func_str, cond_str)
    except Exception as e:
        # TODO: ¿Qué hacer si hay un error?
        raise e

    #Se extraen los dominios de las variables
    dom_u = extrae_dominio(dom_var1_str)
    dom_v = extrae_dominio(dom_var2_str)
    
    resultados = {
        'sup' : superficie,
        'u' : u,
        'v' : v,
        'dom_u' : dom_u,
        'dom_v' : dom_v
    }
    if cond != None:
        resultados['cond'] = cond
    
    #Se comprueba si la superficie es regular
    if not resultados['sup'].has(sp.Function) and not calcp.esRegular(resultados):
        raise Exception("La superficie parametrizada no es regular")
    
    #Se obtiene el punto a clasificar si hubiese y se devuelve los resultados
    u0 = obtiene_valor_pt(u0)
    v0 = obtiene_valor_pt(v0)
    if u0!=None and v0!=None :
        resultados['u0'] = u0
        resultados['v0'] = v0
        func_pt_uv(resultados)
        return dict2latex(resultados)

    x0 = obtiene_valor_pt(x0)
    y0 = obtiene_valor_pt(y0)
    z0 = obtiene_valor_pt(z0)
    if x0!=None and y0!=None and z0!=None:
        resultados['x0'] = x0
        resultados['y0'] = y0
        resultados['z0'] = z0
        func_pt_xyz(resultados)
        return dict2latex(resultados)
    
    if func_pt_uv is calcp.clasicPt_uv:
        raise Exception("No se ha definido correctamente el punto a clasificar")
    
    func(resultados)
    return dict2latex(resultados)

def normaliza_parametrizacion(var1: str, var2: str, sup: str, consts: list, funcs: list, cond: str) -> tuple:
    """
    Transforma la parametrización de una superficie a una expresion sympy con sus variable correspondientes
    No se hacen comprobaciones de tipo

    Argumentos:
    var1                string con la primera variable de la parametrización
    var2                string con la segunda variable de la parametrización
    sup                 string con la parametrización de la superficie
    consts              lista de strings con constantes y su descripción
    func                lista de strings con funciones y su descripción
    cond                string con la condición de las variables de la parametrización
    """
    variables = {}

    opciones = {}
    #Se obtiene la primera variable de la parametrización, por defecto es 'u'. Siempre real
    if not var1:
        var1='u'
    elif ',' in var1:
        var1, opciones = extrae_opciones_var(var1)
    opciones['real'] = True
    u = sp.symbols(var1.replace(' ', ''), **opciones)
    variables[var1] = u

    #Se obtiene la segunda variable de la parametrización, por defecto es 'v'. Siempre real
    opciones = {}
    if not var2:
        var2='v'
    elif ',' in var2:
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
            return sp.Matrix([sp.sympify(elem, locals=variables) for elem in superficie]), u, v, sp.sympify(cond, locals=variables) if cond else None
        except Exception as e:
            raise Exception(f"Error al procesar la superficie: {e}")
    else:
        raise Exception(f"Error al procesar la superficie: {sup}")

def normaliza_implicita(var1: str, var2: str, var3: str, sup: str, consts: list, funcs: list) -> tuple:
    """
    Transforma la parametrización de una superficie a una expresion sympy con sus variable correspondientes
    No se hacen comprobaciones de tipo

    Argumentos:
    var1                string con la primera variable (x)
    var2                string con la segunda variable (y)
    var3                string con la tercera variable (z)
    sup                 string con la ecuación de la superficie
    consts              lista de strings con constantes y su descripción
    func                lista de strings con funciones y su descripción
    """
    variables = {}

    opciones = {}
    #Se obtiene la primera variable de la superficie, por defecto es 'x'. Siempre real
    if not var1:
        var1='x'
    elif ',' in var1:
        var1, opciones = extrae_opciones_var(var1)
    opciones['real'] = True
    x = sp.symbols(var1.replace(' ', ''), **opciones)
    variables[var1] = x

    #Se obtiene la segunda variable de la superficie, por defecto es 'y'. Siempre real
    opciones = {}
    if not var2:
        var2='y'
    elif ',' in var2:
        var2, opciones = extrae_opciones_var(var2)
    opciones['real'] = True
    y = sp.symbols(var2.replace(' ', ''), **opciones)
    variables[var2] = y

    #Se obtiene la tercera variable de la superficie, por defecto es 'z'. Siempre real
    opciones = {}
    if not var3:
        var3='z'
    elif ',' in var3:
        var3, opciones = extrae_opciones_var(var3)
    opciones['real'] = True
    z = sp.symbols(var3.replace(' ', ''), **opciones)
    variables[var3] = z

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

    #Se obtiene la superficie implicita a expresion sympy
    try:
        return sp.sympify(sup, locals=variables), x, y, z
    except Exception as e:
        raise Exception(f"Error al procesar la superficie: {e}")

def extrae_dominio(dom_var) -> tuple:
    """
    Extrae el dominio de una variable, si se le pasa algo que no es un string devuelve el dominio de los reales.
    La entrada debe ser de la forma "(a, b)"

    Argumentos:
    dom_var             string con el dominio de la variable
    """
    dominio = sp.S.Reals
    if isinstance(dom_var, str):
        dom_var = dom_var.replace(' ', '')
        lista_dom_var = dom_var.split(',')
        if len(lista_dom_var) != 2:
            raise Exception(f"Error al procesar el dominio: {dom_var}")
        
        start = sp.sympify(lista_dom_var[0].strip('()'))
        end = sp.sympify(lista_dom_var[1].strip('()'))
        if not start.is_number or not end.is_number:
            raise Exception(f"Error al procesar el dominio: {dom_var}")
        dominio = sp.Interval.open(start, end)
    return dominio

def extrae_opciones_var(string: str) -> tuple:
    """
    Extrae el nombre de una variable y sus opciones. La entrada debe ser de la forma "[nombre, opcion1, opcion2, ...]"

    Argumentos:
    string              string con el nombre de la variable y sus opciones
    """
    partes  = string.replace(' ', '').strip('[]').split(',')
    opciones_dict = {}
    for opcion in partes[1:]:
        if opcion in OPCIONES_VAR:
            opciones_dict[opcion] = True
    return partes[0], opciones_dict

def obtiene_valor_pt(pt: str):
    """
    Obtiene el valor de un punto pasado a objeto sympy

    Argumentos:
    pt              string con el nombre del argumento de la API con el punto
    """
    pt = sp.sympify(pt) if pt else None
    if pt != None and not pt.is_number:
        pt = None
    return pt

def aLatex(res: dict) -> str:
    return {k: str(v) for k, v in res.items()}

"""
-------------------------------------------------------------------------------
ENDPOINTS
-------------------------------------------------------------------------------
"""
app = Flask(__name__)

@app.route('/primera_forma_fundamental')
def primera_forma_fundamental():
    return jsonify(procesar_solicitud(calcp.primeraFormaFundamental, calcp.primeraFormaFundamental_pt_uv, calcp.primeraFormaFundamental_pt_xyz, tx.res_PFF))

@app.route('/segunda_forma_fundamental')
def segunda_forma_fundamental():
    return jsonify(procesar_solicitud(calcp.segundaFormaFundamental, calcp.segundaFormaFundamental_pt_uv, calcp.segundaFormaFundamental_pt_xyz, tx.res_SFF))

@app.route('/curvatura_Gauss')
def curvatura_Gauss():
    return jsonify(procesar_solicitud(calcp.curvaturaGauss, calcp.curvaturaGauss_pt_uv, calcp.curvaturaGauss_pt_xyz, tx.res_curv_Gauss))

@app.route('/curvatura_media')
def curvatura_media():
    return jsonify(procesar_solicitud(calcp.curvaturaMedia, calcp.curvaturaMedia_pt_uv, calcp.curvaturaMedia_pt_xyz, tx.res_curv_media))

@app.route('/curvaturas_principales')
def curvaturas_principales():
    return jsonify(procesar_solicitud(calcp.curvaturasPrincipales, calcp.curvaturasPrincipales_pt_uv, calcp.curvaturasPrincipales_pt_xyz, tx.res_curv_media))

@app.route('/vector_normal')
def vector_normal():
    return jsonify(procesar_solicitud(calcp.normal, calcp.normal_pt_uv, calcp.normal_pt_xyz, tx.res_normal))

@app.route('/clasificacion_punto')
def clasificacion_punto():
    #TODO- ¿como tranformar a Latex?
    return jsonify(procesar_solicitud(calcp.clasicPt_uv, calcp.clasicPt_uv, calcp.clasicPt_xyz))

@app.route('/punto_umbilico')
def punto_umbilico():
    #TODO- ¿como tranformar a Latex?
    return jsonify(procesar_solicitud(calcp.umbilico, calcp.umbilico_pt_uv, calcp.umbilico_pt_xyz))

@app.route('/plano_tangente')
def plano_tangente():
    return jsonify(procesar_solicitud(calcp.planoTangente, calcp.planoTangente_pt_uv, calcp.planoTangente_pt_xyz, tx.res_tangente))

@app.route('/weingarten')
def weingarten():
    return jsonify(procesar_solicitud(calcp.weingarten, calcp.weingarten_pt_uv, calcp.planoTangenteweingarten_pt_xyzpt_xyz, tx.res_Weingarten))

@app.route('/direcciones_principales')
def direcciones_principales():
    return jsonify(procesar_solicitud(calcp.dirPrinc, calcp.dirPrinc_pt_uv, calcp.dirPrinc_pt_xyz, tx.res_dirs_princ))

@app.route('/description')
def description():
    return jsonify(procesar_solicitud(calcp.descripccion, calcp.descripccion_pt_uv, calcp.descripccion_pt_xyz, aLatex))

@app.route('/grafica')
def grafica():
    superficie_str  = request.args.get('superficie', None)
    #Ejemplo: 
    # http://127.0.0.1:5000/grafica?superficie=[cos(u)*cos(v),%20cos(u)*sin(v),%20sin(u)]&dom_var1=(-pi/2,pi/2)&dom_var2=(0,2*pi)
    # http://127.0.0.1:5000/grafica?superficie=[cos(u)*cos(v),%20cos(u)*sin(v),%20sin(u)]&dom_var1=(-pi/2,pi/2)&dom_var2=(0,2*pi)&u0=0.5&v0=0.5
    # http://127.0.0.1:5000/grafica?superficie=x**2-y**2-z**2-1
    # http://127.0.0.1:5000/grafica?superficie=x**2%2By**2%2Bz**2-1&dom_var1=[-1,1]&dom_var2=[-1,1]&dom_var3=[-1,1]&x0=0&y0=0&z0=1

    if superficie_str == None:
        #TODO_ Devolver teoría
        raise Exception("No se ha encontrado la parametrización de la superficie")
    elif '[' in superficie_str:
        var1 = request.args.get('var1', None)
        var2 = request.args.get('var2', None)
        superficie_str  = request.args.get('superficie', None)
        const_str = request.args.getlist('const')
        func_str = request.args.getlist('func')
        cond_str = request.args.get('cond', None)
        dom_var1_str = request.args.get('dom_var1', None)
        dom_var2_str = request.args.get('dom_var2', None)
        u0 = request.args.get('u0', None)
        v0 = request.args.get('v0', None)
        x0 = request.args.get('x0', None)
        y0 = request.args.get('y0', None)
        z0 = request.args.get('z0', None)
        
        if not superficie_str:
            # TODO: Devolver teoría
            raise Exception("No se ha encontrado la parametrización de la superficie")

        try:
            superficie, u, v, cond = normaliza_parametrizacion(var1, var2, superficie_str, const_str, func_str, cond_str)
        except Exception as e:
            # TODO: ¿Qué hacer si hay un error?
            raise e
        
        #Se extraen los dominios de las variables
        dom_u = extrae_dominio(dom_var1_str)
        if dom_u==sp.S.Reals or not isinstance(dom_u, sp.Interval):
            dom_u = sp.Interval(-5, 5)
        dom_v = extrae_dominio(dom_var2_str)
        if dom_v==sp.S.Reals or not isinstance(dom_v, sp.Interval):
            dom_v = sp.Interval(-5, 5)

        resultados = {
            'sup' : superficie,
            'u' : u,
            'v' : v,
            'dom_u' : dom_u,
            'dom_v' : dom_v
        }
        
        if not calcp.esRegular(resultados):
            raise Exception("La superficie parametrizada no es regular")

        u0 = obtiene_valor_pt(u0)
        v0 = obtiene_valor_pt(v0)
        if u0!=None and v0!=None :
            fig = graph.param_desc_pt_uv(superficie, u, v, u0, v0,
                                   limite_inf_u=dom_u.start, limite_sup_u=dom_u.end,
                                   limite_inf_v=dom_v.start, limite_sup_v=dom_v.end)
            return fig.to_html(include_mathjax="cdn")

        x0 = obtiene_valor_pt(x0)
        y0 = obtiene_valor_pt(y0)
        z0 = obtiene_valor_pt(z0)
        if x0!=None and y0!=None and z0!=None:
            fig = graph.param_desc_pt_xyz(superficie, u, v, x0, y0, z0,
                                   limite_inf_u=dom_u.start, limite_sup_u=dom_u.end,
                                   limite_inf_v=dom_v.start, limite_sup_v=dom_v.end)
            return fig.to_html(include_mathjax="cdn")
        
        fig = graph.sup_param(superficie, u, v, 
                        limite_inf_u=dom_u.start, limite_sup_u=dom_u.end, 
                        limite_inf_v=dom_v.start, limite_sup_v=dom_v.end)
        return fig.to_html(include_mathjax="cdn")
    else:
        var1 = request.args.get('var1', None)
        var2 = request.args.get('var2', None)
        var3 = request.args.get('var3', None)
        const_str = request.args.getlist('const')
        func_str = request.args.getlist('func')
        dom_x  = request.args.get('dom_var1', None)
        dom_y  = request.args.get('dom_var2', None)    
        dom_z  = request.args.get('dom_var3', None)

        
        if not superficie_str:
            # TODO: Devolver teoría
            raise Exception("No se ha encontrado la parametrización de la superficie")

        try:
            superficie, x, y, z = normaliza_implicita(var1, var2, var3, superficie_str, const_str, func_str)
        except Exception as e:
            # TODO: ¿Qué hacer si hay un error?
            raise e
        #Compruebo que es una superficie de nivel
        if not utils.esSupNivel(superficie, x, y, z, {}):
            raise Exception("La superficie parametrizada no es regular")

        #Extraigo el dominio donde se quiere considerar la superficie, si no hay o son los reales de pone [-5, 5]
        dom_x = extrae_dominio(dom_x)
        if dom_x==sp.S.Reals or not isinstance(dom_x, sp.Interval):
            dom_x = sp.Interval(-5, 5)
        dom_y = extrae_dominio(dom_y)
        if dom_y==sp.S.Reals or not isinstance(dom_y, sp.Interval):
            dom_y = sp.Interval(-5, 5)
        dom_z = extrae_dominio(dom_z)
        if dom_z==sp.S.Reals or not isinstance(dom_z, sp.Interval):
            dom_z = sp.Interval(-5, 5)

        x0 = obtiene_valor_pt('x0')
        y0 = obtiene_valor_pt('y0')
        z0 = obtiene_valor_pt('z0')
        if x0!=None and y0!=None and z0!=None:
            fig = graph.imp_desc_pt(superficie, x, y, z, x0, y0, z0,
                                   limite_inf_x=dom_x.start, limite_sup_x=dom_x.end,
                                   limite_inf_y=dom_y.start, limite_sup_y=dom_y.end,
                                   limite_inf_z=dom_z.start, limite_sup_z=dom_z.end)
            return fig.to_html(include_mathjax="cdn")
        
        fig = graph.sup_imp(superficie, x, y, z,
                        limite_inf_x=dom_x.start, limite_sup_x=dom_x.end, 
                        limite_inf_y=dom_y.start, limite_sup_y=dom_y.end,
                        limite_inf_z=dom_z.start, limite_sup_z=dom_z.end,
                        titulo=r'$'+sp.latex(superficie)+r'=0$')
        return fig.to_html(include_mathjax="cdn")





if __name__ == '__main__':
    app.run(debug=True)