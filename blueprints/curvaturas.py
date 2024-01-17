from flask import Blueprint, request
from .utils import normaliza_parametrizacion

curvaturas_bp = Blueprint('curvaturas', __name__)

@curvaturas_bp.route('/curvatura_Gauss')
def curvatura_Gauss():
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')
    
    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str)
    except Exception as e:
        #TODO-que hacer si hay error?
        raise e
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        #return str(curvaturaGauss_pt_uv(superficie, u, v, u0, v0))
        print()

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        #return str(curvaturaGauss_pt_xyz(superficie, u, v, x0, y0, z0))
        print()
    
    #return str(curvaturaGauss(superficie, u, v))
    return str(superficie)

@curvaturas_bp.route('/curvatura_media')
def curvatura_media():
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')

    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str)
    except Exception as e:
        #TODO-que hacer si hay error?
        raise e
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        #return str(curvaturaMedia_pt_uv(superficie, u, v, u0, v0))
        print()

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        #return str(curvaturaMedia_pt_xyz(superficie, u, v, x0, y0, z0))
        print()
    
    #return str(curvaturaMedia(superficie, u, v))
    return str(superficie)

@curvaturas_bp.route('/curvaturas_principales')
def curvaturas_principales():
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')

    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str)
    except Exception as e:
        #TODO-que hacer si hay error?
        raise e
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        #return str(curvaturasPrincipales_pt_uv(superficie, u, v, u0, v0))
        print()

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        #return str(curvaturasPrincipales_pt_xyz(superficie, u, v, x0, y0, z0))
        print()
    
    #return str(curvaturasPrincipales(superficie, u, v))
    return str(superficie)





