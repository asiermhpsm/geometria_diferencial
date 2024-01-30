import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

# Función para dibujar el gráfico 3D
def draw_3d_graph():
    ax.clear()  # Limpia cualquier gráfico previo
    # Aquí puedes agregar la lógica para trazar tus datos en 3D

    # Por ejemplo, para dibujar una superficie de ejemplo:
    import numpy as np
    X = np.linspace(-5, 5, 100)
    Y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(X, Y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    ax.plot_surface(X, Y, Z, cmap='viridis')

    canvas.draw()

# Crear una ventana de tkinter
root = tk.Tk()
root.title("Gráfico 3D interactivo")

# Crear una figura de matplotlib en 3D
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111, projection='3d')

# Crear una instancia de FigureCanvasTkAgg y pasar la figura
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Crear un botón para actualizar el gráfico
update_button = tk.Button(root, text="Actualizar Gráfico", command=draw_3d_graph)
update_button.pack()

# Iniciar el bucle principal de tkinter
root.mainloop()
