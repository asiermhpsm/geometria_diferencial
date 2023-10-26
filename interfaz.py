import tkinter as tk
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import graf
import geoDiff


class Aplicacion():
    colores = ["blue", "green", "red", "cyan", "magenta", "yellow", "black",
        "dodgerblue", "darkorange", "limegreen", "purple", "gold", "pink"]
    cmap_options = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'jet', 'cool', 'hot', 
                    'spring', 'summer', 'autumn', 'winter', 'gray', 'bone', 'copper', 'YlGnBu', 
                    'YlOrRd', 'Blues', 'Greens', 'Oranges', 'Reds', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 
                    'PuBu', 'YlGn', 'YlOrBr', 'YlOrRd', 'OrRd']

    mapa_calor = False
    resolucion = 50
    abecedario = [chr(i) for i in range(97, 123)]

    widgets_si_sup_param = []
    widgets_si_sup_form = []

    #Habilita e inhabilita superficie parametrizada o por ecuacion
    def seleccionar_tipo_superficie(self):
        opcion = self.tipo_superficie.get()
        if opcion == 1:
            for elem in self.widgets_si_sup_param:
                elem.config(state=tk.NORMAL)

            for elem in self.widgets_si_sup_form:
                elem.config(state=tk.DISABLED)

        elif opcion == 2:
            for elem in self.widgets_si_sup_form:
                elem.config(state=tk.NORMAL)

            for elem in self.widgets_si_sup_param:
                elem.config(state=tk.DISABLED)

    #Constructor
    def __init__(self):
        self.root = tk.Tk()

        
        
        #Atributos de control
        self.tipo_superficie = tk.IntVar()     #1 indica superficie parametrizada, 2 ecuacion
        self.variable_u = tk.StringVar(value="u")
        self.variable_v = tk.StringVar(value="v")
        self.variable_x = tk.StringVar(value="x")
        self.variable_y = tk.StringVar(value="y")
        self.variable_z = tk.StringVar(value="z")
        self.color_superficie = tk.StringVar(value="Predeterminado")

        #Configuracion del root
        self.ancho = 1500
        self.alto = 850
        self.root.title("Calculadora de superficies")
        self.root.geometry(f"{self.ancho}x{self.alto}")  
        self.root.resizable(False, False) 

        self.init_marcos()

        self.root.mainloop()
    
    #Inicializa los marcos generales
    def init_marcos(self):
        #Marco para introducir funciones
        marco_funciones = tk.Frame(self.root,relief="sunken", borderwidth=4)
        marco_funciones.pack(fill="x")
        self.init_marco_funcion(marco_funciones)

        #Marco para resto app
        marco_principal = tk.Frame(self.root, relief="sunken", borderwidth=4)
        marco_principal.pack(fill="x")
        self.init_marco_principal(marco_principal)

    #Inicializa los marcos para introducir la superficie
    def init_marco_funcion(self, marco):
        #Marco para superficie parametrizada
        marco_superficie_parametrizada = tk.Frame(marco,relief="sunken", borderwidth=2)
        marco_superficie_parametrizada.pack(side="left", expand=True, fill="x")
        self.init_superficie_parametrizada(marco_superficie_parametrizada)


        #Marco para superficie mediante formula
        marco_superficie_formula = tk.Frame(marco,relief="sunken", borderwidth=2)
        marco_superficie_formula.pack(side="left", expand=True, fill="x")
        self.init_superficie_formula(marco_superficie_formula)

    #Inicializa el marco para introducir una superficie parametrizada
    def init_superficie_parametrizada(self, marco):
        #Boton para elegir tipo de superficie
        tk.Radiobutton(marco, text="Superficie parametrizada", variable=self.tipo_superficie, value=1, command=self.seleccionar_tipo_superficie).pack(side="top", pady=10)


        #Marco para introducir la descripcion de la superficie parametrizada
        marco_superficie_parametrizada_descripcion = tk.Frame(marco)
        marco_superficie_parametrizada_descripcion.pack(side="top", pady=5)
        self.init_superficie_parametrizada_descripcion(marco_superficie_parametrizada_descripcion)


        #Marco para introducir las variables de la superficie parametrizada
        marco_superficie_parametrizada_variables = tk.Frame(marco)
        marco_superficie_parametrizada_variables.pack(side="top", pady=5)
        self.init_superficie_parametrizada_variables(marco_superficie_parametrizada_variables)

    #Crea los widget para indroducir una superficie parametrizada
    def init_superficie_parametrizada_descripcion(self, marco):
        ttk.Label(marco, text="\u03C6(").pack(side="left")
        
        self.widgets_si_sup_param.append(AutocompleteCombobox(marco, textvariable=self.variable_u,  completevalues=self.abecedario,width=3, state=tk.DISABLED))
        self.widgets_si_sup_param[-1].pack(side="left")

        ttk.Label(marco, text=",").pack(side="left")

        self.widgets_si_sup_param.append(AutocompleteCombobox(marco, textvariable=self.variable_v, completevalues=self.abecedario, width=3, state=tk.DISABLED))
        self.widgets_si_sup_param[-1].pack(side="left")

        ttk.Label(marco, text=")=(").pack(side="left")

        self.widgets_si_sup_param.append(tk.Entry(marco, state=tk.DISABLED, width=15))
        self.widgets_si_sup_param[-1].pack(side="left")

        ttk.Label(marco, text=",").pack(side="left")

        self.widgets_si_sup_param.append(tk.Entry(marco, state=tk.DISABLED, width=15))
        self.widgets_si_sup_param[-1].pack(side="left")

        ttk.Label(marco, text=",").pack(side="left")

        self.widgets_si_sup_param.append(tk.Entry(marco, state=tk.DISABLED, width=15))
        self.widgets_si_sup_param[-1].pack(side="left")

        ttk.Label(marco, text=")").pack(side="left")

    #Crea los widget para describir las variables de una superficie parametrizada
    def init_superficie_parametrizada_variables(self, marco):
        self.widgets_si_sup_param.append(AutocompleteCombobox(marco, textvariable=self.variable_u,  completevalues=self.abecedario, width=3, state=tk.DISABLED))
        self.widgets_si_sup_param[-1].pack(side="left")

        ttk.Label(marco, text=r": [ ").pack(side="left")

        self.widgets_si_sup_param.append(tk.Entry(marco, state=tk.DISABLED, width=5))
        self.widgets_si_sup_param[-1].pack(side="left")

        ttk.Label(marco, text=",").pack(side="left")

        self.widgets_si_sup_param.append(tk.Entry(marco, state=tk.DISABLED, width=5))
        self.widgets_si_sup_param[-1].pack(side="left")

        ttk.Label(marco, text=r"]").pack(side="left")

        self.widgets_si_sup_param.append(AutocompleteCombobox(marco, textvariable=self.variable_v,  completevalues=self.abecedario, width=3, state=tk.DISABLED))
        self.widgets_si_sup_param[-1].pack(side="left")

        ttk.Label(marco, text=r": [ ").pack(side="left")

        self.widgets_si_sup_param.append(tk.Entry(marco, state=tk.DISABLED, width=5))
        self.widgets_si_sup_param[-1].pack(side="left")

        ttk.Label(marco, text=",").pack(side="left")

        self.widgets_si_sup_param.append(tk.Entry(marco, state=tk.DISABLED, width=5))
        self.widgets_si_sup_param[-1].pack(side="left")

        ttk.Label(marco, text=r"]").pack(side="left")

    #Inicializa el marco para introducir una superficie descrita mediante una formula
    def init_superficie_formula(self, marco):
        #Opcion superficie mediante formula
        tk.Radiobutton(marco, text="Superficie mediante formula", variable=self.tipo_superficie, value=2, command=self.seleccionar_tipo_superficie).pack(side="top", pady=10)

        #Marco para introducir la descripcion de la superficie descrita mediante una formula
        marco_superficie_formula_descripcion = tk.Frame(marco)
        marco_superficie_formula_descripcion.pack(side="top", pady=5)
        self.init_superficie_formula_descripcion(marco_superficie_formula_descripcion)

        #Marco para introducir las variables de la superficie descrita mediante una formula
        marco_superficie_formula_variables = tk.Frame(marco)
        marco_superficie_formula_variables.pack(side="top", pady=5)
        self.init_superficie_formula_variables(marco_superficie_formula_variables)

    #Crea los widget para indroducir una superficie descrita mediante una ecuacion
    def init_superficie_formula_descripcion(self, marco):
        ttk.Label(marco, text="\u03C6={").pack(side="left")

        self.widgets_si_sup_form.append(AutocompleteCombobox(marco, textvariable=self.variable_x,  completevalues=self.abecedario,width=3, state=tk.DISABLED))
        self.widgets_si_sup_form[-1].pack(side="left")

        ttk.Label(marco, text=",").pack(side="left")

        self.widgets_si_sup_form.append(AutocompleteCombobox(marco, textvariable=self.variable_y,  completevalues=self.abecedario,width=3, state=tk.DISABLED))
        self.widgets_si_sup_form[-1].pack(side="left")

        ttk.Label(marco, text=",").pack(side="left")

        self.widgets_si_sup_form.append(AutocompleteCombobox(marco, textvariable=self.variable_z,  completevalues=self.abecedario,width=3, state=tk.DISABLED))
        self.widgets_si_sup_form[-1].pack(side="left")

        ttk.Label(marco, text="):").pack(side="left")

        self.widgets_si_sup_form.append(tk.Entry(marco, state=tk.DISABLED, width=30))
        self.widgets_si_sup_form[-1].pack(side="left")

        ttk.Label(marco, text="=").pack(side="left")

        self.widgets_si_sup_form.append(tk.Entry(marco, state=tk.DISABLED, width=5))
        self.widgets_si_sup_form[-1].pack(side="left")

        ttk.Label(marco, text=")").pack(side="left")
        
    #Crea los widget para describir las variables de una superficie descrita 
    def init_superficie_formula_variables(self, marco):
        self.widgets_si_sup_form.append(AutocompleteCombobox(marco, textvariable=self.variable_x,  completevalues=self.abecedario, width=3, state=tk.DISABLED))
        self.widgets_si_sup_form[-1].pack(side="left")

        ttk.Label(marco, text=r": [ ").pack(side="left")

        self.widgets_si_sup_form.append(tk.Entry(marco, state=tk.DISABLED, width=5))
        self.widgets_si_sup_form[-1].pack(side="left")

        ttk.Label(marco, text=",").pack(side="left")

        self.widgets_si_sup_form.append(tk.Entry(marco, state=tk.DISABLED, width=5))
        self.widgets_si_sup_form[-1].pack(side="left")

        ttk.Label(marco, text=r"]").pack(side="left")

        ttk.Separator(marco, orient="vertical").pack(side="left")

        self.widgets_si_sup_form.append(AutocompleteCombobox(marco, textvariable=self.variable_y,  completevalues=self.abecedario, width=3, state=tk.DISABLED))
        self.widgets_si_sup_form[-1].pack(side="left")

        ttk.Label(marco, text=r": [ ").pack(side="left")

        self.widgets_si_sup_form.append(tk.Entry(marco, state=tk.DISABLED, width=5))
        self.widgets_si_sup_form[-1].pack(side="left")

        ttk.Label(marco, text=",").pack(side="left")

        self.widgets_si_sup_form.append(tk.Entry(marco, state=tk.DISABLED, width=5))
        self.widgets_si_sup_form[-1].pack(side="left")

        ttk.Label(marco, text=r"]").pack(side="left")
        
    #Inicializa el marco principal
    def init_marco_principal(self, marco):
        #Marco para graficar
        marco_graficar = tk.Frame(marco)
        marco_graficar.pack(side="left", expand=True, fill="x")
        self.init_marco_graficar(marco_graficar)


        #Marco para calculos
        marco_calculos = tk.Frame(marco)
        marco_calculos.pack(side="left", expand=True, fill="x")
        #self.init_marco_graficar(marco_calculos)

    def init_marco_graficar(self, marco):
        marco_graficar_usuario = tk.Frame(marco)
        marco_graficar_usuario.pack(side="top")
        #self.init_marco_graficar_usuario(marco_graficar_usuario)

        marco_graficar_imagen = tk.Frame(marco)
        marco_graficar_imagen.pack(side="top")
        self.init_marco_graficar_imagen(marco_graficar_imagen)


    
    def init_marco_graficar_imagen(self, marco):
        fig = plt.figure()
        fig.add_subplot(projection='3d')
        canvas = FigureCanvasTkAgg(fig, master=marco)
        canvas.get_tk_widget().pack()
        



    """   
    #Inicializa el marco con el boton para calcular
    def init_marco_calcular(self, marco):
        marco_opciones = tk.Frame(marco)
        marco_opciones.pack(side="left")

        #Color
        self.init_marco_color(marco_opciones)
        #Mapa calor
        ttk.Checkbutton(marco_opciones, text='Mapa de calor', variable=self.mapa_calor,  onvalue=True, offvalue=False).pack(side="top")
        #Resolucion
        self.init_marco_resolucion(marco_opciones)
        #Boton calcular
        tk.Button(marco, text="Calcular").pack(side="left")

    #Inicializa el marco con la opcion de elegir color de la superficie
    def init_marco_color(self, marco):
        marco_calc_marco_opciones_color = tk.Frame(marco)
        marco_calc_marco_opciones_color.pack(side="top")

        ttk.Label(marco_calc_marco_opciones_color, text="Color:").pack(side="left")
        AutocompleteCombobox(marco_calc_marco_opciones_color, textvariable=self.color_superficie, completevalues=self.colores, text='Mapa de calor').pack(side="left")
    
    #Inicializa el marco con la resolucion de la representacion de la superficie
    def init_marco_resolucion(self, marco):
        marco_calc_marco_opciones_resoluciones = tk.Frame(marco)
        marco_calc_marco_opciones_resoluciones.pack(side="top")

        ttk.Label(marco_calc_marco_opciones_resoluciones, text="Resolucion:").pack(side="left")
        ttk.Entry(marco_calc_marco_opciones_resoluciones, textvariable=self.resolucion).pack(side="left")
    """

def main():
    mi_app = Aplicacion()
    return 0


if __name__ == '__main__':
    main()