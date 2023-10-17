import tkinter as tk
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import metodos

class Aplicacion():
    def seleccionar_representacion_superficie(self):
        opcion = self.representacion_superficie.get()
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

    #Constructor
    def __init__(self):
        self.root = tk.Tk()

        #Atributos para el calculo matemático
        self.colores = ["Predeterminado", "Rojo", "Amarillo", "Azul", "Negro"]
        self.mapa_calor = False
        self.resolucion = 50
        self.abecedario = [chr(i) for i in range(97, 123)]
        
        #Atributos de control
        self.representacion_superficie = tk.IntVar()     #1 indica superficie parametrizada, 2 ecuacion
        self.variable_u = tk.StringVar(value="u")
        self.variable_v = tk.StringVar(value="v")
        self.color_superficie = tk.StringVar(value="Predeterminado")

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
        self.marco_resultados = tk.Frame(self.root)
        self.marco_resultados.pack(side="left")

        self.marco_grafica = tk.Frame(self.marco_resultados, borderwidth=4, relief="groove")
        self.marco_grafica.pack(side="top")
        self.marco_salida = tk.Frame(self.marco_resultados, borderwidth=4, relief="groove")
        self.marco_salida.pack(side="top")

        #Marcos para el usuario
        self.marco_usuario = tk.Frame(self.root)
        self.marco_usuario.pack(side="left")

        self.marco_superficie = tk.Frame(self.marco_usuario, borderwidth=4, relief="groove")
        self.marco_superficie.pack(side="top")
        self.marco_op = tk.Frame(self.marco_usuario)
        self.marco_op.pack(side="top")
        self.marco_calc = tk.Frame(self.marco_usuario, borderwidth=4, relief="groove")
        self.marco_calc.pack(side="top")

        self.init_marco_superficies()
        #TODO- marco operaciones
        #TODO- marco grafica
        #TODO- marco salida
        self.init_marco_calcular()

    #Inicializa el marco para introducir la superficie
    def init_marco_superficies(self):
        self.ancho_entryes = int(self.root.winfo_width() * 0.05)    #Tamaño maximo de una Entry

        self.init_superficie_parametrizada()
        self.init_superficie_ecuaciones()

    #Inicializa el marco para introducir una superficie parametrizada
    def init_superficie_parametrizada(self):
        #Marco dentro de marco_superficie para superficies parametrizadas
        self.marco_superficie_parametrizada = tk.Frame(self.marco_superficie)
        self.marco_superficie_parametrizada.pack(side="top")
        #Marco dentro de marco_superficie para superficies representadas con una ecuacion
        self.marco_superficie_ecuacion = tk.Frame(self.marco_superficie)
        self.marco_superficie_ecuacion.pack(side="top")

        #Opcion superficie parametrizada
        self.opcion_superficie_parametrizada = tk.Radiobutton(self.marco_superficie_parametrizada, text="Superficie parametrizada", variable=self.representacion_superficie, value=1, command=self.seleccionar_representacion_superficie)
        self.opcion_superficie_parametrizada.pack(side="top")

        #Marco dentro de marco_superficie_parametrizada para describir la ecuacion
        self.marco_superficie_parametrizada_desc = tk.Frame(self.marco_superficie_parametrizada)
        self.marco_superficie_parametrizada_desc.pack(side="top")
        #Marco dentro de marco_superficie_parametrizada para describir las variables
        self.marco_superficie_parametrizada_variables = tk.Frame(self.marco_superficie_parametrizada)
        self.marco_superficie_parametrizada_variables.pack(side="top")

        self.init_ecuaciones_superficie_parametrizada()
        self.init_variables_superficie_parametrizada()

    #Inicializa el marco para describir una superficie parametrizada
    def init_ecuaciones_superficie_parametrizada(self):
        self.label_phi1 = ttk.Label(self.marco_superficie_parametrizada_desc, text="\u03C6(")
        self.label_phi1.pack(side="left")
        self.autocompletebox_u1 = AutocompleteCombobox(self.marco_superficie_parametrizada_desc, textvariable=self.variable_u,  completevalues=self.abecedario,width=4, state=tk.DISABLED)
        self.autocompletebox_u1.pack(side="left")
        self.coma1 = ttk.Label(self.marco_superficie_parametrizada_desc, text=",")
        self.coma1.pack(side="left")
        self.autocompletebox_v1 = AutocompleteCombobox(self.marco_superficie_parametrizada_desc, textvariable=self.variable_v, completevalues=self.abecedario, width=4, state=tk.DISABLED)
        self.autocompletebox_v1.pack(side="left")
        self.igual_parent = ttk.Label(self.marco_superficie_parametrizada_desc, text=")=(")
        self.igual_parent.pack(side="left")
        self.entrada1 = tk.Entry(self.marco_superficie_parametrizada_desc, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada1.pack(side="left")
        self.coma2 = ttk.Label(self.marco_superficie_parametrizada_desc, text=",")
        self.coma2.pack(side="left")
        self.entrada2 = tk.Entry(self.marco_superficie_parametrizada_desc, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada2.pack(side="left")
        self.coma3 = ttk.Label(self.marco_superficie_parametrizada_desc, text=",")
        self.coma3.pack(side="left")
        self.entrada3 = tk.Entry(self.marco_superficie_parametrizada_desc, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada3.pack(side="left")
        self.cerrar_parent1 = ttk.Label(self.marco_superficie_parametrizada_desc, text=")")
        self.cerrar_parent1.pack(side="left")

    #Inicializa el marco para describir la variables de una superficie parametrizada
    def init_variables_superficie_parametrizada(self):
        self.autocompletebox_u2 = AutocompleteCombobox(self.marco_superficie_parametrizada_variables, textvariable=self.variable_u,  completevalues=self.abecedario, width=4, state=tk.DISABLED)
        self.autocompletebox_u2.pack(side="left")
        self.abrir_corch1 = ttk.Label(self.marco_superficie_parametrizada_variables, text=r": [ ")
        self.abrir_corch1.pack(side="left")
        self.entrada4 = tk.Entry(self.marco_superficie_parametrizada_variables, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada4.pack(side="left")
        self.coma4 = ttk.Label(self.marco_superficie_parametrizada_variables, text=",")
        self.coma4.pack(side="left")
        self.entrada5 = tk.Entry(self.marco_superficie_parametrizada_variables, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada5.pack(side="left")
        self.cerrar_corch1 = ttk.Label(self.marco_superficie_parametrizada_variables, text=r"]")
        self.cerrar_corch1.pack(side="left")
        self.separador2 = ttk.Separator(self.marco_superficie_parametrizada_variables, orient="vertical")
        self.separador2.pack(side="left")
        self.autocompletebox_v2 = AutocompleteCombobox(self.marco_superficie_parametrizada_variables, textvariable=self.variable_v,  completevalues=self.abecedario, width=4, state=tk.DISABLED)
        self.autocompletebox_v2.pack(side="left")
        self.abrir_corch2 = ttk.Label(self.marco_superficie_parametrizada_variables, text=r": [ ")
        self.abrir_corch2.pack(side="left")
        self.entrada6 = tk.Entry(self.marco_superficie_parametrizada_variables, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada6.pack(side="left")
        self.coma5 = ttk.Label(self.marco_superficie_parametrizada_variables, text=",")
        self.coma5.pack(side="left")
        self.entrada7 = tk.Entry(self.marco_superficie_parametrizada_variables, state=tk.DISABLED, width=self.ancho_entryes)
        self.entrada7.pack(side="left")
        self.cerrar_corch2 = ttk.Label(self.marco_superficie_parametrizada_variables, text=r"]")
        self.cerrar_corch2.pack(side="left")

    #Inicializa el marco para introducir una superficie mediante una ecuacion
    def init_superficie_ecuaciones(self):
        #Marco dentro de marco_superficie_parametrizada para describir la ecuacion
        self.marco_superficie_ecuacion_ecuacion = tk.Frame(self.marco_superficie_parametrizada)
        self.marco_superficie_ecuacion_ecuacion.pack(side="top")
        #Marco dentro de marco_superficie_parametrizada para describir las ecuaciones
        self.marco_superficie_ecuacion_variables = tk.Frame(self.marco_superficie_parametrizada)
        self.marco_superficie_ecuacion_variables.pack(side="top")

        #Opcion superficie mediante ecuacion
        self.opcion_superficie_ecuacion = tk.Radiobutton(self.marco_superficie_ecuacion, text="Superficie mediante ecuacion", variable=self.representacion_superficie, value=2, command=self.seleccionar_representacion_superficie)
        self.opcion_superficie_ecuacion.pack(side="top")

        #TODO- self.init_ecuaciones_superficie_ecuaciones()
        #TODO- self.init_variables_superficie_ecuaciones()
        
    #Inicializa el marco con el boton para calcular
    def init_marco_calcular(self):
        self.marco_calc_marco_opciones = tk.Frame(self.marco_calc)
        self.marco_calc_marco_opciones.pack(side="left")

        #Color
        self.init_marco_color()
        #Mapa caloe
        self.checkbutton_mapa_calor= ttk.Checkbutton(self.marco_calc_marco_opciones, text='Mapa de calor', variable=self.mapa_calor,  onvalue=True, offvalue=False)
        self.checkbutton_mapa_calor.pack(side="top")
        #Resolucion
        self.init_marco_resolucion()
        #Boton calcular
        self.boton_calcular = tk.Button(self.marco_calc, text="Calcular")
        self.boton_calcular.pack(side="left")


        


    #Inicializa el marco con la opcion de elegir color de la superficie
    def init_marco_color(self):
        self.marco_calc_marco_opciones_color = tk.Frame(self.marco_calc_marco_opciones)
        self.marco_calc_marco_opciones_color.pack(side="top")

        self.texto_color_sup = ttk.Label(self.marco_calc_marco_opciones_color, text="Color:")
        self.texto_color_sup.pack(side="left")
        self.autocompletebox_color_superficie = AutocompleteCombobox(self.marco_calc_marco_opciones_color, textvariable=self.color_superficie, completevalues=self.colores, text='Mapa de calor')
        self.autocompletebox_color_superficie.pack(side="left")
    
    #Inicializa el marco con la resolucion de la representacion de la superficie
    def init_marco_resolucion(self):
        self.marco_calc_marco_opciones_resoluciones = tk.Frame(self.marco_calc_marco_opciones)
        self.marco_calc_marco_opciones_resoluciones.pack(side="top")

        self.texto_color_sup = ttk.Label(self.marco_calc_marco_opciones_resoluciones, text="Resolucion:")
        self.texto_color_sup.pack(side="left")
        self.entrada_resolucion= ttk.Entry(self.marco_calc_marco_opciones_resoluciones, textvariable=self.resolucion)
        self.entrada_resolucion.pack(side="left")


def main():
    mi_app = Aplicacion()
    return 0


if __name__ == '__main__':
    main()