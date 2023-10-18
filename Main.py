import tkinter as tk
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import metodos

class Aplicacion():
    #Atributos para el calculo matemático
    colores = ["blue", "green", "red", "cyan", "magenta", "yellow", "black",
        "dodgerblue", "darkorange", "limegreen", "purple", "gold", "pink"]
    mapa_calor = False
    resolucion = 50
    abecedario = [chr(i) for i in range(97, 123)]

    #Habilita e inhabilita superficie parametrizada o por ecuacion
    def seleccionar_tipo_superficie(self):
        opcion = self.tipo_superficie.get()
        if opcion == 1:
            self.autocompletebox_u1.config(state=tk.NORMAL)
            self.autocompletebox_v1.config(state=tk.NORMAL)
            self.entrada1.config(state=tk.NORMAL)
            self.entrada2.config(state=tk.NORMAL)
            self.entrada3.config(state=tk.NORMAL)
            self.autocompletebox_u2.config(state=tk.NORMAL)
            self.entrada4.config(state=tk.NORMAL)
            self.entrada5.config(state=tk.NORMAL)
            self.autocompletebox_v2.config(state=tk.NORMAL)
            self.entrada6.config(state=tk.NORMAL)
            self.entrada7.config(state=tk.NORMAL)
            #TODO- deshabilitar la superficie por ecuaciones
        else:
            self.autocompletebox_u1.config(state=tk.DISABLED)
            self.autocompletebox_v1.config(state=tk.DISABLED)
            self.entrada1.config(state=tk.DISABLED)
            self.entrada2.config(state=tk.DISABLED)
            self.entrada3.config(state=tk.DISABLED)
            self.autocompletebox_u2.config(state=tk.DISABLED)
            self.entrada4.config(state=tk.DISABLED)
            self.entrada5.config(state=tk.DISABLED)
            self.autocompletebox_v2.config(state=tk.DISABLED)
            self.entrada6.config(state=tk.DISABLED)
            self.entrada7.config(state=tk.DISABLED)
            #TODO- habilitar la superficie por ecuaciones

    #Constructor
    def __init__(self):
        self.root = tk.Tk()

        
        
        #Atributos de control
        self.tipo_superficie = tk.IntVar()     #1 indica superficie parametrizada, 2 ecuacion
        self.variable_u = tk.StringVar(value="u")
        self.variable_v = tk.StringVar(value="v")
        self.color_superficie = tk.StringVar(value="Predeterminado")

        self.ancho_entryes = int(self.root.winfo_width() * 0.05)    #Tamaño maximo de una Entry
        self.ancho_minimo = 1200
        self.alto_minimo = 700
        #ancho_minimo = int(root.winfo_screenwidth() * 0.85)
        #alto_minimo = int(root.winfo_screenheight() * 0.85)

        #Configuracion del root
        self.root.title("Calculadora de superficies")
        self.root.state('zoomed')
        self.root.wm_minsize(self.ancho_minimo, self.alto_minimo)

        self.init_marcos()

        self.root.mainloop()
    
    #Inicializa lo marcos principales
    def init_marcos(self):
        #Marcos de resultados
        marco_resultados = tk.Frame(self.root)
        marco_resultados.pack(side="left")

        marco_grafica = tk.Frame(marco_resultados, borderwidth=4, relief="groove")
        marco_grafica.pack(side="top")
        marco_salida = tk.Frame(marco_resultados, borderwidth=4, relief="groove")
        marco_salida.pack(side="top")

        #Marcos para el usuario
        marco_usuario = tk.Frame(self.root)
        marco_usuario.pack(side="left")

        marco_superficie = tk.Frame(marco_usuario, borderwidth=4, relief="groove")
        marco_superficie.pack(side="top")
        marco_op = tk.Frame(marco_usuario, borderwidth=4, relief="groove")
        marco_op.pack(side="top")
        marco_calc = tk.Frame(marco_usuario, borderwidth=4, relief="groove")
        marco_calc.pack(side="top")

        self.init_marco_superficies(marco_superficie)
        #TODO- marco operaciones
        #TODO- marco grafica
        #TODO- marco salida
        self.init_marco_calcular(marco_calc)

    #Inicializa el marco para introducir la superficie
    def init_marco_superficies(self, marco_superficie):

        self.init_superficie_parametrizada(marco_superficie)
        self.init_superficie_ecuaciones(marco_superficie)

    #Inicializa el marco para introducir una superficie parametrizada
    def init_superficie_parametrizada(self, marco):
        marco_superficie_parametrizada = tk.Frame(marco)
        marco_superficie_parametrizada.pack(side="top")

        opcion_superficie_parametrizada = tk.Radiobutton(marco_superficie_parametrizada, text="Superficie parametrizada", variable=self.tipo_superficie, value=1, command=self.seleccionar_tipo_superficie)
        opcion_superficie_parametrizada.pack(side="top")

        marco_superficie_parametrizada_ecuaciones = tk.Frame(marco_superficie_parametrizada)
        marco_superficie_parametrizada_ecuaciones.pack(side="top")

        marco_superficie_parametrizada_variables = tk.Frame(marco_superficie_parametrizada)
        marco_superficie_parametrizada_variables.pack(side="top")

        self.init_ecuaciones_superficie_parametrizada(marco_superficie_parametrizada_ecuaciones)
        self.init_variables_superficie_parametrizada(marco_superficie_parametrizada_variables)

    #Inicializa el marco para describir una superficie parametrizada
    def init_ecuaciones_superficie_parametrizada(self, marco):
        ttk.Label(marco, text="\u03C6(").pack(side="left")
        self.autocompletebox_u1 = AutocompleteCombobox(marco, textvariable=self.variable_u,  completevalues=self.abecedario,width=4, state=tk.DISABLED)
        self.autocompletebox_u1.pack(side="left")
        ttk.Label(marco, text=",").pack(side="left")
        self.autocompletebox_v1 = AutocompleteCombobox(marco, textvariable=self.variable_v, completevalues=self.abecedario, width=4, state=tk.DISABLED)
        self.autocompletebox_v1.pack(side="left")
        ttk.Label(marco, text=")=(").pack(side="left")
        self.entrada1 = tk.Entry(marco, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada1.pack(side="left")
        ttk.Label(marco, text=",").pack(side="left")
        self.entrada2 = tk.Entry(marco, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada2.pack(side="left")
        ttk.Label(marco, text=",").pack(side="left")
        self.entrada3 = tk.Entry(marco, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada3.pack(side="left")
        ttk.Label(marco, text=")").pack(side="left")

    #Inicializa el marco para describir la variables de una superficie parametrizada
    def init_variables_superficie_parametrizada(self, marco):
        self.autocompletebox_u2 = AutocompleteCombobox(marco, textvariable=self.variable_u,  completevalues=self.abecedario, width=4, state=tk.DISABLED)
        self.autocompletebox_u2.pack(side="left")
        ttk.Label(marco, text=r": [ ").pack(side="left")
        self.entrada4 = tk.Entry(marco, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada4.pack(side="left")
        ttk.Label(marco, text=",").pack(side="left")
        self.entrada5 = tk.Entry(marco, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada5.pack(side="left")
        ttk.Label(marco, text=r"]").pack(side="left")
        self.separador2 = ttk.Separator(marco, orient="vertical")
        self.separador2.pack(side="left")
        self.autocompletebox_v2 = AutocompleteCombobox(marco, textvariable=self.variable_v,  completevalues=self.abecedario, width=4, state=tk.DISABLED)
        self.autocompletebox_v2.pack(side="left")
        ttk.Label(marco, text=r": [ ").pack(side="left")
        self.entrada6 = tk.Entry(marco, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada6.pack(side="left")
        ttk.Label(marco, text=",").pack(side="left")
        self.entrada7 = tk.Entry(marco, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada7.pack(side="left")
        ttk.Label(marco, text=r"]").pack(side="left")

    #Inicializa el marco para introducir una superficie mediante una ecuacion
    def init_superficie_ecuaciones(self, marco):
        #Marco dentro de marco_superficie para superficies representadas con una ecuacion
        marco_superficie_ecuacion = tk.Frame(marco)
        marco_superficie_ecuacion.pack(side="top")

        #Opcion superficie mediante ecuacion
        tk.Radiobutton(marco, text="Superficie mediante ecuacion", variable=self.tipo_superficie, value=2, command=self.seleccionar_tipo_superficie).pack(side="top")

        #Marco dentro de marco_superficie_parametrizada para describir la ecuacion
        marco_superficie_ecuacion_ecuacion = tk.Frame(marco_superficie_ecuacion)
        marco_superficie_ecuacion_ecuacion.pack(side="top")
        #Marco dentro de marco_superficie_parametrizada para describir las ecuaciones
        marco_superficie_ecuacion_variables = tk.Frame(marco_superficie_ecuacion)
        marco_superficie_ecuacion_variables.pack(side="top")

        #TODO- self.init_ecuaciones_superficie_ecuaciones()
        #TODO- self.init_variables_superficie_ecuaciones()
        
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


def main():
    mi_app = Aplicacion()
    return 0


if __name__ == '__main__':
    main()