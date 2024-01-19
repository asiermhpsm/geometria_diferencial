from flask import Flask, request
import sympy as sp
from utils import *

"""
-------------------------------------------------------------------------------
FUNCIONES AUXILIARES
-------------------------------------------------------------------------------
"""

def normaliza_parametrizacion(var1, var2, sup, consts):
    """
    Transforma la parametrización de una superficie a una expresion sympy con sus variable correspondientes
    No se hacen comprobaciones de tipo

    Argumentos:
    var1                string con la primera variable de la parametrización
    var2                string con la segunda variable de la parametrización
    sup                 string con la parametrización de la superficie
    """
    variables = {}

    if not var1:
        var1='u'
    u = sp.symbols(var1)
    variables[var1] = u

    if not var2:
        var2='v'
    v = sp.symbols(var2)
    variables[var2] = v

    if consts:
        for elem in consts:
            partes  = elem.strip('[]').split(',')
            nombre_variable = partes[0].strip()
            opciones = partes[1:]
            opciones_dict = {}
            for opcion in opciones:
                opciones_dict[opcion.strip()] = True
            variables[nombre_variable] = sp.symbols(nombre_variable, **opciones_dict)

    elementos_str = sup.strip('[]').split(',')
    try:
        superficie = [sp.sympify(elem, locals=variables) for elem in elementos_str]
    except Exception as e:
        raise Exception(f"Error al procesar la superficie: {e}")
    if len(superficie) != 3:
        raise Exception(f"La parametrización de la superficie debe tener 3 elementos pero se han encontrado {len(superficie)}")
    
    return superficie, u, v

"""
-------------------------------------------------------------------------------
ENDPOINTS
-------------------------------------------------------------------------------
"""
app = Flask(__name__)

@app.route('/primera_forma_fundamental')
def primera_forma_fundamental():
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')
    const_str = request.args.getlist('const')
    
    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str, const_str)
    except Exception as e:
        #TODO-que hacer si hay error?
        raise e
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        return str(primeraFormaFundamental_pt_uv(superficie, u, v, u0, v0))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        return str(primeraFormaFundamental_pt_xyz(superficie, u, v, x0, y0, z0))
    
    return str(primeraFormaFundamental(superficie, u, v))

@app.route('/segunda_forma_fundamental')
def segunda_forma_fundamental():
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')
    const_str = request.args.getlist('const')
    
    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str, const_str)
    except Exception as e:
        #TODO-que hacer si hay error?
        raise e
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        return str(segundaFormaFundamental_pt_uv(superficie, u, v, u0, v0))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        return str(segundaFormaFundamental_pt_xyz(superficie, u, v, x0, y0, z0))
    
    return str(segundaFormaFundamental(superficie, u, v))

@app.route('/curvatura_Gauss')
def curvatura_Gauss():
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')
    const_str = request.args.getlist('const')
    
    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str, const_str)
    except Exception as e:
        #TODO-que hacer si hay error?
        raise e
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        return str(curvaturaGauss_pt_uv(superficie, u, v, u0, v0))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        return str(curvaturaGauss_pt_xyz(superficie, u, v, x0, y0, z0))
    
    return str(curvaturaGauss(superficie, u, v))

@app.route('/curvatura_media')
def curvatura_media():
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')
    const_str = request.args.getlist('const')

    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str, const_str)
    except Exception as e:
        #TODO-que hacer si hay error?
        raise e
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        return str(curvaturaMedia_pt_uv(superficie, u, v, u0, v0))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        return str(curvaturaMedia_pt_xyz(superficie, u, v, x0, y0, z0))
    
    return str(curvaturaMedia(superficie, u, v))

@app.route('/curvaturas_principales')
def curvaturas_principales():
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')
    const_str = request.args.getlist('const')

    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str, const_str)
    except Exception as e:
        #TODO-que hacer si hay error?
        raise e
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        return str(curvaturasPrincipales_pt_uv(superficie, u, v, u0, v0))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        return str(curvaturasPrincipales_pt_xyz(superficie, u, v, x0, y0, z0))

    
    return str(curvaturasPrincipales(superficie, u, v))

@app.route('/vector_normal')
def vector_normal():
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')
    const_str = request.args.getlist('const')
    
    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str, const_str)
    except Exception as e:
        #TODO-que hacer si hay error?
        raise e
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        return str(normal_pt_uv(superficie, u, v, u0, v0))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        return str(normal_pt_xyz(superficie, u, v, x0, y0, z0))
    
    return str(normal(superficie, u, v))

@app.route('/clasificacion_punto')
def clasificacion_punto():
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')
    const_str = request.args.getlist('const')
    
    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str, const_str)
    except Exception as e:
        #TODO-que hacer si hay error?
        raise e
    
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
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')
    const_str = request.args.getlist('const')
    
    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str, const_str)
    except Exception as e:
        #TODO-que hacer si hay error?
        raise e
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        return str(planoTangente_pt_uv(superficie, u, v, u0, v0))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        return str(planoTangente_pt_xyz(superficie, u, v, x0, y0, z0))
    print(planoTangente(superficie, u, v))
    return str(planoTangente(superficie, u, v))

@app.route('/direcciones_principales')
def direcciones_principales():
    # TODO
    return ''

@app.route('/representacion')
def representar():
    # TODO
    return ''


if __name__ == '__main__':
    app.run(debug=True)