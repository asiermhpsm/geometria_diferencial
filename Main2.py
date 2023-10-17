import tkinter as tk
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import metodos

#Atributos para el calculo matemático
colores = ["Predeterminado", "Rojo", "Amarillo", "Azul", "Negro"]
mapa_calor = False
resolucion = 50
abecedario = [chr(i) for i in range(97, 123)]

def seleccionar_representacion_superficie():
    opcion = representacion_superficie.get()
    if opcion == 1:
        autocompletebox_u1.config(state=tk.NORMAL)
        autocompletebox_v1.config(state=tk.NORMAL)
        entrada1.config(state=tk.NORMAL)
        entrada2.config(state=tk.NORMAL)
        entrada3.config(state=tk.NORMAL)
        autocompletebox_u2.config(state=tk.NORMAL)
        entrada4.config(state=tk.NORMAL)
        entrada5.config(state=tk.NORMAL)
        autocompletebox_v2.config(state=tk.NORMAL)
        entrada6.config(state=tk.NORMAL)
        entrada7.config(state=tk.NORMAL)
    else:
        autocompletebox_u1.config(state=tk.DISABLED)
        autocompletebox_v1.config(state=tk.DISABLED)
        entrada1.config(state=tk.DISABLED)
        entrada2.config(state=tk.DISABLED)
        entrada3.config(state=tk.DISABLED)
        autocompletebox_u2.config(state=tk.DISABLED)
        entrada4.config(state=tk.DISABLED)
        entrada5.config(state=tk.DISABLED)
        autocompletebox_v2.config(state=tk.DISABLED)
        entrada6.config(state=tk.DISABLED)
        entrada7.config(state=tk.DISABLED)


root = tk.Tk()

#Atributos de control
representacion_superficie = tk.IntVar()     #1 indica superficie parametrizada, 2 ecuacion
variable_u = tk.StringVar(value="u")
variable_v = tk.StringVar(value="v")
color_superficie = tk.StringVar(value="Predeterminado")
 
ancho_minimo = 1200
alto_minimo = 700
#ancho_minimo = int(root.winfo_screenwidth() * 0.85)
#alto_minimo = int(root.winfo_screenheight() * 0.85)

root.title("Calculadora de superficies")
root.state('zoomed')
root.wm_minsize(ancho_minimo, alto_minimo)

#INICIALIZACION DE MARCOS PRINCIPALES
#Marcos de resultados
marco_resultados = tk.Frame(root)
marco_resultados.pack(side="left")

marco_grafica = tk.Frame(marco_resultados, borderwidth=4, relief="groove")
marco_grafica.pack(side="top")
marco_salida = tk.Frame(marco_resultados, borderwidth=4, relief="groove")
marco_salida.pack(side="top")

#Marcos para el usuario
marco_usuario = tk.Frame(root)
marco_usuario.pack(side="left")

marco_superficie = tk.Frame(marco_usuario, borderwidth=4, relief="groove")
marco_superficie.pack(side="top")
marco_op = tk.Frame(marco_usuario)
marco_op.pack(side="top")
marco_calc = tk.Frame(marco_usuario, borderwidth=4, relief="groove")
marco_calc.pack(side="top")

#---------------------------------------------------------------------------
#MARCO DE INTRODUCIR SUPERFICIE
#---------------------------------------------------------------------------

ancho_entryes = int(root.winfo_width() * 0.05)

#Marco dentro de marco_superficie para superficies parametrizadas
marco_superficie_parametrizada = tk.Frame(marco_superficie)
marco_superficie_parametrizada.pack(side="top")
#Marco dentro de marco_superficie para superficies representadas con una ecuacion
marco_superficie_ecuacion = tk.Frame(marco_superficie)
marco_superficie_ecuacion.pack(side="top")

#SUPERFICIE PARAMETRIZADA
#Opcion superficie parametrizada
opcion_superficie_parametrizada = tk.Radiobutton(marco_superficie_parametrizada, text="Superficie parametrizada", variable=representacion_superficie, value=1, command=seleccionar_representacion_superficie)
opcion_superficie_parametrizada.pack(side="top")

#Marco dentro de marco_superficie_parametrizada para describir la ecuacion
marco_superficie_parametrizada_desc = tk.Frame(marco_superficie_parametrizada)
marco_superficie_parametrizada_desc.pack(side="top")
#Marco dentro de marco_superficie_parametrizada para describir las variables
marco_superficie_parametrizada_variables = tk.Frame(marco_superficie_parametrizada)
marco_superficie_parametrizada_variables.pack(side="top")

#Descripcion de la superficie
label_phi1 = ttk.Label(marco_superficie_parametrizada_desc, text="\u03C6(")
label_phi1.pack(side="left")
autocompletebox_u1 = AutocompleteCombobox(marco_superficie_parametrizada_desc, textvariable=variable_u,  completevalues=abecedario,width=4, state=tk.DISABLED)
autocompletebox_u1.pack(side="left")
coma1 = ttk.Label(marco_superficie_parametrizada_desc, text=",")
coma1.pack(side="left")
autocompletebox_v1 = AutocompleteCombobox(marco_superficie_parametrizada_desc, textvariable=variable_v, completevalues=abecedario, width=4, state=tk.DISABLED)
autocompletebox_v1.pack(side="left")
igual_parent = ttk.Label(marco_superficie_parametrizada_desc, text=")=(")
igual_parent.pack(side="left")
entrada1 = tk.Entry(marco_superficie_parametrizada_desc, state=tk.DISABLED, width=ancho_entryes)
entrada1.pack(side="left")
coma2 = ttk.Label(marco_superficie_parametrizada_desc, text=",")
coma2.pack(side="left")
entrada2 = tk.Entry(marco_superficie_parametrizada_desc, state=tk.DISABLED, width=ancho_entryes)
entrada2.pack(side="left")
coma3 = ttk.Label(marco_superficie_parametrizada_desc, text=",")
coma3.pack(side="left")
entrada3 = tk.Entry(marco_superficie_parametrizada_desc, state=tk.DISABLED, width=ancho_entryes)
entrada3.pack(side="left")
cerrar_parent1 = ttk.Label(marco_superficie_parametrizada_desc, text=")")
cerrar_parent1.pack(side="left")

#Descripcion de las variables
autocompletebox_u2 = AutocompleteCombobox(marco_superficie_parametrizada_variables, textvariable=variable_u,  completevalues=abecedario, width=4, state=tk.DISABLED)
autocompletebox_u2.pack(side="left")
abrir_corch1 = ttk.Label(marco_superficie_parametrizada_variables, text=r": [ ")
abrir_corch1.pack(side="left")
entrada4 = tk.Entry(marco_superficie_parametrizada_variables, state=tk.DISABLED, width=ancho_entryes)
entrada4.pack(side="left")
coma4 = ttk.Label(marco_superficie_parametrizada_variables, text=",")
coma4.pack(side="left")
entrada5 = tk.Entry(marco_superficie_parametrizada_variables, state=tk.DISABLED, width=ancho_entryes)
entrada5.pack(side="left")
cerrar_corch1 = ttk.Label(marco_superficie_parametrizada_variables, text=r"]")
cerrar_corch1.pack(side="left")
separador2 = ttk.Separator(marco_superficie_parametrizada_variables, orient="vertical")
separador2.pack(side="left")
autocompletebox_v2 = AutocompleteCombobox(marco_superficie_parametrizada_variables, textvariable=variable_v,  completevalues=abecedario, width=4, state=tk.DISABLED)
autocompletebox_v2.pack(side="left")
abrir_corch2 = ttk.Label(marco_superficie_parametrizada_variables, text=r": [ ")
abrir_corch2.pack(side="left")
entrada6 = tk.Entry(marco_superficie_parametrizada_variables, state=tk.DISABLED, width=ancho_entryes)
entrada6.pack(side="left")
coma5 = ttk.Label(marco_superficie_parametrizada_variables, text=",")
coma5.pack(side="left")
entrada7 = tk.Entry(marco_superficie_parametrizada_variables, state=tk.DISABLED, width=ancho_entryes)
entrada7.pack(side="left")
cerrar_corch2 = ttk.Label(marco_superficie_parametrizada_variables, text=r"]")
cerrar_corch2.pack(side="left")



#SUPERFICIE MEDIANTE ECUACION
#Marco dentro de marco_superficie_parametrizada para describir la ecuacion
marco_superficie_ecuacion_ecuacion = tk.Frame(marco_superficie_parametrizada)
marco_superficie_ecuacion_ecuacion.pack(side="top")
#Marco dentro de marco_superficie_parametrizada para describir las ecuaciones
marco_superficie_ecuacion_variables = tk.Frame(marco_superficie_parametrizada)
marco_superficie_ecuacion_variables.pack(side="top")

#Opcion superficie mediante ecuacion
opcion_superficie_ecuacion = tk.Radiobutton(marco_superficie_ecuacion, text="Superficie mediante ecuacion", variable=representacion_superficie, value=2, command=seleccionar_representacion_superficie)
opcion_superficie_ecuacion.pack(side="top")


#---------------------------------------------------------------------------
#MARCO DE BOTON CALCULAR
#---------------------------------------------------------------------------

#Marco dentro de marco_calc a la izquierda para color, mapa calor y resolucion
marco_calc_marco_opciones = tk.Frame(marco_calc)
marco_calc_marco_opciones.pack(side="left")
#Marco dentro de marco_calc_marco_opciones para color de superficie
marco_calc_marco_opciones_color = tk.Frame(marco_calc_marco_opciones)
marco_calc_marco_opciones_color.pack(side="top")
#Marco dentro de marco_calc_marco_opciones para resolucion de superficie
marco_calc_marco_opciones_resoluciones = tk.Frame(marco_calc_marco_opciones)
marco_calc_marco_opciones_resoluciones.pack(side="top")


#Color de superficie
texto_color_sup = ttk.Label(marco_calc_marco_opciones_color, text="Color:")
texto_color_sup.pack(side="left")
autocompletebox_color_superficie = AutocompleteCombobox(marco_calc_marco_opciones_color, textvariable=color_superficie, completevalues=colores, text='Mapa de calor')
autocompletebox_color_superficie.pack(side="left")

#Mapa de calor
checkbutton_mapa_calor= ttk.Checkbutton(marco_calc_marco_opciones, text='Mapa de calor', variable=mapa_calor,  onvalue=True, offvalue=False)
checkbutton_mapa_calor.pack(side="top")

#Resolucion
texto_color_sup = ttk.Label(marco_calc_marco_opciones_resoluciones, text="Resolucion:")
texto_color_sup.pack(side="left")
entrada_resolucion= ttk.Entry(marco_calc_marco_opciones_resoluciones, textvariable=resolucion)
entrada_resolucion.pack(side="left")

#Boton calcular
boton_calcular = tk.Button(marco_calc, text="Calcular")
boton_calcular.pack(side="left")

 

root.mainloop()

