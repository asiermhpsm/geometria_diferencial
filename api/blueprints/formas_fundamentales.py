from flask import Blueprint, request
import sympy as sp

formas_fundamentales_bp = Blueprint('formas_fundamentales', __name__)

def normaliza_parametrizacion(var1, var2, sup):
    if var1:
        u = sp.symbols(var1, real = True)
    else:
        u = sp.symbols('u', real = True)
        var1='u'

    if var2:
        v = sp.symbols(var2, real = True)
    else:
        v = sp.symbols('v', real = True)
        var2='v'

    elementos_str = sup.strip('[]').split(',')
    try:
        superficie = [sp.sympify(elem, locals={var1: u, var2: v}) for elem in elementos_str]
    except Exception as e:
        raise Exception(f"Error al procesar la superficie: {e}")
    if len(superficie) != 3:
        raise Exception(f"La parametrización de la superficie debe tener 3 elementos pero se han encontrado {len(superficie)}")
    
    return superficie, u, v

@formas_fundamentales_bp.route('/primera_forma_fundamental')
def primera_forma_fundamental():
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
        #return str(primeraFormaFundamental_pt_uv(superficie, u, v, u0, v0))
        print()

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        #return str(primeraFormaFundamental_pt_xyz(superficie, u, v, x0, y0, z0))
        print()
    
    #return str(primeraFormaFundamental(superficie, u, v))
    return str(superficie)

@formas_fundamentales_bp.route('/segunda_forma_fundamental')
def segunda_forma_fundamental():
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
        #return str(segundaFormaFundamental_pt_uv(superficie, u, v, u0, v0))
        print()

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        #return str(segundaFormaFundamental_pt_xyz(superficie, u, v, x0, y0, z0))
        print()
    
    #return str(segundaFormaFundamental(superficie, u, v))
    return str(superficie)


