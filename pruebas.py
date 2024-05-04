
def direcciones_asintoticas(II):

    def equalVectors(v1, v2):
        return sp.Abs(v1.normalized().dot(v2.normalized())) == 1
    
    x,y = sp.symbols('x y', real=True)
    vec = sp.Matrix([x,y]).T
    pol = (vec*II*vec.T)[0]
    pol = sp.simplify(pol/(x**2))
    direcciones = []
    #Caso x=1
    pol1 = pol.subs(x,1)
    sol = sp.solve(sp.Eq(pol1,0), y)
    for i in sol:
        direcciones.append(sp.Matrix([1,i]).T)
    #Caso y=1
    pol2 = pol.subs(y,1)
    sol = sp.solve(sp.Eq(pol2,0), x)
    for i in sol:
        direcciones.append(sp.Matrix([i,1]).T)
    vectores_unicos = []
    for vector in direcciones:
        vector_repetido = False
        for vector_unico in vectores_unicos:
            if equalVectors(vector, vector_unico):
                vector_repetido = True
                break
        if not vector_repetido:
            vectores_unicos.append(vector)
    return vectores_unicos


from utils.calc_param import segundaFormaFundamental, segundaFormaFundamental_pt_uv
import sympy as sp

"""u, v = sp.symbols('u v', real=True)
parab_hiper = sp.Matrix([u, v, u**2-v**2]).T
res = { 'sup' : parab_hiper, 'u' : u, 'v' : v }
segundaFormaFundamental(res)
II = sp.Matrix([[res['e'],res['f']],[res['f'], res['g']]])
print(direcciones_asintoticas(II))"""

u, v = sp.symbols('u v', real=True)
parab_hiper = sp.Matrix([u, v, u**2-v**2]).T
res = { 'sup' : parab_hiper, 'u' : u, 'v' : v, 'u0' : 0, 'v0' : 0 }
segundaFormaFundamental_pt_uv(res)
II = sp.Matrix([[res['e_pt'],res['f_pt']],[res['f_pt'], res['g_pt']]])
dirs = direcciones_asintoticas(II)
print(dirs)

from utils.graph import sup_param, vector
fig = sup_param(res['sup'], res['u'], res['v'], sp.Interval(-2,2), sp.Interval(-2,2))
punto = res['sup'].subs({res['u']:res['u0'], res['v']:res['v0']})
colores = ['yellow', 'black', 'brown', 'purple']
for i, dir in enumerate(dirs):
    vect = res['sup'].subs({res['u']:dir[0], res['v']:dir[1]})
    vector(punto, vect, fig=fig, color=colores[i])
    vector(punto, -1*vect, fig=fig, color=colores[i])
fig.show() 
