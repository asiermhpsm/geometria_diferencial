import tkinter as tk

def actualizar_entrada():
    opcion = var.get()
    if opcion == 1:
        entrada.config(state=tk.NORMAL)
    else:
        entrada.config(state=tk.DISABLED)

ventana = tk.Tk()
ventana.title("Radiobutton con Label y Entry")

var = tk.IntVar()  # Variable de control para Radiobutton

radio1 = tk.Radiobutton(ventana, text="Habilitar Entrada", variable=var, value=1, command=actualizar_entrada)
radio2 = tk.Radiobutton(ventana, text="Deshabilitar Entrada", variable=var, value=2, command=actualizar_entrada)

entrada_label = tk.Label(ventana, text="Entrada:")
entrada = tk.Entry(ventana, state=tk.DISABLED)  # Inicialmente deshabilitado

radio1.pack()
radio2.pack()

entrada_label.pack()
entrada.pack()

ventana.mainloop()
