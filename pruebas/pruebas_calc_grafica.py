import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import cm
import sympy as sp
import numpy as np
from metodos import procesa_sup_uv

u, v = sp.symbols('u, v', real = True)

def mostrar_cono():
    ecuaciones1 = [u*sp.cos(v), u*sp.sin(v), 2*u]
    tipo, X, Y, Z, color_map, color = procesa_sup_uv(ecuaciones1, u, v, 0, 5, 0, 2*np.pi, color_map=True)
    mostrar_grafico(X, Y, Z)

def mostrar_sup():
    ecuaciones2 = [u+v, u-v, u*v]
    tipo, X, Y, Z, color_map, color = procesa_sup_uv(ecuaciones2, u, v, 0, 5, 0, 5, color_map=True)
    mostrar_grafico(X, Y, Z)

def mostrar_embudo():
    ecuaciones3 = [sp.sech(u)*sp.cos(v), sp.sech(u)*sp.sin(v), u-sp.tanh(u)]
    tipo, X, Y, Z, color_map, color = procesa_sup_uv(ecuaciones3, u, v, 0, 5, 0, 2*np.pi, color_map=True)
    mostrar_grafico(X, Y, Z)

def mostrar_toro():
    R = 10
    r = 5
    ecuaciones4 = [(R+r*sp.cos(v))*sp.cos(u), (R +r*sp.cos(v))*sp.sin(u), r*sp.sin(v)]
    tipo, X, Y, Z, color_map, color = procesa_sup_uv(ecuaciones4, u, v, 0, 2*np.pi, 0, 2*np.pi)
    mostrar_grafico(X, Y, Z)

def mostrar_esfera():
    ecuaciones5 = [sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v), sp.sin(u)]
    tipo, X, Y, Z, color_map, color = procesa_sup_uv(ecuaciones5, u, v, 0, 2*np.pi, 0, 2*np.pi)
    mostrar_grafico(X, Y, Z)
    

def mostrar_grafico(X, Y, Z):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    surf = ax.plot_surface(X, Y, Z)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_aspect('equal')
    
    canvas = FigureCanvasTkAgg(fig, master=marco_grafico)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0)

root = tk.Tk()
root.title("Interfaz Gráfica con Gráfico de Matplotlib")

marco_grafico = ttk.Frame(root)
marco_grafico.grid(row=0, column=0)

boton_mostrar_grafico = tk.Button(root, text="Mostrar Cono", command=mostrar_cono)
boton_mostrar_grafico.grid(row=0, column=1)
boton_mostrar_grafico = tk.Button(root, text="Mostrar Superficie", command=mostrar_sup)
boton_mostrar_grafico.grid(row=1, column=1)
boton_mostrar_grafico = tk.Button(root, text="Mostrar Embudo", command=mostrar_embudo)
boton_mostrar_grafico.grid(row=2, column=1)
boton_mostrar_grafico = tk.Button(root, text="Mostrar Toro", command=mostrar_toro)
boton_mostrar_grafico.grid(row=3, column=1)
boton_mostrar_grafico = tk.Button(root, text="Mostrar Esfera", command=mostrar_esfera)
boton_mostrar_grafico.grid(row=4, column=1)

root.mainloop()
