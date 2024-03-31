import tkinter as tk

# Crear ventana
ventana = tk.Tk()
ventana.title("Entry Bloqueada")

# Crear Entry bloqueada
entry_bloqueada = tk.Entry(ventana, state="readonly")
entry_bloqueada.pack()

# Configurar el texto de la Entry
entry_bloqueada.insert(0, "Texto bloqueado")

# Mostrar ventana
ventana.mainloop()
