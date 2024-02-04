from flask import Flask, request, send_file, jsonify, render_template
import io
import json
from PIL import Image
import sympy as sp
import numpy as np
import re

#from sympy.core.assumptions import assumptions
#print(assumptions(variables[nombre_func]))

import plotly.graph_objects as go

from mayavi import mlab

from matplotlib.image import imsave
#from matplotlib import colormaps
#import matplotlib.colors as mcolors

from utils import *
#from utils_graph import *
from utils_graph_plotly import *

mlab.options.offscreen = True

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
#colormapas = list(colormaps)
#colores = list(mcolors.BASE_COLORS.keys())+list(mcolors.TABLEAU_COLORS.keys()) + list(mcolors.CSS4_COLORS.keys()) + list(mcolors.XKCD_COLORS.keys())

def procesar_parametrizacion():
    """
    Procesa una solicitud
    """
    var1 = request.args.get('var1', None)
    var2 = request.args.get('var2', None)
    superficie_str  = request.args.get('superficie')
    const_str = request.args.getlist('const')
    func_str = request.args.getlist('func')
    
    if not superficie_str:
        raise Exception("No se ha encontrado la parametrización de la superficie")

    try:
        superficie, u, v = normaliza_parametrizacion(var1, var2, superficie_str, const_str, func_str)
    except Exception as e:
        # TODO: ¿Qué hacer si hay un error?
        raise e

    return superficie, u, v

def normaliza_parametrizacion(var1, var2, sup, consts, func):
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

    if not var1:
        var1='u'
    u = sp.symbols(var1, real=True)
    variables[var1] = u

    if not var2:
        var2='v'
    v = sp.symbols(var2, real=True)
    variables[var2] = v

    #https://docs.sympy.org/latest/guides/assumptions.html#predicates
    #https://docs.sympy.org/latest/modules/core.html#module-sympy.core.assumptions
    if consts:
        for elem in consts:
            elem = elem.replace(' ', '')
            partes  = elem.strip('[]').split(',')
            nombre_variable = partes[0].strip()
            opciones = partes[1:]
            opciones_dict = {}
            for opcion in opciones:
                if opcion.strip() in OPCIONES_VAR:
                    opciones_dict[opcion.strip()] = True
            opciones_dict['real'] = True
            variables[nombre_variable] = sp.symbols(nombre_variable, **opciones_dict)
    
    if func:
        for elem in func:
            elem = elem.replace(' ', '')
            partes  = elem.strip('[]').split(')')
            definicion_func = re.split(r'[(),]', partes[0])
            definicion_func = [elemento.strip() for elemento in definicion_func if elemento.strip() != '']
            nombre_func = definicion_func[0]
            variables_func = [variables[var] for var in definicion_func[1:]]
            descripciones = partes[1].split(',')
            descripciones_dict = {}
            for descripcion in descripciones:
                if descripcion in OPCIONES_VAR:
                    descripciones_dict[descripcion] = True
            descripciones_dict['real'] = True
            variables[nombre_func] = sp.Function(nombre_func, **descripciones_dict)(*variables_func)

    elementos_str = sup.strip('[]').split(',')
    try:
        superficie = [sp.sympify(elem, locals=variables) for elem in elementos_str]
    except Exception as e:
        raise Exception(f"Error al procesar la superficie: {e}")
    if len(superficie) != 3:
        raise Exception(f"La parametrización de la superficie debe tener 3 elementos pero se han encontrado {len(superficie)}")
    
    return sp.Matrix(superficie), u, v

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


def grafica_sup_param(sup, u, v, limite_inf_u, limite_sup_u, limite_inf_v, limite_sup_v):
    parametric_surface = sp.lambdify((u, v), sup, 'numpy')
    u_values = np.linspace(float(limite_inf_u), float(limite_sup_u), 100)
    v_values = np.linspace(float(limite_inf_v), float(limite_sup_v), 100)
    u_values, v_values = np.meshgrid(u_values, v_values)
    x, y, z = parametric_surface(u_values, v_values)
    mlab.mesh(x, y, z, color=(0.2980392156862745, 0.4470588235294118, 0.6901960784313725))
    return max(float(np.max(x)), float(np.max(y)), float(np.max(z)))

def grafica_sup_ec(sup, x, y, z, limite_inf_x, limite_sup_x, limite_inf_y, limite_sup_y):
    parametric_surface = sp.lambdify((x, y, z), sup, 'numpy')
    x_vals, y_vals, z_vals = np.mgrid[limite_inf_x:limite_sup_x:100j, limite_inf_y:limite_sup_y:100j, -10:10:100j]
    values = parametric_surface(x_vals, y_vals, z_vals)
    mlab.contour3d(x_vals, y_vals, z_vals, values, contours=[0])

def grafica_punto(punto):
    mlab.points3d(*punto, color=(1, 0, 0), scale_factor=0.1, mode='sphere')

def grafica_vector(inicio, vector):
    mlab.quiver3d(*inicio, *vector, color=(0, 0, 1), scale_factor=1)


"""
-------------------------------------------------------------------------------
ENDPOINTS
-------------------------------------------------------------------------------
"""
app = Flask(__name__)

@app.route('/primera_forma_fundamental')
def primera_forma_fundamental():
    superficie, u, v = procesar_parametrizacion()
    resultados = {}

    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        primeraFormaFundamental_pt_uv(superficie, u, v, u0, v0, resultados)
        return jsonify(convertir_a_string(resultados))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        primeraFormaFundamental_pt_xyz(superficie, u, v, x0, y0, z0, resultados)
        return jsonify(convertir_a_string(resultados))
    
    primeraFormaFundamental(superficie, u, v, resultados)
    return jsonify(convertir_a_string(resultados))

@app.route('/segunda_forma_fundamental')
def segunda_forma_fundamental():
    superficie, u, v = procesar_parametrizacion()
    resultados = {}

    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        segundaFormaFundamental_pt_uv(superficie, u, v, u0, v0, resultados)
        return jsonify(convertir_a_string(resultados))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        segundaFormaFundamental_pt_xyz(superficie, u, v, x0, y0, z0, resultados)
        return jsonify(convertir_a_string(resultados))
    
    segundaFormaFundamental(superficie, u, v, resultados)
    return jsonify(convertir_a_string(resultados))

@app.route('/curvatura_Gauss')
def curvatura_Gauss():
    superficie, u, v = procesar_parametrizacion()
    resultados = {}
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        curvaturaGauss_pt_uv(superficie, u, v, u0, v0, resultados)
        return jsonify(convertir_a_string(resultados))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        curvaturaGauss_pt_xyz(superficie, u, v, x0, y0, z0, resultados)
        return jsonify(convertir_a_string(resultados))
    
    curvaturaGauss(superficie, u, v, resultados)
    return jsonify(convertir_a_string(resultados))

@app.route('/curvatura_media')
def curvatura_media():
    superficie, u, v = procesar_parametrizacion()
    resultados = {}
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        curvaturaMedia_pt_uv(superficie, u, v, u0, v0, resultados)
        return jsonify(convertir_a_string(resultados))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        curvaturaMedia_pt_xyz(superficie, u, v, x0, y0, z0, resultados)
        return jsonify(convertir_a_string(resultados))
    
    curvaturaMedia(superficie, u, v, resultados)
    return jsonify(convertir_a_string(resultados))

@app.route('/curvaturas_principales')
def curvaturas_principales():
    superficie, u, v = procesar_parametrizacion()
    resultados = {}
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        curvaturasPrincipales_pt_uv(superficie, u, v, u0, v0, resultados)
        return jsonify(convertir_a_string(resultados))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        curvaturasPrincipales_pt_xyz(superficie, u, v, x0, y0, z0, resultados)
        return jsonify(convertir_a_string(resultados))

    curvaturasPrincipales(superficie, u, v, resultados)
    return jsonify(convertir_a_string(resultados))

@app.route('/vector_normal')
def vector_normal():
    superficie, u, v = procesar_parametrizacion()
    resultados = {}

    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        normal_pt_uv(superficie, u, v, u0, v0, resultados)
        return jsonify(convertir_a_string(resultados))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        normal_pt_xyz(superficie, u, v, x0, y0, z0, resultados)
        return jsonify(convertir_a_string(resultados))
    
    normal(superficie, u, v, resultados)
    return jsonify(convertir_a_string(resultados))

@app.route('/clasificacion_punto')
def clasificacion_punto():
    superficie, u, v = procesar_parametrizacion()
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
    superficie, u, v = procesar_parametrizacion()
    resultados = {}
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        planoTangente_pt_uv(superficie, u, v, u0, v0, resultados)
        return jsonify(convertir_a_string(resultados))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        planoTangente_pt_xyz(superficie, u, v, x0, y0, z0, resultados)
        return jsonify(convertir_a_string(resultados))
    
    planoTangente(superficie, u, v, resultados)
    return jsonify(convertir_a_string(resultados))

@app.route('/direcciones_principales')
def direcciones_principales():
    superficie, u, v = procesar_parametrizacion()
    resultados = {}
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        dirPrinc_pt_uv(superficie, u, v, u0, v0, resultados)
        return jsonify(convertir_a_string(resultados))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        dirPrinc_pt_xyz(superficie, u, v, x0, y0, z0, resultados)
        return jsonify(convertir_a_string(resultados))

    dirPrinc(superficie, u, v, resultados)
    return jsonify(convertir_a_string(resultados))

@app.route('/description')
def description():
    superficie, u, v = procesar_parametrizacion()
    resultados = {}
    
    u0 = request.args.get('u0', None)
    v0 = request.args.get('v0', None)
    if u0 and v0:
        descripccion_pt_uv(superficie, u, v, u0, v0, resultados)
        return jsonify(convertir_a_string(resultados))

    x0 = request.args.get('x0', None)
    y0 = request.args.get('y0', None)
    z0 = request.args.get('z0', None)
    if x0 and y0 and z0:
        descripccion_pt_xyz(superficie, u, v, x0, y0, z0, resultados)
        return jsonify(convertir_a_string(resultados))

    descripccion(superficie, u, v, resultados)
    return jsonify(convertir_a_string(resultados))

@app.route('/grafica')
def grafica():
    fig = go.Figure()
    if '[' in request.args.get('superficie'):
        superficie, u, v = procesar_parametrizacion()
        fig = grafica_sup_param_plotly(superficie, u, v, 0, 2*sp.pi, 0, sp.pi, fig)
        fig.update_layout(
            scene=dict(
                aspectmode='data',
                aspectratio=dict(x=1, y=1, z=1)
            )
        )
        return render_template('grafica.html', plot=fig.to_html())
        return jsonify(json.loads(fig.to_json()))
    else:
        return 'Superficie nivel'
    
"""@app.route('/grafica')
def grafica():
    superficie, u, v = procesar_parametrizacion()
    resultados = {}

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    grafica_sup_param(ax,superficie,u,v,-sp.pi/2,sp.pi/2,0,2*sp.pi,{})
    ax.set_aspect('equal')
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    #data = base64.b64encode(buf.getbuffer()).decode("ascii")
    #return f"<img src='data:image/png;base64,{data}'/>"
    return send_file(io.BytesIO(buf.read()), mimetype='image/png')"""


"""
@app.route('/grafica')
def grafica():
    superficie, u, v = procesar_parametrizacion()
    resultados = {}
    
    maximo = grafica_sup_param(superficie,u,v,-sp.pi/2,sp.pi/2,0,2*sp.pi)
    print(maximo)

    mlab.plot3d([0, maximo], [0, 0], [0, 0], color=(1, 0, 0), tube_radius=None)
    mlab.plot3d([0, 0], [0, maximo], [0, 0], color=(0, 1, 0), tube_radius=None)
    mlab.plot3d([0, 0], [0, 0], [0, maximo], color=(0, 0, 1), tube_radius=None)
    
    buf1 = io.BytesIO()
    imsave(buf1, mlab.screenshot(antialiased=True), format='png')
    buf1.seek(0)

    mlab.view(azimuth=0, elevation=90, distance='auto')
    buf2 = io.BytesIO()
    imsave(buf2, mlab.screenshot(antialiased=True), format='png')
    buf2.seek(0)

    mlab.view(azimuth=90, elevation=0, distance='auto')
    buf3 = io.BytesIO()
    imsave(buf3, mlab.screenshot(antialiased=True), format='png')
    buf3.seek(0)

    mlab.view(azimuth=0, elevation=0, distance='auto')
    buf4 = io.BytesIO()
    imsave(buf4, mlab.screenshot(antialiased=True), format='png')
    buf4.seek(0)
    
    mlab.clf()
    mlab.close()

    image1 = Image.open(buf1)
    image2 = Image.open(buf2)
    image3 = Image.open(buf3)
    image4 = Image.open(buf4)

    width, height = image1.size
    combined_image = Image.new('RGB', (width * 2, height * 2))
    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (width, 0))
    combined_image.paste(image3, (0, height))
    combined_image.paste(image4, (width, height))

    combined_buf = io.BytesIO()
    combined_image.save(combined_buf, format='PNG')
    combined_buf.seek(0)

    return send_file(combined_buf, mimetype='image/png')
"""

if __name__ == '__main__':
    app.run(debug=True)