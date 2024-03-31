import tkinter as tk
from tkinter import ttk

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def add_entry():
    entry = ttk.Entry(interior_frame)
    entry.grid(row=len(entries), column=0, padx=10, pady=5, sticky="ew")
    entries.append(entry)
    interior_frame.update_idletasks()  # Actualiza el frame interior para que el canvas ajuste la barra de desplazamiento

root = tk.Tk()
root.geometry("400x300")

main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

interior_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=interior_frame, anchor="nw")

add_button = ttk.Button(root, text="Agregar Entry", command=add_entry)
add_button.pack(pady=10)

entries = []  # Lista para almacenar las entries creadas dinámicamente

interior_frame.bind("<Configure>", on_configure)

root.mainloop()
