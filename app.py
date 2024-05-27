from flask import Flask, request, jsonify, Blueprint, Response
from flask_cors import CORS, cross_origin
import flask

import sympy as sp
import re

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

def respuesta_error(error: str) -> flask.Response:
    """
    Devuelve una respuesta de error con el mensaje pasado

    Argumentos:
    error               string con el mensaje de error
    """
    return Response(error, 400)

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
def procesar_solicitud_param(func: callable, func_pt_uv: callable, dict2latex: callable, dict2latex_pt: callable, txth: str='') -> dict:
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
        return {'titulo': 'Superficie parametrizada', 'descripcion' : txth, 'algoritmo': txth}


    #Se consigue la parametrización de la superficie convertida a objeto sympy
    func_str = request.args.getlist('func')

    dom_u = extrae_dominio(request.args.get('dom_var1', None))
    var1 = request.args.get('var1', None)
    if dom_u.start>=0 and dom_u.end>=0:
        var1 = '[u,positive]' if var1 == None else '['+ var1 + ',positive]'
    elif dom_u.start<=0 and dom_u.end<=0:
        var1 = '[u,negative]' if var1 == None else '['+ var1 + ',negative]'

    dom_v = extrae_dominio(request.args.get('dom_var2', None))
    var2 = request.args.get('var2', None)
    if dom_u.start>=0 and dom_u.end>=0:
        var2 = '[v,positive]' if var2 == None else '['+ var2 + ',positive]'
    elif dom_u.start<=0 and dom_u.end<=0:
        var2 = '[v,negative]' if var2 == None else '['+ var2 + ',negative]'

    try:
        superficie, variables = normaliza_parametrizacion(var1, var2, superficie_str, request.args.getlist('const'), func_str)
    except Exception as e:
        return respuesta_error(str(e))

    resultados = {
        'sup' : superficie,
        'u' : variables['u'],
        'v' : variables['v'],
        'dom_u' : dom_u,
        'dom_v' : dom_v
    }

    #Dominio en forma de elipse
    cond_str = request.args.get('cond', None)
    if cond_str != None:
        try:
            sy_cond = sp.sympify(cond_str, locals=variables)
            if sy_cond.free_symbols.issubset(set([variables['u'], variables['v']])) and isinstance(sy_cond, sp.StrictLessThan):
                expr = sy_cond.lhs - sy_cond.rhs
                a = expr.coeff(variables['u']**2)
                b = expr.coeff(variables['v']**2)
                if a==0 or b==0:
                    return respuesta_error('El dominio en forma de elipse debe cumplir que a!=0 y b!=0')
                r = expr - a*variables['u']**2 - b*variables['v']**2
                if r.is_constant():
                    resultados['cond'] = sy_cond
            else:
                return respuesta_error('El dominio en forma de elipse no puede contener constantes en su fórmula y debe ser una desigualdad estricta')
        except Exception as e:
            return respuesta_error(f'Error al procesar el dominio en forma de elipse: {str(e)}')
    
    #Se comprueba si la superficie es regular (solo si se tiene una superficies sin funciones)
    if not calcp.esRegular(resultados):
        return respuesta_error("La superficie parametrizada no es regular")
    
    #Se obtiene el punto a clasificar si hubiese y se devuelve los resultados
    u0 = obtiene_valor_pt(request.args.get('u0', None))
    v0 = obtiene_valor_pt(request.args.get('v0', None))
    if u0!=None and v0!=None :
        resultados['u0'] = u0
        resultados['v0'] = v0
        func_pt_uv(resultados)
        if 'cond' in resultados:
            calcp.simplifica_resultados_cond(resultados)
        elif request.args.get('trig', None)!=None:
            calcp.simplifica_resultados_trig(resultados)
        return jsonify({'pasos': dict2latex_pt(resultados)})
    
    if func==None:
        return respuesta_error("No se ha definido correctamente el punto")
    
    func(resultados)
    if 'cond' in resultados:
        calcp.simplifica_resultados_cond(resultados)
    elif request.args.get('trig', None)!=None:
        calcp.simplifica_resultados_trig(resultados)
    return jsonify({'pasos': dict2latex(resultados)})

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
    variables_sup = {}

    #Se obtiene la primera variable de la parametrización, por defecto es 'u'. Siempre real
    opciones = {}
    if not var1: var1='u'
    elif ',' in var1: var1, opciones = extrae_opciones_var(var1)
    opciones['real'] = True
    u = sp.symbols(var1, **opciones)
    variables[var1] = u
    variables_sup['u'] = u

    #Se obtiene la segunda variable de la parametrización, por defecto es 'v'. Siempre real
    opciones = {}
    if not var2: var2='v'
    elif ',' in var2: var2, opciones = extrae_opciones_var(var2)
    opciones['real'] = True
    v = sp.symbols(var2, **opciones)
    variables[var2] = v
    variables_sup['v'] = v

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
            return sp.Matrix([sp.sympify(elem, locals=variables) for elem in superficie]).T, variables_sup
        except Exception as e:
            raise Exception(f"Error al procesar la superficie: {e}")
    else:
        raise Exception(f"Error al procesar la superficie: {sup}")


#ENDPOINTS
@param_surf_bp.route('/vector_normal')
def vector_normal():
    return procesar_solicitud_param(calcp.normal, calcp.normal_pt_uv, txparamres.res_vect_normal, txparamres.res_vect_normal_pt, txparamth.TH_VEC_NORMAL)

@param_surf_bp.route('/plano_tangente')
def plano_tangente():
    return procesar_solicitud_param(calcp.planoTangente, calcp.planoTangente_pt_uv, txparamres.res_plano_tangente, txparamres.res_plano_tangente_pt, txparamth.TH_PLANO_TANG)

@param_surf_bp.route('/primera_forma_fundamental')
def primera_forma_fundamental():
    return procesar_solicitud_param(calcp.primeraFormaFundamental, calcp.primeraFormaFundamental_pt_uv, txparamres.res_PFF, txparamres.res_PFF_pt, txparamth.TH_PFF)

@param_surf_bp.route('/segunda_forma_fundamental')
def segunda_forma_fundamental():
    return procesar_solicitud_param(calcp.segundaFormaFundamental, calcp.segundaFormaFundamental_pt_uv, txparamres.res_SFF, txparamres.res_SFF_pt, txparamth.TH_SFF)

@param_surf_bp.route('/weingarten')
def weingarten():
    return procesar_solicitud_param(calcp.weingarten, calcp.weingarten_pt_uv, txparamres.res_Weingarten, txparamres.res_Weingarten_pt, txparamth.TH_WEINGARTEN)

@param_surf_bp.route('/curvatura_Gauss')
def curvatura_Gauss():
    return procesar_solicitud_param(calcp.curvaturaGauss, calcp.curvaturaGauss_pt_uv, txparamres.res_curv_Gauss, txparamres.res_curv_Gauss_pt, txparamth.TH_CURV_GAUSS)

@param_surf_bp.route('/curvatura_media')
def curvatura_media():
    return procesar_solicitud_param(calcp.curvaturaMedia, calcp.curvaturaMedia_pt_uv, txparamres.res_curv_media, txparamres.res_curv_media_pt, txparamth.TH_CURV_MEDIA)

@param_surf_bp.route('/curvaturas_principales')
def curvaturas_principales():
    return procesar_solicitud_param(calcp.curvaturasPrincipales, calcp.curvaturasPrincipales_pt_uv, txparamres.res_curvs_principales, txparamres.res_curvs_principales_pt, txparamth.TH_CURVS_PRINCIPALES)

@param_surf_bp.route('/direcciones_principales')
def direcciones_principales():
    return procesar_solicitud_param(calcp.dirPrinc, calcp.dirPrinc_pt_uv, txparamres.res_dirs_principales, txparamres.res_dirs_principales_pt, txparamth.TH_DIRS_PRINCIPALES)

@param_surf_bp.route('/punto_umbilico')
def punto_umbilico():
    return procesar_solicitud_param(None, calcp.umbilico_pt_uv, txparamres.res_ptos_umbilicos, txparamres.res_ptos_umbilicos_pt, txparamth.TH_PTS_UMBILICOS)

@param_surf_bp.route('/clasificacion_punto')
def clasificacion_punto():
    return procesar_solicitud_param(None, calcp.clasicPt_uv, calcp.clasicPt_xyz, None, txparamres.res_clasif_pt, txparamth.TH_CLASIFICACION_PTOS)

@param_surf_bp.route('/direccion_asintotica')
def direccion_asintotica():
    return procesar_solicitud_param(None, calcp.dirAsin_pt_uv, None, txparamres.res_dirs_asint, txparamth.TH_DIRS_ASINTOTICAS)

@param_surf_bp.route('/description')
def description():
    return procesar_solicitud_param(calcp.descripccion, calcp.descripccion_pt_uv, txparamres.res_analisis_completo, txparamres.res_analisis_completo_pt, txparamth.TH_ANALISIS)

@param_surf_bp.route('/grafica')
def grafica():
    superficie_str  = request.args.get('superficie', None)
    if superficie_str == None:
        return respuesta_error("No se ha encontrado la parametrización de la superficie")
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
                sup = sp.Matrix([sp.sympify(elem, locals=variables) for elem in superficie]).T
            except Exception as e:
                return respuesta_error(f"Error al procesar la superficie: {e}")
        else:
            return respuesta_error(f"Error al procesar la superficie: {superficie_str}")
        
        if not sup.free_symbols.issubset(set([u, v])):
            return respuesta_error(f"Se han detectado variables no permitidas, solo se permiten {u},{v}")

        #Se analiza si el dominio de la variables es de la forma a*u+b*v<r
        a = None
        b = None
        cond_str = request.args.get('cond', None)
        if cond_str!=None:
            try:
                sy_cond = sp.sympify(cond_str, locals=variables)
                if sy_cond.free_symbols.issubset(set([u, v])) and isinstance(sy_cond, sp.StrictLessThan):
                    expr = sy_cond.lhs - sy_cond.rhs
                    a = expr.coeff(u**2)
                    b = expr.coeff(v**2)
                    r = expr - a*u**2 - b*v**2
                    if r.is_constant():
                        a = a/-r
                        b = b/-r
            except Exception as e:
                return respuesta_error(f'Error al procesar el dominio en forma de elipse: {str(e)}')

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
            return respuesta_error("La superficie parametrizada no es regular")

        u0 = obtiene_valor_pt(request.args.get('u0', None))
        v0 = obtiene_valor_pt(request.args.get('v0', None))
        if u0!=None and v0!=None :
            tangente = request.args.get('tangente', None)!=None
            normal = request.args.get('normal', None)!=None
            dirs_principales = request.args.get('dirs_principales', None)!=None
            curvs_principales = request.args.get('curvs_principales', None)!=None
            dirs_asintoticas = request.args.get('dirs_asintoticas', None)!=None
            fig = graph.param_desc_pt_uv(sup, u, v, u0, v0, dom_u=dom_u, dom_v=dom_v, a=a, b=b, 
                                         tangente=tangente, normal=normal, dirs_principales=dirs_principales, 
                                         curvs_principales=curvs_principales, dirs_asintoticas=dirs_asintoticas)
        elif a!=None and b!=None:
            fig = graph.sup_param_cond_elipse(sup, u, v, a, b, titulo=r'$\vec{\varphi}='+sp.latex(sup, mat_delim='(')+r'$')
        else:
            fig = graph.sup_param(sup, u, v, dom_u=dom_u, dom_v=dom_v, titulo=r'$\vec{\varphi}='+sp.latex(sup, mat_delim='(')+r'$')
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
        return {'titulo': 'Superficie implicita', 'descripcion' : txth, 'algoritmo': txth}

    #Se consigue la parametrización de la superficie convertida a objeto sympy
    try:
        superficie, x, y, z = normaliza_implicita(superficie_str, request.args.getlist('const'), func_str)
    except Exception as e:
        return respuesta_error(str(e))
    
    resultados = {
        'sup' : superficie,
        'x' : x,
        'y' : y,
        'z' : z
    }
    
    #Se comprueba si la superficie es regular (solo si se tiene una superficies sin funciones)
    if not calci.esSupNivel(resultados):
        return respuesta_error("La superficie implicita no es superficie de nivel")
    
    #Se obtiene el punto a clasificar si hubiese y se devuelve los resultados
    x0 = obtiene_valor_pt(request.args.get('x0', None))
    y0 = obtiene_valor_pt(request.args.get('y0', None))
    z0 = obtiene_valor_pt(request.args.get('z0', None))
    if x0!=None and y0!=None and z0!=None:
        resultados['x0'] = x0
        resultados['y0'] = y0
        resultados['z0'] = z0
        valor = superficie.subs({x:x0, y:y0, z:z0})
        try:
            if sp.Abs(valor)>0.1:
                return respuesta_error(f'El punto {x0, y0, z0} no pertenece a la superficie {superficie_str}=0 ya que {valor} no es 0')
        except:
            return respuesta_error('No se ha podido establecer si el punto pertenece a la superficie')
        func_pt(resultados)
        return jsonify({'pasos': dict2latex_pt(resultados)})
    
    func(resultados)
    return jsonify({'pasos': dict2latex(resultados)})

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
    return procesar_solicitud_imp(calci.normal, calci.normal_pt, txsimplres.res_vect_normal, txsimplres.res_vect_normal_pt, txsimplth.TH_VEC_NORMAL)

@imp_surf_bp.route('/plano_tangente')
def plano_tangente():
    return procesar_solicitud_imp(calci.tangente, calci.tangente_pt, txsimplres.res_plano_tangente, txsimplres.res_plano_tangente_pt, txsimplth.TH_PLANO_TANG)

@imp_surf_bp.route('/description')
def description():
    return procesar_solicitud_imp(calci.descripccion, calci.descripccion_pt_uv, txsimplres.res_analisis_completo, txsimplres.res_analisis_completo_pt, txsimplth.TH_ANALISIS)

@imp_surf_bp.route('/grafica')
def grafica():
    superficie_str  = request.args.get('superficie', None)
    if superficie_str == None:
        return respuesta_error("No se ha encontrado la superficie")
    else:
        x = sp.symbols('x', real=True)
        y = sp.symbols('y', real=True)
        z = sp.symbols('z', real=True)

        variables = {'x':x, 'y':y, 'z':z}

        try:
            superficie = sp.sympify(superficie_str, locals=variables)
        except Exception as e:
            return respuesta_error(f"Error al procesar la superficie: {e}")
        
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
            tangente = request.args.get('tangente', None)!=None
            normal = request.args.get('normal', None)!=None
            fig = graph.imp_desc_pt(superficie, x, y, z, x0, y0, z0,dom_x=dom_x, dom_y=dom_y, dom_z=dom_z, tangente=tangente, normal=normal)
        else:
            fig = graph.sup_imp(superficie, x, y, z,dom_x=dom_x, dom_y=dom_y, dom_z=dom_z,titulo=r'$'+sp.latex(superficie)+r'=0$')
        return fig.to_html(include_mathjax="cdn")






app.register_blueprint(param_surf_bp, url_prefix='/param_surf')
app.register_blueprint(imp_surf_bp, url_prefix='/imp_surf')

if __name__ == '__main__':
    app.run(debug=True)