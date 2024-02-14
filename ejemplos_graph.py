from utils_graph_matplotlib import *
from utils_graph_mayavi import *
from utils_graph_plotly import *
import sympy as sp
from mayavi import mlab
import matplotlib.pyplot as plt
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


while True:
    print('\n\t1-superficie parametrizada'+
          '\n\t2-superficie mediante ecuacion'+
          '\n\t3-plano'+
          '\n\t4-salir')
    opcion = int(input('Seleccione opcion:'))
    if opcion == 1:
        superficie = int(input(f"Indique número del 0 al {len(superficies_parametrizadas)-1}:"))
        if superficie < 0 or superficie > len(superficies_parametrizadas)-1:
            continue
        sup, u_inf, u_sup, v_inf, v_sup = superficies_parametrizadas[superficie]
        print('\t1-mayavi'+
              '\n\t2-matplotlib'+
              '\n\t3-plotly'+
              '\n\t4-salir')
        motor = int(input('Seleccione biblioteca:'))
        if motor == 1:
            grafica_sup_param_mayavi(sup, u, v, u_inf, u_sup, v_inf, v_sup)
            mlab.orientation_axes()
            mlab.show()
        elif motor == 2:
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            grafica_sup_param_matplotlib(ax, sup, u, v, u_inf, u_sup, v_inf, v_sup)
            ax.set_aspect('equal')
            plt.show()
        elif motor == 3:
            fig = go.Figure()
            fig = grafica_sup_param_plotly(sup, u, v, u_inf, u_sup, v_inf, v_sup, fig)
            fig.update_layout(
                scene=dict(
                    aspectmode='data',
                    aspectratio=dict(x=1, y=1, z=1)
                )
            )
            fig.show()
        elif motor == 4:
            break
        else:
            continue    
    elif opcion == 2:
        print('\t0-esfera'+
              '\n\t1-elipsoide'+
              '\n\t2-hiperbolide de 1 hoja'+
              '\n\t3-hiperboloide de 2 hojas'+
              '\n\t4-cono'+
              '\n\t5-parabolide eliptico'+
              '\n\t6-parabolide hiperbolico'+
              '\n\t7-cilindro eliptico'+
              '\n\t8-cilindro hiperbolico'+
              '\n\t9-cilindro parabolico'+
              '\n\t10-plano'+
              '\n\t11-2 planos'+
              '\n\t12-planos cruzados')
        sup = int(input('Seleccione superficie:'))
        print('\t1-mayavi'+
              '\n\t2-plotly'+
              '\n\t3-salir')
        motor = int(input('Seleccione biblioteca:'))
        if motor == 1:
            grafica_sup_ec_mayavi(superficies_eq[sup], x, y, z)
            #mlab.plot3d([0, 2], [0, 0], [0, 0], color=(1, 0, 0), tube_radius=None)
            #mlab.plot3d([0, 0], [0, 2], [0, 0], color=(0, 1, 0), tube_radius=None)
            #mlab.plot3d([0, 0], [0, 0], [0, 2], color=(0, 0, 1), tube_radius=None)
            #mlab.axes()
            mlab.orientation_axes()
            mlab.show()
        elif motor == 2:
            fig = go.Figure()
            fig = grafica_sup_ec_plotly(superficies_eq[sup], x, y, z, fig=fig)
            fig.update_layout(
                scene=dict(
                    aspectmode='data',
                    aspectratio=dict(x=1, y=1, z=1)
                )
            )
            fig.show()
    elif opcion == 3:
        print('\ta*x+b*y+c*z+d=0')
        a = float(input('a:'))
        b = float(input('b:'))
        c = float(input('c:'))
        d = float(input('d:'))
        plano = a*x+b*y+c*z+d
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        grafica_sup_ec_matplotlib(ax, plano, x, y, z)
        ax.set_aspect('equal')
        plt.show()
    elif opcion == 4:
        break
    else:
        print('Opción invalida\n')