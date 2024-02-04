from utils_graph_plotly import *
import plotly.graph_objects as go

u, v = sp.symbols('u v')
s, t = sp.symbols('s t')
x, y, z = sp.symbols('x y z')

p=1
q=2
r=3

superficies_parametrizadas = []
superficies_parametrizadas.append( ((sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v) , sp.sin(u)), -sp.pi/2, sp.pi/2, 0, 2*sp.pi) )
superficies_parametrizadas.append( ((u, v, 0), -1, 1, -1, 1) )
superficies_parametrizadas.append( ((sp.cos(u + v), sp.sin(u - v), u - v), 0, 2*sp.pi, 0, 2*sp.pi) )
superficies_parametrizadas.append( ((sp.sin(u), sp.cos(u), v), 0, 2*sp.pi, 0, 2*sp.pi) )
superficies_parametrizadas.append( ((u*sp.cos(v),u*sp.sin(v), 0), 0, 2*sp.pi, 0, 2*sp.pi) )
superficies_parametrizadas.append( ((u+v, u*v, u-v), -1, 1, -1, 1) )
superficies_parametrizadas.append( ((u**2+v, u-v**2, u), -1, 1, -1, 1) )
superficies_parametrizadas.append( ((sp.sin(u), sp.cos(u), u), 0, sp.pi, 0, 2) ) #TODO-Revisar
superficies_parametrizadas.append( ((u, 0, v), -1, 1, -1, 1) )
superficies_parametrizadas.append( ((u, u**2, v), -1, 1, -1, 1) )
superficies_parametrizadas.append( ((sp.cos(u), sp.sin(u), v), 0, 2*sp.pi, 0, 2*sp.pi) )
superficies_parametrizadas.append( ( ((1 + 2*sp.cos(u))*sp.cos(v), (1 + 2*sp.cos(u))*sp.sin(v), 2*sp.sin(u)), 0, 2*sp.pi, 0, 2*sp.pi) )
superficies_parametrizadas.append( ((u, u**2 + v, v), -1, 1, -1, 1) )
superficies_parametrizadas.append( ((sp.cosh(u)*sp.cos(v), sp.cosh(u)*sp.sin(v), sp.sinh(u)), 0, 2*sp.pi, 0, 2*sp.pi) )
superficies_parametrizadas.append( ((u, v, u**2 + v**2), -1, 1, -1, 1) )
superficies_parametrizadas.append( ((u*sp.cos(v), u*sp.sin(v), u**2), 0, 2*sp.pi, 0, 2*sp.pi) )
superficies_parametrizadas.append( ((sp.cos(u)*sp.cos(v), -sp.cos(u)*sp.sin(v), 2*sp.sin(u)), 0, 2*sp.pi, 0, 2*sp.pi) )
superficies_parametrizadas.append( ((u*sp.cos(v), u*sp.sin(v), (u**2)/2), 0, 2*sp.pi, 0, 2*sp.pi) )
superficies_parametrizadas.append( ((sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v) , sp.sin(u)*sp.cos(v)), 0, 2*sp.pi, 0, 2*sp.pi) )
superficies_parametrizadas.append( ((u, v, u**2+v**2), -1, 1, -1, 1) )

esfera_eq = x**2 + y**2 + z**2 - 1
elipsoide_eq = (x/p)**2 + (y/q)**2 + (z/r)**2 - 1
hiperboloide1hoja_eq = (x/p)**2 + (y/q)**2 - (z/r)**2 - 1
hiperboloide2hojas_eq = (x/p)**2 - (y/q)**2 - (z/r)**2 - 1
cono_eq = (x/p)**2 + (y/q)**2 - (z/r)**2
paraboloideeliptico_eq = (x/p)**2 + (y/q)**2 - z
paraboloidehiperbolico_eq = (x/p)**2 - (y/q)**2 - z
cilindroeliptico_eq = (x/p)**2 + (y/q)**2 - 1
cilindrohiperbolico_eq = (x/p)**2 - (y/q)**2 - 1
cilindroparabolico_eq = (x/p)**2 - y
plano_eq_1 = x
plano_eq_2 = x**2 - p**2
plano_eq_3 = (x/p)**2 - (y/q)**2
superficies_eq = [esfera_eq, elipsoide_eq, hiperboloide1hoja_eq, hiperboloide2hojas_eq,
                  cono_eq, paraboloideeliptico_eq, paraboloidehiperbolico_eq,
                  cilindroeliptico_eq, cilindrohiperbolico_eq, cilindroparabolico_eq, 
                  plano_eq_1, plano_eq_2, plano_eq_3]



i=0
for sup, u_inf, u_sup, v_inf, v_sup in superficies_parametrizadas:
    i = i+1
    fig = go.Figure()
    fig = grafica_sup_param_plotly(sup, u, v, u_inf, u_sup, v_inf, v_sup, fig)
    fig.update_layout(
        scene=dict(
            aspectmode='data',
            aspectratio=dict(x=1, y=1, z=1)
        )
    )
    fig.show()
    if i%5 == 0:
        cont = input()

i=0
for sup in superficies_eq:
    i = i+1
    fig = go.Figure()
    fig = grafica_sup_ec_plotly(sup, x, y, z, fig=fig)
    fig.update_layout(
        scene=dict(
            aspectmode='data',
            aspectratio=dict(x=1, y=1, z=1)
        )
    )
    fig.show()
    if i%5 == 0:
        cont = input()
