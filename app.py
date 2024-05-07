from flask import Flask, request, jsonify, Blueprint

import sympy as sp
import re

import plotly.graph_objects as go

import utils.utils as utils
import utils.calc_param as calcp
import utils.calc_imp as calci
import utils.graph as graph

import utils.Latex.sparam.teoria.teoria as txparamth
import utils.Latex.sparam.resultados.resultados as txparamres

import utils.Latex.simpl.teoria.teoria as txsimplth
import utils.Latex.simpl.resultados.resultados as txsimplres


app = Flask(__name__)

"""
-------------------------------------------------------------------------------
FUNCIONES AUXILIARES Y ATRIBUTOS GENERALES
-------------------------------------------------------------------------------
"""
#Opciones que pueden describir a una variable, constante o función
OPCIONES_VAR = ['positive', 'negative','integer','noninteger','even', 'odd']

def extrae_dominio(dom_var: str) -> tuple:
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
    pt              string con el valor del punto que se quiere obtener
    """
    pt = sp.sympify(pt) if pt else None
    if pt != None and not pt.is_number:
        pt = None
    return pt

"""
-------------------------------------------------------------------------------
SUPERFICIE PARAMETRIZADA
-------------------------------------------------------------------------------
"""
param_surf_bp = Blueprint('parametrizada', __name__)

#FUNCION AUXILIARES
def procesar_solicitud_param(func: callable, func_pt_uv: callable, func_pt_xyz: callable, dict2latex: callable, dict2latex_pt: callable, txth: str='') -> dict:
    """
    Procesa una solicitud
    Argumentos:
    func                funcion a ejecutar sin punto especifico
    func_pt_uv          funcion a ejecutar con punto especifico en función de u, v
    func_pt_xyz         funcion a ejecutar con punto especifico en función de x, y, z
    dict2latex          funcion que convierte el resultado a latex
    dict2latex_pt       funcion que convierte el resultado con punto a latex
    txth                string con la teoría de la función
    """
    superficie_str  = request.args.get('superficie', None)
    if not superficie_str:
        return {'pasos': [{"descripcion": txth, "paso": "", "pasoLatex": "" }]}


    #Se consigue la parametrización de la superficie convertida a objeto sympy
    func_str = request.args.getlist('func')
    try:
        superficie, variables = normaliza_parametrizacion(request.args.get('var1', None), 
                                                          request.args.get('var2', None), 
                                                          superficie_str, 
                                                          request.args.getlist('const'), 
                                                          func_str)
    except Exception as e:
        # TODO: ¿Qué hacer si hay un error?
        raise e

    #Se extraen los dominios de las variables
    dom_u = extrae_dominio(request.args.get('dom_var1', None))
    dom_v = extrae_dominio(request.args.get('dom_var2', None))
    
    resultados = {
        'sup' : superficie,
        'u' : variables['u'],
        'v' : variables['v'],
        'dom_u' : dom_u,
        'dom_v' : dom_v
    }

    cond_str = request.args.get('cond', None)
    if cond_str != None:
        resultados['cond'] = sp.sympify(cond_str, locals=variables)
    
    #Se comprueba si la superficie es regular (solo si se tiene una superficies sin funciones)
    if func_str == [] and not calcp.esRegular(resultados):
        raise Exception("La superficie parametrizada no es regular")
    
    #Variable para saber si simplificar los valores absolutos de las funciones trigonometricas
    simp_trig = True if request.args.get('trig', None)!=None else False

    #Se obtiene el punto a clasificar si hubiese y se devuelve los resultados
    u0 = obtiene_valor_pt(request.args.get('u0', None))
    v0 = obtiene_valor_pt(request.args.get('v0', None))
    if u0!=None and v0!=None :
        resultados['u0'] = u0
        resultados['v0'] = v0
        func_pt_uv(resultados)
        if simp_trig:
            utils.aplica_simplificaciones(resultados)
        return {'pasos': dict2latex_pt(resultados)}

    x0 = obtiene_valor_pt(request.args.get('x0', None))
    y0 = obtiene_valor_pt(request.args.get('y0', None))
    z0 = obtiene_valor_pt(request.args.get('z0', None))
    if x0!=None and y0!=None and z0!=None:
        resultados['x0'] = x0
        resultados['y0'] = y0
        resultados['z0'] = z0
        func_pt_xyz(resultados)
        if simp_trig:
            utils.aplica_simplificaciones(resultados)
        return {'pasos': dict2latex_pt(resultados)}
    
    if func==None:
        raise Exception("No se ha definido correctamente el punto")
    
    func(resultados)
    if simp_trig:
        utils.aplica_simplificaciones(resultados)
    return {'pasos': dict2latex(resultados)}

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

    #Se obtiene la primera variable de la parametrización, por defecto es 'u'. Siempre real
    opciones = {}
    if not var1: var1='u'
    elif ',' in var1: var1, opciones = extrae_opciones_var(var1)
    opciones['real'] = True
    u = sp.symbols(var1, **opciones)
    variables['u'] = u

    #Se obtiene la segunda variable de la parametrización, por defecto es 'v'. Siempre real
    opciones = {}
    if not var2: var2='v'
    elif ',' in var2: var2, opciones = extrae_opciones_var(var2)
    opciones['real'] = True
    v = sp.symbols(var2, **opciones)
    variables['v'] = v

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
            return sp.Matrix([sp.sympify(elem, locals=variables) for elem in superficie]).T, variables
        except Exception as e:
            raise Exception(f"Error al procesar la superficie: {e}")
    else:
        raise Exception(f"Error al procesar la superficie: {sup}")


#ENDPOINTS
@param_surf_bp.route('/primera_forma_fundamental')
def primera_forma_fundamental():
    return jsonify(procesar_solicitud_param(calcp.primeraFormaFundamental, calcp.primeraFormaFundamental_pt_uv, calcp.primeraFormaFundamental_pt_xyz, txparamres.res_PFF, txparamres.res_PFF_pt, txparamth.TH_PFF))

@param_surf_bp.route('/segunda_forma_fundamental')
def segunda_forma_fundamental():
    return jsonify(procesar_solicitud_param(calcp.segundaFormaFundamental, calcp.segundaFormaFundamental_pt_uv, calcp.segundaFormaFundamental_pt_xyz, txparamres.res_SFF, txparamres.res_SFF_pt, txparamth.TH_SFF))

@param_surf_bp.route('/curvatura_Gauss')
def curvatura_Gauss():
    return jsonify(procesar_solicitud_param(calcp.curvaturaGauss, calcp.curvaturaGauss_pt_uv, calcp.curvaturaGauss_pt_xyz, txparamres.res_curv_Gauss, txparamres.res_curv_Gauss_pt, txparamth.TH_CURV_GAUSS))

@param_surf_bp.route('/curvatura_media')
def curvatura_media():
    return jsonify(procesar_solicitud_param(calcp.curvaturaMedia, calcp.curvaturaMedia_pt_uv, calcp.curvaturaMedia_pt_xyz, txparamres.res_curv_media, txparamres.res_curv_media_pt, txparamth.TH_CURV_MEDIA))

@param_surf_bp.route('/curvaturas_principales')
def curvaturas_principales():
    return jsonify(procesar_solicitud_param(calcp.curvaturasPrincipales, calcp.curvaturasPrincipales_pt_uv, calcp.curvaturasPrincipales_pt_xyz, txparamres.res_curvs_principales, txparamres.res_curvs_principales_pt, txparamth.TH_CURVS_PRINCIPALES))

@param_surf_bp.route('/vector_normal')
def vector_normal():
    return jsonify(procesar_solicitud_param(calcp.normal, calcp.normal_pt_uv, calcp.normal_pt_xyz, txparamres.res_vect_normal, txparamres.res_vect_normal_pt, txparamth.TH_VEC_NORMAL))

@param_surf_bp.route('/clasificacion_punto')
def clasificacion_punto():
    return jsonify(procesar_solicitud_param(None, calcp.clasicPt_uv, calcp.clasicPt_xyz, None, txparamres.res_clasif_pt, txparamth.TH_CLASIFICACION_PTOS))

@param_surf_bp.route('/punto_umbilico')
def punto_umbilico():
    return jsonify(procesar_solicitud_param(None, calcp.umbilico_pt_uv, calcp.umbilico_pt_xyz, txparamres.res_ptos_umbilicos, txparamres.res_ptos_umbilicos_pt, txparamth.TH_PTS_UMBILICOS))

@param_surf_bp.route('/direccion_asintotica')
def direccion_asintotica():
    return jsonify(procesar_solicitud_param(None, calcp.dirAsin_pt_uv, calcp.dirAsin_pt_xyz, None, txparamres.res_dirs_asint, txparamth.TH_DIRS_ASINTOTICAS))

@param_surf_bp.route('/plano_tangente')
def plano_tangente():
    return jsonify(procesar_solicitud_param(calcp.planoTangente, calcp.planoTangente_pt_uv, calcp.planoTangente_pt_xyz, txparamres.res_plano_tangente, txparamres.res_plano_tangente_pt, txparamth.TH_PLANO_TANG))

@param_surf_bp.route('/weingarten')
def weingarten():
    return jsonify(procesar_solicitud_param(calcp.weingarten, calcp.weingarten_pt_uv, calcp.weingarten_pt_xyz, txparamres.res_Weingarten, txparamres.res_Weingarten_pt, txparamth.TH_WEINGARTEN))

@param_surf_bp.route('/direcciones_principales')
def direcciones_principales():
    return jsonify(procesar_solicitud_param(calcp.dirPrinc, calcp.dirPrinc_pt_uv, calcp.dirPrinc_pt_xyz, txparamres.res_dirs_principales, txparamres.res_dirs_principales_pt, txparamth.TH_DIRS_PRINCIPALES))

@param_surf_bp.route('/description')
def description():
    return jsonify(procesar_solicitud_param(calcp.descripccion, calcp.descripccion_pt_uv, calcp.descripccion_pt_xyz, txparamres.res_analisis_completo, txparamres.res_analisis_completo_pt, txparamth.TH_ANALISIS))

@param_surf_bp.route('/grafica')
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
    else:
        #Se obtienen las variables de la parametrización
        variables = {}

        opciones = {}
        var1 = request.args.get('var1', None)
        if not var1: var1='u'
        elif ',' in var1: var1, opciones = extrae_opciones_var(var1)
        opciones['real'] = True
        u = sp.symbols(var1, **opciones)
        variables[var1] = u

        opciones = {}
        var2 = request.args.get('var2', None)
        if not var2: var2='v'
        elif ',' in var2: var2, opciones = extrae_opciones_var(var2)
        opciones['real'] = True
        v = sp.symbols(var2, **opciones)
        variables[var2] = v


        #Se obtiene la superficie parametrizada a expresion sympy
        superficie = superficie_str.strip('[] ').split(',')
        if len(superficie) == 3:
            try:
                sup = sp.Matrix([sp.sympify(elem, locals=variables) for elem in superficie])
            except Exception as e:
                raise Exception(f"Error al procesar la superficie: {e}")
        else:
            raise Exception(f"Error al procesar la superficie: {superficie_str}")
        
        if not sup.free_symbols.issubset(set([u, v])):
            raise Exception("Se han detectado variables no permitidas, solo se permiten u,v")

        #Si el dominio de la variables es de la forma a*u+b*v<r se representa directamente
        cond_str = request.args.get('cond', None)
        if cond_str!=None:
            sy_cond = sp.sympify(cond_str, locals=variables)
            if sy_cond.free_symbols.issubset(set([u, v])) and isinstance(sy_cond, sp.StrictLessThan):
                expr = sy_cond.lhs - sy_cond.rhs
                a = expr.coeff(u**2)
                b = expr.coeff(v**2)
                r = expr - a*u**2 - b*v**2
                if r.is_constant():
                    a = a/-r
                    b = b/-r
                    fig = graph.sup_param_cond_elipse(sup, u, v, a, b)
                    return fig.to_html(include_mathjax="cdn")

        #Se extraen los dominios de las variables
        dom_u = extrae_dominio(request.args.get('dom_var1', None))
        if dom_u==sp.S.Reals or not isinstance(dom_u, sp.Interval):
            dom_u = sp.Interval(-5, 5)
        dom_v = extrae_dominio(request.args.get('dom_var2', None))
        if dom_v==sp.S.Reals or not isinstance(dom_v, sp.Interval):
            dom_v = sp.Interval(-5, 5)

        resultados = {
            'sup' : sup,
            'u' : u,
            'v' : v,
            'dom_u' : dom_u,
            'dom_v' : dom_v
        }

        if not calcp.esRegular(resultados):
            raise Exception("La superficie parametrizada no es regular")

        u0 = obtiene_valor_pt(request.args.get('u0', None))
        v0 = obtiene_valor_pt(request.args.get('v0', None))
        if u0!=None and v0!=None :
            fig = graph.param_desc_pt_uv(sup, u, v, u0, v0, dom_u=dom_u, dom_v=dom_v)
            return fig.to_html(include_mathjax="cdn")
        
        x0 = obtiene_valor_pt(request.args.get('x0', None))
        y0 = obtiene_valor_pt(request.args.get('y0', None))
        z0 = obtiene_valor_pt(request.args.get('z0', None))
        if x0!=None and y0!=None and z0!=None:
            fig = graph.param_desc_pt_xyz(sup, u, v, x0, y0, z0, dom_u=dom_u, dom_v=dom_v)
            return fig.to_html(include_mathjax="cdn")

        fig = graph.sup_param(sup, u, v, dom_u=dom_u, dom_v=dom_v)
        return fig.to_html(include_mathjax="cdn")
    


"""
-------------------------------------------------------------------------------
ENDPOINTS SUPERFICIE IMPLICITA
-------------------------------------------------------------------------------
"""
imp_surf_bp = Blueprint('implicita', __name__)

#FUNCION AUXILIARES
def procesar_solicitud_imp(func: callable, func_pt: callable, dict2latex: callable, dict2latex_pt: callable, txth: str='') -> dict:
    """
    Procesa una solicitud
    Argumentos:
    func                funcion a ejecutar sin punto especifico
    func_pt             funcion a ejecutar con punto especifico en función de x,y,z
    dict2latex          funcion que convierte el resultado a latex
    """
    #Se obtiene los parametros de la solicitud
    superficie_str  = request.args.get('superficie', None)
    func_str = request.args.getlist('func')
    
    if not superficie_str:
        return {'pasos': [{"descripcion": txth, "paso": "", "pasoLatex": "" }]}

    #Se consigue la parametrización de la superficie convertida a objeto sympy
    try:
        superficie, x, y, z = normaliza_implicita(superficie_str, request.args.getlist('const'), func_str)
    except Exception as e:
        # TODO: ¿Qué hacer si hay un error?
        raise e
    
    resultados = {
        'sup' : superficie,
        'x' : x,
        'y' : y,
        'z' : z
    }
    
    #Se comprueba si la superficie es regular (solo si se tiene una superficies sin funciones)
    if func_str == [] and not calci.esSupNivel(resultados):
        raise Exception("La superficie implicita no es superficie de nivel")
    
    #Se obtiene el punto a clasificar si hubiese y se devuelve los resultados
    x0 = obtiene_valor_pt(request.args.get('x0', None))
    y0 = obtiene_valor_pt(request.args.get('y0', None))
    z0 = obtiene_valor_pt(request.args.get('z0', None))
    if x0!=None and y0!=None and z0!=None:
        resultados['x0'] = x0
        resultados['y0'] = y0
        resultados['z0'] = z0
        func_pt(resultados)
        return {'pasos': dict2latex_pt(resultados)}
    
    func(resultados)
    return {'pasos': dict2latex(resultados)}

def normaliza_implicita(sup: str, consts: list, funcs: list) -> tuple:
    """
    Transforma la parametrización de una superficie a una expresion sympy con sus variable correspondientes
    No se hacen comprobaciones de tipo

    Argumentos:
    sup                 string con la ecuación de la superficie
    consts              lista de strings con constantes y su descripción
    func                lista de strings con funciones y su descripción
    """
    x = sp.symbols('x', real=True)
    y = sp.symbols('y', real=True)
    z = sp.symbols('z', real=True)

    variables = {'x':x, 'y':y, 'z':z}

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


#ENDPOINTS
@imp_surf_bp.route('/vector_normal')
def vector_normal():
    return jsonify(procesar_solicitud_imp(calci.normal, calci.normal_pt, txsimplres.res_vect_normal, txsimplres.res_vect_normal_pt, txsimplth.TH_VEC_NORMAL))

@imp_surf_bp.route('/plano_tangente')
def plano_tangente():
    return jsonify(procesar_solicitud_imp(calci.tangente, calci.tangente_pt, txsimplres.res_plano_tangente, txsimplres.res_plano_tangente_pt, txsimplth.TH_PLANO_TANG))

@imp_surf_bp.route('/grafica')
def grafica():
    superficie_str  = request.args.get('superficie', None)
    if superficie_str == None:
        #TODO_ Devolver teoría
        raise Exception("No se ha encontrado la superficie")
    else:
        x = sp.symbols('x', real=True)
        y = sp.symbols('y', real=True)
        z = sp.symbols('z', real=True)

        variables = {'x':x, 'y':y, 'z':z}

        try:
            superficie = sp.sympify(superficie_str, locals=variables)
        except Exception as e:
            # TODO: ¿Qué hacer si hay un error?
            raise e
        
        if not superficie.free_symbols.issubset(set([variables['x'], variables['y'], variables['z']])):
            raise Exception("Se han detectado variables no permitidas, solo se permiten x, y, z")
        
        resultados = {
            'sup' : superficie,
            'x' : x,
            'y' : y,
            'z' : z
        }

        #Compruebo que es una superficie de nivel
        if not calci.esSupNivel(resultados):
            raise Exception("No es superficie de nivel")

        #Extraigo el dominio donde se quiere considerar la superficie, si no hay o son los reales de pone [-5, 5]
        dom_x = extrae_dominio(request.args.get('dom_x', None))
        if dom_x==sp.S.Reals or not isinstance(dom_x, sp.Interval):
            dom_x = sp.Interval(-5, 5)
        dom_y = extrae_dominio(request.args.get('dom_y', None))
        if dom_y==sp.S.Reals or not isinstance(dom_y, sp.Interval):
            dom_y = sp.Interval(-5, 5)
        dom_z = extrae_dominio(request.args.get('dom_z', None))
        if dom_z==sp.S.Reals or not isinstance(dom_z, sp.Interval):
            dom_z = sp.Interval(-5, 5)

        x0 = obtiene_valor_pt(request.args.get('x0', None))
        y0 = obtiene_valor_pt(request.args.get('y0', None))
        z0 = obtiene_valor_pt(request.args.get('z0', None))
        if x0!=None and y0!=None and z0!=None:
            fig = graph.imp_desc_pt(superficie, x, y, z, x0, y0, z0,
                                   dom_x=dom_x, dom_y=dom_y, dom_z=dom_z)
            return fig.to_html(include_mathjax="cdn")
        
        fig = graph.sup_imp(superficie, x, y, z,
                            dom_x=dom_x, dom_y=dom_y, dom_z=dom_z,
                            titulo=r'$'+sp.latex(superficie)+r'=0$')
        return fig.to_html(include_mathjax="cdn")






app.register_blueprint(param_surf_bp, url_prefix='/param_surf')
app.register_blueprint(imp_surf_bp, url_prefix='/imp_surf')

if __name__ == '__main__':
    app.run(debug=True)