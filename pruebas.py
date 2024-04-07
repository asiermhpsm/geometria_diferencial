import tkinter as tk
from tkinter import ttk

def abrir_nueva_ventana():
    # Crear una nueva ventana
    nueva_ventana = tk.Toplevel(ventana_principal)
    nueva_ventana.title("Nueva Ventana")
    
    # Contenido de la nueva ventana
    etiqueta = ttk.Label(nueva_ventana, text="¡Esta es una nueva ventana!")
    etiqueta.pack()

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Ventana Principal")

# Crear un botón para abrir la nueva ventana
boton_abrir = ttk.Button(ventana_principal, text="Abrir Nueva Ventana", command=abrir_nueva_ventana)
boton_abrir.pack()

# Ejecutar el bucle principal de la interfaz gráfica
ventana_principal.mainloop()
