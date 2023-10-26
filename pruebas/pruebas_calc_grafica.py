import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para dibujar el gráfico
def draw_graph(data):
    plot.clear()  # Limpia cualquier gráfico previo
    plot.plot(data)  # Dibuja el nuevo gráfico

# Función que se ejecuta al presionar el botón
def update_graph():
    # Aquí puedes obtener los datos para el gráfico, por ejemplo, desde una entrada de usuario
    new_data = [1, 4, 9, 16, 25]

    # Llama a la función de dibujo para actualizar el gráfico
    draw_graph(new_data)
    canvas.draw()

# Crear una ventana de tkinter
root = tk.Tk()
root.title("Gráfico interactivo")

# Crear una figura de matplotlib
fig = Figure(figsize=(5, 4), dpi=100)
plot = fig.add_subplot(111)

# Crear una instancia de FigureCanvasTkAgg y pasar la figura
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Crear un botón para actualizar el gráfico
update_button = tk.Button(root, text="Actualizar Gráfico", command=update_graph)
update_button.pack()

# Iniciar el bucle principal de tkinter
root.mainloop()
