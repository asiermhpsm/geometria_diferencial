
def dirAsin_pt(res):

    if res['e_pt']==0 and res['f_pt']==0 and res['g_pt']==0:
        x0, y0 = sp.symbols('x0 y0', real=True)
        res['Dirs_asint'] = [sp.Matrix([x0, y0]).T]
    elif res['e_pt']==0:
        res['Dirs_asint'] = [sp.Matrix([1, 0]).T, sp.Matrix([-res['g_pt'], 2*res['f_pt']]).T]
    elif res['g_pt']==0:
        res['Dirs_asint'] = [sp.Matrix([0, 1]).T, sp.Matrix([-2*res['f_pt'], -res['e_pt'], ]).T]
    elif res['f_pt']**2- res['g_pt']*res['e_pt'] < 0:
        res['Dirs_asint'] = []
    else:
        raiz = sp.sqrt(res['f_pt']**2- res['g_pt']*res['e_pt'])
        res['Dirs_asint'] = [sp.Matrix([res['g_pt'], -res['f_pt']+raiz]).T, sp.Matrix([res['g_pt'], -res['f_pt']-raiz]).T]


from utils.calc_param import segundaFormaFundamental, segundaFormaFundamental_pt_uv
import sympy as sp
import numpy as np
import plotly.graph_objects as go

"""u, v = sp.symbols('u v', real=True)
parab_hiper = sp.Matrix([u, v, u**2-v**2]).T
res = { 'sup' : parab_hiper, 'u' : u, 'v' : v }
segundaFormaFundamental(res)
II = sp.Matrix([[res['e'],res['f']],[res['f'], res['g']]])
print(II)
print(direcciones_asintoticas(II))"""

u, v = sp.symbols('u v', real=True)
parab_hiper = sp.Matrix([sp.cos(u), sp.sin(u), v]).T
dom_u = sp.Interval(0,2*sp.pi)
dom_v = sp.Interval(-2,2)
res = { 'sup' : parab_hiper, 'u' : u, 'v' : v, 'u0' : 0, 'v0' : 0, 'dom_u' : dom_u, 'dom_v' : dom_v}
segundaFormaFundamental_pt_uv(res)
dirAsin_pt(res)
dirs = res['Dirs_asint']

from utils.graph import sup_param, point
fig = sup_param(res['sup'], res['u'], res['v'], dom_u, dom_v)
punto = res['sup'].subs({res['u']:res['u0'], res['v']:res['v0']})
point(punto, fig=fig, titulo='Punto')
colores = ['black', 'brown', 'purple', 'yellow']
t = sp.symbols('t', real=True)
for i, dir in enumerate(dirs):
    if isinstance(dir[0], sp.Symbol):
        continue

    puntos_posibles = set()
    ti = (res['dom_u'].start-res['u0'])/dir[0]
    puntos_posibles.add((res['u0']+ti*dir[0], res['v0']+ti*dir[1]))
    ti = (res['dom_v'].start-res['v0'])/dir[1]
    puntos_posibles.add((res['u0']+ti*dir[0], res['v0']+ti*dir[1]))
    ti = (res['dom_u'].end-res['u0'])/dir[0]
    puntos_posibles.add((res['u0']+ti*dir[0], res['v0']+ti*dir[1]))
    ti = (res['dom_v'].end-res['v0'])/dir[1]
    puntos_posibles.add((res['u0']+ti*dir[0], res['v0']+ti*dir[1]))
    puntos = [pto for pto in puntos_posibles if pto[0] in res['dom_u'] and pto[1] in res['dom_v']]
    puntos = [sp.Matrix(pto).T for pto in puntos]
    if len(puntos)!=2:
        raise Exception('Error en la dirección asintótica')
    p1, p2 = puntos
    linea = p1 + t*(p2-p1)

    curva = list(res['sup'].subs({res['u']:linea[0], res['v']:linea[1]}))
    func_curva = sp.lambdify(t, curva, 'numpy')
    t_values = np.linspace(0, 1, 50)
    X, Y, Z = func_curva(t_values)
    if np.isscalar(X): X = np.full_like(t_values, X)
    if np.isscalar(Y): Y = np.full_like(t_values, Y)
    if np.isscalar(Z): Z = np.full_like(t_values, Z)
    fig.add_trace(
        go.Scatter3d(x=X, y=Y, z=Z, 
                     mode='lines', 
                     name=f'Dir. asintótica {i+1}', 
                     line=dict(color=colores[i], width=10)))
    fig.update_layout(scene=dict(aspectmode='data'))

fig.show() 
