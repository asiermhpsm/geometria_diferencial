import tkinter as tk
from tkinter import ttk
from app import app
import json
import tempfile
import webbrowser

"""
-------------------------------------------------------------------------------
API
-------------------------------------------------------------------------------
"""
server = app.test_client()
"""response = server.get('/param_surf/description?superficie=[u, v, 0]')
print(response.status_code)
data = json.loads(response.get_data())
for k, v in data.items():
    print(k, v)"""


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
VARIABLES CON LAS SELECCIONES
-------------------------------------------------------------------------------
"""
#VARIABLES DE SUPERFICIES PARAMETRIZADAS

#Primera variable de la superficie parametrizada
var1 = tk.StringVar()
#Segunda variable de la superficie parametrizada
var2 = tk.StringVar()
#Primera componente de la superficie parametrizada
comp1_sup_param = tk.StringVar()
#Segunda componente de la superficie parametrizada
comp2_sup_param = tk.StringVar()
#Tercera componente de la superficie parametrizada
comp3_sup_param = tk.StringVar()
#Tipo de dominio, 1 para intervalo de variables, 2 para dominio elíptico
tipo_dom_vars = tk.IntVar()
tipo_dom_vars.set(1)
#Dominio de la primera variable
dom_var1 = (tk.StringVar(), tk.StringVar())
#Dominio de la segunda variable
dom_var2 = (tk.StringVar(), tk.StringVar())
#Descrición de la primera variable
desc_var1 = {
    'positive': tk.BooleanVar(),
    'negative': tk.BooleanVar(),
    'integer': tk.BooleanVar(),
    'noninteger': tk.BooleanVar(),
    'even': tk.BooleanVar(),
    'odd': tk.BooleanVar()
}
for key in desc_var1:
    desc_var1[key].set(False)
#Descrición de la segunda variable
desc_var2 = {
    'positive': tk.BooleanVar(),
    'negative': tk.BooleanVar(),
    'integer': tk.BooleanVar(),
    'noninteger': tk.BooleanVar(),
    'even': tk.BooleanVar(),
    'odd': tk.BooleanVar()
}
for key in desc_var2:
    desc_var2[key].set(False)
#Lista con tuplas de nombre de constante + diccionario con la descripción de la constante
consts = []
#Lista con tuplas de nombre de funcion (y variables de dependencia) + diccionario con la descripción de la funcion
funcs = []
#valor a del dominio elíptico
a_dom_elip = tk.StringVar()
#valor b del dominio elíptico
b_dom_elip = tk.StringVar()
#valor r del dominio elíptico
r_dom_elip = tk.StringVar()
#Tipo de punto de superficie parametrica, 1 para punto genérico, 2 para punto de la forma phi(u,v), 3 para punto de la forma (x,y,z)
opc_punto_param = tk.IntVar()
opc_punto_param.set(1)
#Componente u del punto phi(u,v) de la superficie parametrica
comp1_pto_uv_param = tk.StringVar()
#Componente v del punto phi(u,v) de la superficie parametrica
comp2_pto_uv_param = tk.StringVar()
#Componente x del punto (x,y,z) de la superficie parametrica
comp1_pto_xyz_param = tk.StringVar()
#Componente y del punto (x,y,z) de la superficie parametrica
comp2_pto_xyz_param = tk.StringVar()
#Componente z del punto (x,y,z) de la superficie parametrica
comp3_pto_xyz_param = tk.StringVar()
#Diccionario con lo que se quiere calcular de la superficie parametrica
cal_param = {
    'vector_normal': tk.BooleanVar(),
    'plano_tangente': tk.BooleanVar(),
    'primera_forma_fundamental': tk.BooleanVar(),
    'segunda_forma_fundamental': tk.BooleanVar(),
    'curvatura_Gauss': tk.BooleanVar(),
    'curvatura_media': tk.BooleanVar(),
    'curvaturas_principales': tk.BooleanVar(),
    'direcciones_principales': tk.BooleanVar(),
    'weingarten': tk.BooleanVar(),
    'clasificacion_punto': tk.BooleanVar(),
    'punto_umbilico': tk.BooleanVar(),
    'description': tk.BooleanVar(),
}
for key in cal_param:
    cal_param[key].set(False)


#VARIBLES DE SUPERFICIES IMPLICITAS

#Parte izquierda de la ecuación de la superficie implicita
izq_sup_imp = tk.StringVar()
#Parte derecha de la ecuación de la superficie implicita
der_sup_imp = tk.StringVar()
#Tipo de punto de superficie implicita, 1 para punto genérico, 2 para punto de la forma (x,y,z)
opc_punto_imp = tk.IntVar()
opc_punto_imp.set(1)
#Componente x del punto (x,y,z) de la superficie implicita
comp1_pto_xyz_imp= tk.StringVar()
#Componente y del punto (x,y,z) de la superficie implicita
comp2_pto_xyz_imp = tk.StringVar()
#Componente z del punto (x,y,z) de la superficie implicita
comp3_pto_xyz_imp = tk.StringVar()
#Diccionario con lo que se quiere calcular de la superficie implicita
cal_imp = {
    'vector_normal': tk.BooleanVar(),
    'plano_tangente': tk.BooleanVar(),
}
for key in cal_imp:
    cal_imp[key].set(False)


"""
-------------------------------------------------------------------------------
FUNCIONES AUXILIARES
-------------------------------------------------------------------------------
"""
#AUXILIARES
def nueva_ventana(texto: str, titulo: str):
    nueva_ventana = tk.Toplevel(root)
    nueva_ventana.title(titulo)
    ttk.Label(nueva_ventana, text=texto).pack()

def prepara_var(nombre:str, opciones: dict):
    aux = ''
    for k, v in opciones.items():
        if v.get():
            aux = aux + f', {k}'
    return nombre if aux=='' else '['+nombre+aux+']'


#Funciones de configuración de la pantalla
def poner_texto_fondo(entrada, texto_fondo):
    def on_entry_click(event, entry, default_text):
        if entry.get() == default_text and not str(entry.cget("foreground"))=='black':
            entry.delete(0, tk.END)
            entry.config(foreground='black')

    def on_focus_out(event, entry, default_text):
        if not entry.get():
            entry.insert(0, default_text)
            entry.config(foreground='grey')

    entrada.insert(0, texto_fondo)
    entrada.configure(foreground='grey')
    entrada.bind("<FocusIn>", lambda event, entry=entrada: on_entry_click(event, entry, texto_fondo))
    entrada.bind("<FocusOut>", lambda event, entry=entrada: on_focus_out(event, entry, texto_fondo))


def on_configure(event):
    canva_dom_vars.configure(scrollregion=canva_dom_vars.bbox("all"))


def poner_resaltado_b_calc_param(event):
    b_calc_param.config(bg="#D4D4D4")
def quitar_resaltado_b_calc_param(event):
    b_calc_param.config(bg=root.cget("bg"))

def poner_resaltado_b_graf_param(event):
    b_graf_param.config(bg="#D4D4D4")
def quitar_resaltado_b_graf_param(event):
    b_graf_param.config(bg=root.cget("bg"))

def poner_resaltado_b_reset_param(event):
    b_reset_param.config(bg="#FF5555")
def quitar_resaltado_b_reset_param(event):
    b_reset_param.config(bg=root.cget("bg"))


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




#Funciones de acciones
def anadir_cte():
    nombre = tk.StringVar()
    desc_cte = {
        'positive': tk.BooleanVar(),
        'negative': tk.BooleanVar(),
        'integer': tk.BooleanVar(),
        'noninteger': tk.BooleanVar(),
        'even': tk.BooleanVar(),
        'odd': tk.BooleanVar()
    }
    for key in desc_cte:
        desc_cte[key].set(False)
    aux = ttk.Frame(frame_interior_canva)
    aux.pack(fill="x", pady=10)
    ttk.Label(aux, text="Constante: ").pack(side="left")
    aux2 = ttk.Entry(aux, width=10, justify="center", textvariable=nombre)
    poner_texto_fondo(aux2, 'r')
    aux2.pack(side="left")
    aux = ttk.Frame(frame_interior_canva)
    aux.pack(fill="x")
    ttk.Checkbutton(aux, text="Positiva", style="small.TCheckbutton", variable=desc_cte["positive"]).pack(side="left", padx=3)
    ttk.Checkbutton(aux, text="Negativa", style="small.TCheckbutton", variable=desc_cte["negative"]).pack(side="left", padx=3)
    ttk.Checkbutton(aux, text="Entera", style="small.TCheckbutton", variable=desc_cte["integer"]).pack(side="left", padx=3)
    ttk.Checkbutton(aux, text="No entera", style="small.TCheckbutton", variable=desc_cte["noninteger"]).pack(side="left", padx=3)
    ttk.Checkbutton(aux, text="Par", style="small.TCheckbutton", variable=desc_cte["even"]).pack(side="left", padx=3)
    ttk.Checkbutton(aux, text="Impar", style="small.TCheckbutton", variable=desc_cte["odd"]).pack(side="left", padx=3)
    consts.append((nombre, desc_cte))
    frame_interior_canva.update_idletasks()

def anadir_func():
    nombre = tk.StringVar()
    desc_func = {
        'positive': tk.BooleanVar(),
        'negative': tk.BooleanVar(),
        'integer': tk.BooleanVar(),
        'noninteger': tk.BooleanVar(),
        'even': tk.BooleanVar(),
        'odd': tk.BooleanVar()
    }
    for key in desc_func:
        desc_func[key].set(False)
    aux = ttk.Frame(frame_interior_canva)
    aux.pack(fill="x", pady=10)
    ttk.Label(aux, text="Funcion: ").pack(side="left")
    aux2 = ttk.Entry(aux, width=10, justify="center", textvariable=nombre)
    poner_texto_fondo(aux2, 'f(u,v)')
    aux2.pack(side="left")
    aux = ttk.Frame(frame_interior_canva)
    aux.pack(fill="x")
    ttk.Checkbutton(aux, text="Positiva", style="small.TCheckbutton", variable=desc_func["positive"]).pack(side="left", padx=3)
    ttk.Checkbutton(aux, text="Negativa", style="small.TCheckbutton", variable=desc_func["negative"]).pack(side="left", padx=3)
    ttk.Checkbutton(aux, text="Entera", style="small.TCheckbutton", variable=desc_func["integer"]).pack(side="left", padx=3)
    ttk.Checkbutton(aux, text="No entera", style="small.TCheckbutton", variable=desc_func["noninteger"]).pack(side="left", padx=3)
    ttk.Checkbutton(aux, text="Par", style="small.TCheckbutton", variable=desc_func["even"]).pack(side="left", padx=3)
    ttk.Checkbutton(aux, text="Impar", style="small.TCheckbutton", variable=desc_func["odd"]).pack(side="left", padx=3)
    funcs.append((nombre, desc_func))
    frame_interior_canva.update_idletasks()

def cerrar_ventana():
    root.destroy()

def calcular_sup_param():
    #Superficie y variables
    url_vals = f'superficie=[{comp1_sup_param.get()},{comp2_sup_param.get()},{comp3_sup_param.get()}]'
    if var1.get() != 'u':
        url_vals = url_vals + f'&var1={var1.get()}'
    if var2.get() != 'v':
        url_vals = url_vals + f'&var2={var2.get()}'

    #Dominio de tipo intervalo
    if tipo_dom_vars.get() == 1:
        if dom_var1[0].get() != '-\u221E' or dom_var1[1].get() != '\u221E':
            url_vals = url_vals + f'&dom_var1=({dom_var1[0].get()},{dom_var1[1].get()})'
        if dom_var2[0].get() != '-\u221E' or dom_var2[1].get() != '\u221E':
            url_vals = url_vals + f'&dom2_var=({dom_var2[0].get()},{dom_var2[1].get()})'
        ctes = ''
        for cte in consts:
            ctes = ctes + f'&const={prepara_var(cte[0].get(), cte[1])}'
        if ctes != '': 
            url_vals = url_vals + ctes
        funciones = ''
        for func in funcs:
            funciones = funciones + f'&func={prepara_var(func[0].get(), func[1])}'
        if funciones != '': 
            url_vals = url_vals + funciones
    #Dominio de tipo elíptico
    else:
        url_vals = url_vals + f'&cond={a_dom_elip.get()}*u^2 + {b_dom_elip.get()}*v^2 < {r_dom_elip.get()}'

    #Tipo de punto
    if opc_punto_param.get() == 2:
        url_vals = url_vals + f'&u0={comp1_pto_uv_param.get()}&v0={comp2_pto_uv_param.get()}'
    elif opc_punto_param.get() == 3:
        url_vals = url_vals + f'&x0={comp1_pto_xyz_param.get()}&y0={comp2_pto_xyz_param.get()}&z0={comp3_pto_xyz_param.get()}'

    url_vals = url_vals.replace('+', r'%2B')
    for v, k in cal_param.items():
        if k.get():
            response = server.get(f'/param_surf/{v}?{url_vals}')
            if response.status_code == 200:
                nueva_ventana(str(json.loads(response.get_data())), v)
                print(json.loads(response.get_data()))
            else:
                nueva_ventana(f"Error al calcular {v}", v)

def graficar_sup_param():
    #Superficie y variables
    url_vals = f'superficie=[{comp1_sup_param.get()},{comp2_sup_param.get()},{comp3_sup_param.get()}]'
    if var1.get() != 'u':
        url_vals = url_vals + f'&var1={var1.get()}'
    if var2.get() != 'v':
        url_vals = url_vals + f'&var2={var2.get()}'

    #Dominio de tipo intervalo
    if tipo_dom_vars.get() == 1:
        if dom_var1[0].get() != '-\u221E' and dom_var1[1].get() != '\u221E':
            url_vals = url_vals + f'&dom_var1=({dom_var1[0].get()},{dom_var1[1].get()})'
        if dom_var2[0].get() != '-\u221E' and dom_var2[1].get() != '\u221E':
            url_vals = url_vals + f'&dom_var2=({dom_var2[0].get()},{dom_var2[1].get()})'
        ctes = ''
        for cte in consts:
            ctes = ctes + f'&const={prepara_var(cte[0].get(), cte[1])}'
        if ctes != '': 
            url_vals = url_vals + ctes
        funciones = ''
        for func in funcs:
            funciones = funciones + f'&func={prepara_var(func[0].get(), func[1])}'
        if funciones != '': 
            url_vals = url_vals + funciones
    #Dominio de tipo elíptico
    else:
        url_vals = url_vals + f'&cond={a_dom_elip.get()}*u^2 + {b_dom_elip.get()}*v^2 < {r_dom_elip.get()}'

    #Tipo de punto
    if opc_punto_param.get() == 2:
        url_vals = url_vals + f'&u0={comp1_pto_uv_param.get()}&v0={comp2_pto_uv_param.get()}'
    elif opc_punto_param.get() == 3:
        url_vals = url_vals + f'&x0={comp1_pto_xyz_param.get()}&y0={comp2_pto_xyz_param.get()}&z0={comp3_pto_xyz_param.get()}'

    url_vals = url_vals.replace('+', r'%2B')
    response = server.get(f'/param_surf/grafica?{url_vals}')
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as temp_file:
            temp_file.write(response.data.decode('utf-8'))
            temp_file_path = temp_file.name
        webbrowser.open(temp_file_path)
        pass
    else:
        nueva_ventana(f"Error al graficar", "Gráfica")




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
aux2 = ttk.Entry(frame_sup_param, width=5, justify="center", textvariable=var1)
poner_texto_fondo(aux2, 'u')
aux2.place(x=26, y=cont_altura)
ttk.Label(frame_sup_param, text=",", font=(None, 12, "italic bold")).place(x=62, y=cont_altura)
aux2 = ttk.Entry(frame_sup_param, width=5, justify="center", textvariable=var2)
poner_texto_fondo(aux2, 'v')
aux2.place(x=70, y=cont_altura)
ttk.Label(frame_sup_param, text=") = (", font=(None, 12, "italic bold")).place(x=106, y=cont_altura)
aux2 = ttk.Entry(frame_sup_param, width=30, justify="center", textvariable=comp1_sup_param)
poner_texto_fondo(aux2, "cos(u)")
aux2.place(x=138, y=cont_altura)
ttk.Label(frame_sup_param, text=",", font=(None, 12, "italic bold")).place(x=324, y=cont_altura)
aux2 = ttk.Entry(frame_sup_param, width=30, justify="center", textvariable=comp2_sup_param)
poner_texto_fondo(aux2, "sin(u)")
aux2.place(x=332, y=cont_altura)
ttk.Label(frame_sup_param, text=",", font=(None, 12, "italic bold")).place(x=518, y=cont_altura)
aux2 = ttk.Entry(frame_sup_param, width=30, justify="center", textvariable=comp3_sup_param)
poner_texto_fondo(aux2, "v")
aux2.place(x=526, y=cont_altura)
ttk.Label(frame_sup_param, text=")", font=(None, 12, "italic bold")).place(x=712, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Radiobutton de dominio intervalo de variables
aux = ttk.Radiobutton(frame_sup_param, text="Dominio de variables en forma de intervalo", variable=tipo_dom_vars, value=1)
aux.place(x=5, y=cont_altura)

#Radiobutton de dominio eliptico
aux = ttk.Radiobutton(frame_sup_param, text="Dominio eliptico de variables", variable=tipo_dom_vars, value=2)
aux.place(x=425, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 10

#Canva de dominio de variables
canva_dom_vars = tk.Canvas(frame_sup_param, width=400, height=130)
canva_dom_vars.place(x=15, y=cont_altura)

frame_interior_canva = ttk.Frame(canva_dom_vars, width=325, height=200)
canva_dom_vars.create_window((0, 0), window=frame_interior_canva, anchor="nw")

scrollbar = ttk.Scrollbar(frame_interior_canva, orient=tk.VERTICAL, command=canva_dom_vars.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canva_dom_vars.configure(yscrollcommand=scrollbar.set)

s = ttk.Style()
s.configure("small.TCheckbutton", font=(None, 7))

#Definición de dominio de primera variable
aux = ttk.Frame(frame_interior_canva)
aux.pack(fill="x", pady=10)
ttk.Label(aux, text="Variable 1: ").pack(side="left")
ttk.Entry(aux, width=5, state="disabled", justify="center", textvariable=var1).pack(side="left")
ttk.Label(aux, text="\u03F5 (").pack(side="left")
aux2 = ttk.Entry(aux, width=10, justify="center", textvariable=dom_var1[0])
poner_texto_fondo(aux2, "0")
aux2.pack(side="left")
ttk.Label(aux, text=",").pack(side="left")
aux2 = ttk.Entry(aux, width=10, justify="center", textvariable=dom_var1[1])
poner_texto_fondo(aux2, "2*pi")
aux2.pack(side="left")
ttk.Label(aux, text=")").pack(side="left")
aux = ttk.Frame(frame_interior_canva)
aux.pack(fill="x")
ttk.Checkbutton(aux, text="Positivo", style="small.TCheckbutton", variable=desc_var1["positive"]).pack(side="left", padx=3)
ttk.Checkbutton(aux, text="Negativo", style="small.TCheckbutton", variable=desc_var1["negative"]).pack(side="left", padx=3)
ttk.Checkbutton(aux, text="Entero", style="small.TCheckbutton", variable=desc_var1["integer"]).pack(side="left", padx=3)
ttk.Checkbutton(aux, text="No entero", style="small.TCheckbutton", variable=desc_var1["noninteger"]).pack(side="left", padx=3)
ttk.Checkbutton(aux, text="Par", style="small.TCheckbutton", variable=desc_var1["even"]).pack(side="left", padx=3)
ttk.Checkbutton(aux, text="Impar", style="small.TCheckbutton", variable=desc_var1["odd"]).pack(side="left", padx=3)

#Definición de dominio de segunda variable
aux = ttk.Frame(frame_interior_canva)
aux.pack(fill="x", pady=10)
ttk.Label(aux, text="Variable 2: ").pack(side="left")
ttk.Entry(aux, width=5, state="disabled", justify="center", textvariable=var2).pack(side="left")
ttk.Label(aux, text="\u03F5 (").pack(side="left")
aux2 = ttk.Entry(aux, width=10, justify="center", textvariable=dom_var2[0])
poner_texto_fondo(aux2, "-\u221E")
aux2.pack(side="left")
ttk.Label(aux, text=",").pack(side="left")
aux2 = ttk.Entry(aux, width=10, justify="center", textvariable=dom_var2[1])
poner_texto_fondo(aux2, "\u221E")
aux2.pack(side="left")
ttk.Label(aux, text=")").pack(side="left")
aux = ttk.Frame(frame_interior_canva)
aux.pack(fill="x")
ttk.Checkbutton(aux, text="Positivo", style="small.TCheckbutton", variable=desc_var2["positive"]).pack(side="left", padx=3)
ttk.Checkbutton(aux, text="Negativo", style="small.TCheckbutton", variable=desc_var2["negative"]).pack(side="left", padx=3)
ttk.Checkbutton(aux, text="Entero", style="small.TCheckbutton", variable=desc_var2["integer"]).pack(side="left", padx=3)
ttk.Checkbutton(aux, text="No entero", style="small.TCheckbutton", variable=desc_var2["noninteger"]).pack(side="left", padx=3)
ttk.Checkbutton(aux, text="Par", style="small.TCheckbutton", variable=desc_var2["even"]).pack(side="left", padx=3)
ttk.Checkbutton(aux, text="Impar", style="small.TCheckbutton", variable=desc_var2["odd"]).pack(side="left", padx=3)

ttk.Button(frame_sup_param, text="Definir constante", command=anadir_cte).place(x=75, y=cont_altura + 135)
ttk.Button(frame_sup_param, text="Definir función", command=anadir_func).place(x=220, y=cont_altura + 135)

canva_dom_vars.configure(scrollregion=canva_dom_vars.bbox("all"))
frame_interior_canva.bind("<Configure>", on_configure)

#Definición de dominio eliptico
ttk.Label(frame_sup_param, text="{(").place(x=440, y=cont_altura + 10)
ttk.Entry(frame_sup_param, width=5, state="disabled", justify="center", textvariable=var1).place(x=453, y=cont_altura + 10)
ttk.Label(frame_sup_param, text=",").place(x=489, y=cont_altura + 10)
ttk.Entry(frame_sup_param, width=5, state="disabled", justify="center", textvariable=var2).place(x=496, y=cont_altura + 10)
ttk.Label(frame_sup_param, text="):").place(x=532, y=cont_altura + 10)
aux2 = ttk.Entry(frame_sup_param, width=5, justify="center", textvariable=a_dom_elip)
poner_texto_fondo(aux2, "1")
aux2.place(x=543, y=cont_altura + 10)
ttk.Entry(frame_sup_param, width=5, state="disabled", justify="center", textvariable=var1).place(x=576, y=cont_altura + 10)
ttk.Label(frame_sup_param, text="\u00B2 +").place(x=615, y=cont_altura + 10)
aux2 = ttk.Entry(frame_sup_param, width=5, justify="center", textvariable=b_dom_elip)
poner_texto_fondo(aux2, "1")
aux2.place(x=641, y=cont_altura + 10)
ttk.Entry(frame_sup_param, width=5, state="disabled", justify="center", textvariable=var2).place(x=674, y=cont_altura + 10)
ttk.Label(frame_sup_param, text="\u00B2 < ").place(x=713, y=cont_altura + 10)
aux2 = ttk.Entry(frame_sup_param, width=5, justify="center", textvariable=r_dom_elip)
poner_texto_fondo(aux2, "1")
aux2.place(x=746, y=cont_altura + 10)
ttk.Label(frame_sup_param, text="}").place(x=783, y=cont_altura + 10)

cont_altura = 375

#Separador horizontal
ttk.Separator(frame_sup_param, orient=tk.HORIZONTAL).place(x=25, y=350, width=750)

#Sección punto
aux = ttk.Label(frame_sup_param, text="Punto:", font=(None, 12, "bold"))
aux.place(x=5, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Radiobutton de punto genérico
aux = ttk.Radiobutton(frame_sup_param, text="Punto genérico", variable=opc_punto_param, value=1)
aux.place(x=5, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Radiobutton de punto uv
aux = ttk.Radiobutton(frame_sup_param, text="Punto \u03C6(", variable=opc_punto_param, value=2)
aux.place(x=5, y=cont_altura)
aux2 = ttk.Entry(frame_sup_param, width=10, justify="center", textvariable=comp1_pto_uv_param)
poner_texto_fondo(aux2, "pi/2")
aux2.place(x=77, y=cont_altura)
ttk.Label(frame_sup_param, text=",").place(x=143, y=cont_altura)
aux2 = ttk.Entry(frame_sup_param, width=10, justify="center", textvariable=comp2_pto_uv_param)
poner_texto_fondo(aux2, "0")
aux2.place(x=150, y=cont_altura)
ttk.Label(frame_sup_param, text=")").place(x=216, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Radiobutton de punto xyz
aux = ttk.Radiobutton(frame_sup_param, text="Punto ", variable=opc_punto_param, value=3)
aux.place(x=5, y=cont_altura)
ttk.Label(frame_sup_param, text="(").place(x=60, y=cont_altura)
aux2 = ttk.Entry(frame_sup_param, width=10, justify="center", textvariable=comp1_pto_xyz_param)
poner_texto_fondo(aux2, "1")
aux2.place(x=66, y=cont_altura)
ttk.Label(frame_sup_param, text=",").place(x=133, y=cont_altura)
aux2 = ttk.Entry(frame_sup_param, width=10, justify="center", textvariable=comp2_pto_xyz_param)
poner_texto_fondo(aux2, "0")
aux2.place(x=140, y=cont_altura)
ttk.Label(frame_sup_param, text=",").place(x=207, y=cont_altura)
aux2 = ttk.Entry(frame_sup_param, width=10, justify="center", textvariable=comp3_pto_xyz_param)
poner_texto_fondo(aux2, "0")
aux2.place(x=214, y=cont_altura)
ttk.Label(frame_sup_param, text=")").place(x=280, y=cont_altura)

#Separador vertical
ttk.Separator(frame_sup_param, orient=tk.VERTICAL).place(x=300, y=365, height=215)

cont_altura = 375

#Sección de botones de cálculo
frame_calc = ttk.Frame(frame_sup_param)
frame_calc.place(x=315, y=cont_altura)
ttk.Checkbutton(frame_calc, text="Vector normal", variable=cal_param["vector_normal"]).grid(row=0, column=0, padx=15, sticky="w")
ttk.Checkbutton(frame_calc, text="Plano tangente", variable=cal_param["plano_tangente"]).grid(row=0, column=1, padx=15, sticky="w")
ttk.Checkbutton(frame_calc, text="Primera Form. Fund", variable=cal_param["primera_forma_fundamental"]).grid(row=0, column=2, padx=15, sticky="w")
ttk.Checkbutton(frame_calc, text="SegundaForm. Fund.", variable=cal_param["segunda_forma_fundamental"]).grid(row=1, column=0, padx=15, sticky="w")
ttk.Checkbutton(frame_calc, text="Curv Gauss", variable=cal_param["curvatura_Gauss"]).grid(row=1, column=1, padx=15, sticky="w")
ttk.Checkbutton(frame_calc, text="Curv media", variable=cal_param["curvatura_media"]).grid(row=1, column=2, padx=15, sticky="w")
ttk.Checkbutton(frame_calc, text="Curvs principales", variable=cal_param["curvaturas_principales"]).grid(row=2, column=0, padx=15, sticky="w")
ttk.Checkbutton(frame_calc, text="Dirs principales", variable=cal_param["direcciones_principales"]).grid(row=2, column=1, padx=15, sticky="w")
ttk.Checkbutton(frame_calc, text="Matriz Weingarten", variable=cal_param["weingarten"]).grid(row=2, column=2, padx=15, sticky="w")
ttk.Checkbutton(frame_calc, text="Clasificación pto", variable=cal_param["clasificacion_punto"]).grid(row=3, column=0, padx=15, sticky="w")
ttk.Checkbutton(frame_calc, text="Punto umbílico", variable=cal_param["punto_umbilico"]).grid(row=3, column=1, padx=15, sticky="w")
ttk.Checkbutton(frame_calc, text="Análisis completo", variable=cal_param["description"]).grid(row=3, column=2, padx=15, sticky="w")

cont_altura = frame_sup_param.winfo_reqheight() - 100

#Botón de calcular
b_calc_param = tk.Button(frame_sup_param, text="Calcular", command=calcular_sup_param, width=10, height=2, font=(None, 12))
b_calc_param.place(x=375, y=cont_altura)
b_calc_param.bind("<Enter>", poner_resaltado_b_calc_param)
b_calc_param.bind("<Leave>", quitar_resaltado_b_calc_param)

#Botón de graficar
b_graf_param = tk.Button(frame_sup_param, text="Graficar", command=graficar_sup_param, width=10, height=2, font=(None, 12))
b_graf_param.place(x=498, y=cont_altura)
b_graf_param.bind("<Enter>", poner_resaltado_b_graf_param)
b_graf_param.bind("<Leave>", quitar_resaltado_b_graf_param)

#Botón de resetar
b_reset_param = tk.Button(frame_sup_param, text="Salir", command=cerrar_ventana, width=10, height=2, font=(None, 12))
b_reset_param.place(x=621, y=cont_altura)
b_reset_param.bind("<Enter>", poner_resaltado_b_reset_param)
b_reset_param.bind("<Leave>", quitar_resaltado_b_reset_param)



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
aux2 = ttk.Entry(frame_sup_imp, width=30, justify="center", textvariable=izq_sup_imp)
poner_texto_fondo(aux2, "x^2+y^2+z^2")
aux2.place(x=64, y=cont_altura)
ttk.Label(frame_sup_imp, text="=", font=(None, 12, "italic bold")).place(x=250, y=cont_altura)
aux2 = ttk.Entry(frame_sup_imp, width=10, justify="center", textvariable=der_sup_imp)
poner_texto_fondo(aux2, "1")
aux2.place(x=263, y=cont_altura)
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
aux2 = ttk.Entry(frame_sup_imp, width=10, justify="center", textvariable=comp1_pto_xyz_imp)
poner_texto_fondo(aux2, "1")
aux2.place(x=66, y=cont_altura)
ttk.Label(frame_sup_imp, text=",").place(x=133, y=cont_altura)
aux2 = ttk.Entry(frame_sup_imp, width=10, justify="center", textvariable=comp2_pto_xyz_imp)
poner_texto_fondo(aux2, "1")
aux2.place(x=140, y=cont_altura)
ttk.Label(frame_sup_imp, text=",").place(x=207, y=cont_altura)
aux2 = ttk.Entry(frame_sup_imp, width=10, justify="center", textvariable=comp3_pto_xyz_imp)
poner_texto_fondo(aux2, "1")
aux2.place(x=214, y=cont_altura)
ttk.Label(frame_sup_imp, text=")").place(x=280, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Sección de botones de cálculo
aux = ttk.Label(frame_sup_imp, text="Cálculo:", font=(None, 12, "bold"))
aux.place(x=5, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 20

#Checkbutton de vector normal
aux = ttk.Checkbutton(frame_sup_imp, text="Vector normal", variable=cal_imp["vector_normal"], command=None)
aux.place(x=5, y=cont_altura)

cont_altura = cont_altura + aux.winfo_reqheight() + 5

#Checkbutton de plano tangente
aux = ttk.Checkbutton(frame_sup_imp, text="Plano tangente", variable=cal_imp["plano_tangente"], command=None)
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
b_reset_imp = tk.Button(frame_sup_imp, text="Salir", command=cerrar_ventana, width=10, height=2, font=(None, 12))
b_reset_imp.place(x=cont_ancho, y=cont_altura)
b_reset_imp.bind("<Enter>", poner_resaltado_b_reset_imp)
b_reset_imp.bind("<Leave>", quitar_resaltado_b_reset_imp)



root.mainloop()



"""print(titulo_sup_imp.winfo_reqwidth())
print(titulo_sup_imp.winfo_reqheight())"""