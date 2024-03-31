import tkinter as tk
from tkinter import ttk

"""
-------------------------------------------------------------------------------
RAÍZ
-------------------------------------------------------------------------------
"""
root = tk.Tk()
root.title("Calculadora de superficies")
root.geometry("1200x600")  
root.resizable(False, False)

"""
-------------------------------------------------------------------------------
VARIABLES CON LA OPCIONES
-------------------------------------------------------------------------------
"""
#VARIABLES DE SUPERFICIES PARAMETRIZADAS
dom_vars_interv = tk.IntVar()
dom_vars_interv.set(1)

#VARIBLES DE SUPERFICIES IMPLICITAS

#Tipo de punto, 1 para punto genérico, 2 para punto de la forma (x,y,z)
opc_punto_imp = tk.IntVar()
opc_punto_imp.set(1)

#Diccionario con lo que se quiere calcular
cal_imp = {
    'normal': tk.BooleanVar(),
    'tangente': tk.BooleanVar(),
}
cal_imp["normal"].set(False)
cal_imp["tangente"].set(False)

"""
-------------------------------------------------------------------------------
FUNCIONES AUXILIARES
-------------------------------------------------------------------------------
"""
def poner_resaltado_b_calc_imp(event):
    b_calc_imp.config(bg="#D4D4D4")
def quitar_resaltado_b_calc_imp(event):
    b_calc_imp.config(bg=root.cget("bg"))

def poner_resaltado_b_graf_imp(event):
    b_graf_imp.config(bg="#D4D4D4")
def quitar_resaltado_b_graf_imp(event):
    b_graf_imp.config(bg=root.cget("bg"))

def poner_resaltado_b_reset_imp(event):
    b_reset_imp.config(bg="#FF5555")
def quitar_resaltado_b_reset_imp(event):
    b_reset_imp.config(bg=root.cget("bg"))


"""
-------------------------------------------------------------------------------
SUPERFICIES PARAMETRIZADAS
-------------------------------------------------------------------------------
"""
#Marco general
frame_sup_param = tk.Frame(root, width=800, height=600, relief="solid", borderwidth=1)
frame_sup_param.place(x=0, y=0)

#Título
frame_titulo_sup_param = tk.Frame(frame_sup_param, width=800, height=40, relief="ridge", borderwidth=2)
frame_titulo_sup_param.place(x=0, y=0)
ttk.Label(frame_titulo_sup_param, text="SUPERFICIE PARAMETRIZADA", font=("Arial Black", 12)).place(x=265, y=5)

cont_altura = 60

#Sección de la ecuación
aux = ttk.Label(frame_sup_param, text="Superficie:", font=(None, 12, "bold"))
aux.place(x=5, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Superficie
aux = ttk.Label(frame_sup_param, text="\u03C6(", font=(None, 12, "italic bold"))
aux.place(x=5, y=cont_altura)
ttk.Entry(frame_sup_param, width=5).place(x=26, y=cont_altura)
ttk.Label(frame_sup_param, text=",", font=(None, 12, "italic bold")).place(x=62, y=cont_altura)
ttk.Entry(frame_sup_param, width=5).place(x=70, y=cont_altura)
ttk.Label(frame_sup_param, text=") = (", font=(None, 12, "italic bold")).place(x=106, y=cont_altura)
ttk.Entry(frame_sup_param, width=30).place(x=138, y=cont_altura)
ttk.Label(frame_sup_param, text=",", font=(None, 12, "italic bold")).place(x=324, y=cont_altura)
ttk.Entry(frame_sup_param, width=30).place(x=332, y=cont_altura)
ttk.Label(frame_sup_param, text=",", font=(None, 12, "italic bold")).place(x=518, y=cont_altura)
ttk.Entry(frame_sup_param, width=30).place(x=526, y=cont_altura)
ttk.Label(frame_sup_param, text=")", font=(None, 12, "italic bold")).place(x=712, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Radiobutton de dominio intervalo de variables
aux = ttk.Radiobutton(frame_sup_param, text="Dominio de variables en forma de intervalo", variable=dom_vars_interv, value=1)
aux.place(x=5, y=cont_altura)

#Radiobutton de dominio eliptico
aux = ttk.Radiobutton(frame_sup_param, text="Dominio eliptico de variables", variable=dom_vars_interv, value=2)
aux.place(x=405, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 10



#Definición de dominio eliptico
ttk.Label(frame_sup_param, text="{(").place(x=420, y=cont_altura)
ttk.Entry(frame_sup_param, width=5, state="disabled").place(x=433, y=cont_altura)
ttk.Label(frame_sup_param, text=",").place(x=469, y=cont_altura)
ttk.Entry(frame_sup_param, width=5, state="disabled").place(x=476, y=cont_altura)
ttk.Label(frame_sup_param, text="):").place(x=512, y=cont_altura)
ttk.Entry(frame_sup_param, width=5).place(x=523, y=cont_altura)
ttk.Entry(frame_sup_param, width=5, state="disabled").place(x=556, y=cont_altura)
ttk.Label(frame_sup_param, text="^2+").place(x=595, y=cont_altura)
ttk.Entry(frame_sup_param, width=5).place(x=621, y=cont_altura)
ttk.Entry(frame_sup_param, width=5, state="disabled").place(x=654, y=cont_altura)
ttk.Label(frame_sup_param, text="^2 < ").place(x=693, y=cont_altura)
ttk.Entry(frame_sup_param, width=5).place(x=726, y=cont_altura)
ttk.Label(frame_sup_param, text="}").place(x=763, y=cont_altura)


"""
-------------------------------------------------------------------------------
SUPERFICIES IMPLICITAS
-------------------------------------------------------------------------------
"""
#Marco general
frame_sup_imp = tk.Frame(root, width=400, height=600, relief="solid", borderwidth=1)
frame_sup_imp.place(x=800, y=0)

#Título
frame_titulo_sup_imp = tk.Frame(frame_sup_imp, width=400, height=40, relief="ridge", borderwidth=2)
frame_titulo_sup_imp.place(x=0, y=0)
ttk.Label(frame_titulo_sup_imp, text="SUPERFICIE IMPLICITA", font=("Arial Black", 12)).place(x=95, y=5)

cont_altura = 60

#Sección de la ecuación
aux = ttk.Label(frame_sup_imp, text="Superficie:", font=(None, 12, "bold"))
aux.place(x=5, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Superficie
aux = ttk.Label(frame_sup_imp, text="{(x,y,z): ", font=(None, 12, "italic bold"))
aux.place(x=5, y=cont_altura)
ttk.Entry(frame_sup_imp, width=30).place(x=64, y=cont_altura)
ttk.Label(frame_sup_imp, text="=", font=(None, 12, "italic bold")).place(x=250, y=cont_altura)
ttk.Entry(frame_sup_imp, width=10).place(x=263, y=cont_altura)
ttk.Label(frame_sup_imp, text="}", font=(None, 12, "italic bold")).place(x=329, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Sección del punto
aux = ttk.Label(frame_sup_imp, text="Punto:", font=(None, 12, "bold"))
aux.place(x=5, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Radiobutton de punto general
aux = ttk.Radiobutton(frame_sup_imp, text="Punto genérico", variable=opc_punto_imp, value=1)
aux.place(x=5, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 10

#Radiobutton de punto especifico
aux = ttk.Radiobutton(frame_sup_imp, text="Punto ", variable=opc_punto_imp, value=2)
aux.place(x=5, y=cont_altura)
ttk.Label(frame_sup_imp, text="(").place(x=60, y=cont_altura)
ttk.Entry(frame_sup_imp, width=10).place(x=66, y=cont_altura)
ttk.Label(frame_sup_imp, text=",").place(x=133, y=cont_altura)
ttk.Entry(frame_sup_imp, width=10).place(x=140, y=cont_altura)
ttk.Label(frame_sup_imp, text=",").place(x=207, y=cont_altura)
ttk.Entry(frame_sup_imp, width=10).place(x=214, y=cont_altura)
ttk.Label(frame_sup_imp, text=")").place(x=280, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Sección de botones de cálculo
aux = ttk.Label(frame_sup_imp, text="Cálculo:", font=(None, 12, "bold"))
aux.place(x=5, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Checkbutton de vector normal
aux = ttk.Checkbutton(frame_sup_imp, text="Vector normal", variable=cal_imp["normal"], command=None)
aux.place(x=5, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 5

#Checkbutton de plano tangente
aux = ttk.Checkbutton(frame_sup_imp, text="Plano tangente", variable=cal_imp["tangente"], command=None)
aux.place(x=5, y=cont_altura)

cont_altura = frame_sup_imp.winfo_reqheight() - 100

#Botón de calcular
b_calc_imp = tk.Button(frame_sup_imp, text="Calcular", command=None, width=10, height=2, font=(None, 12))
b_calc_imp.place(x=30, y=cont_altura)
b_calc_imp.bind("<Enter>", poner_resaltado_b_calc_imp)
b_calc_imp.bind("<Leave>", quitar_resaltado_b_calc_imp)

cont_ancho = 30 + aux.winfo_reqwidth() + 20

#Botón de graficar
b_graf_imp = tk.Button(frame_sup_imp, text="Graficar", command=None, width=10, height=2, font=(None, 12))
b_graf_imp.place(x=cont_ancho, y=cont_altura)
b_graf_imp.bind("<Enter>", poner_resaltado_b_graf_imp)
b_graf_imp.bind("<Leave>", quitar_resaltado_b_graf_imp)

cont_ancho = cont_ancho + aux.winfo_reqwidth() + 20

#Botón de resetar
b_reset_imp = tk.Button(frame_sup_imp, text="Reset", command=None, width=10, height=2, font=(None, 12))
b_reset_imp.place(x=cont_ancho, y=cont_altura)
b_reset_imp.bind("<Enter>", poner_resaltado_b_reset_imp)
b_reset_imp.bind("<Leave>", quitar_resaltado_b_reset_imp)



root.mainloop()



"""print(titulo_sup_imp.winfo_reqwidth())
print(titulo_sup_imp.winfo_reqheight())"""