import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib import cm

from points import uv_to_xyz

class Figura:
    def __init__(self):
        pass

    def grafica(self):
        pass

class Superficie_Parametrizada(Figura):
    """
    Clase que representa superficie parametrizada, solo se guardan los puntos (x, y, z) ya procesados y las opciones de representacion
    """
    X = None
    Y = None
    Z = None

    color_map = False
    color = None

    def __init__(self, parametrizacion, u, v,limite_inf_u, limite_sup_u, limite_inf_v, limite_sup_v, color_map=False, color=None, resolucion=50):
        """
        Constructor de superficie parametrizada
        No se hacen comprobaciones de tipo

        Argumentos:
        parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
        u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
        v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
        limite_inf_u        limite inferior de la variable u
        limite_sup_u        limite superior de la variable u
        limite_inf_v        limite inferior de la variable v
        limite_sup_v        limite superior de la variable v
        color_map           opcional, booleano para representar con mapa de calor
        color               opcional, color de la superficie
        resolucion          opcional, resolucion con la que se grafica la superficie (50 significa 50x50 puntos)
        """
        self.color_map = color_map
        self.color = color

        # Establezco límites
        u_values = np.linspace(limite_inf_u, limite_sup_u, resolucion)
        v_values = np.linspace(limite_inf_v, limite_sup_v, resolucion)

        self.X = np.array([[float(parametrizacion[0].subs([[u, u_value],[v,v_value]])) for v_value in v_values] for u_value in u_values])
        self.Y = np.array([[float(parametrizacion[1].subs([[u, u_value],[v,v_value]])) for v_value in v_values] for u_value in u_values])
        self.Z = np.array([[float(parametrizacion[2].subs([[u, u_value],[v,v_value]])) for v_value in v_values] for u_value in u_values])

    def grafica(self, fig, ax):
        """
        Graficador de la superficie
        No se hacen comprobaciones de tipo

        Argumentos:
        fig                  resultado de plt.figure()
        ax                   resultado de fig.add_subplot(projection='3d')
        """
        if self.color_map:
            if self.color:
                surf = ax.plot_surface(self.X, self.Y, self.Z, cmap=cm.coolwarm, color=self.color)
                fig.colorbar(surf, shrink=0.5, aspect=5)
            else:
                surf = ax.plot_surface(self.X, self.Y, self.Z, cmap=cm.coolwarm)
                fig.colorbar(surf, shrink=0.5, aspect=5)
        else:
            if self.color:
                surf = ax.plot_surface(self.X, self.Y, self.Z, color=self.color)
            else:
                surf = ax.plot_surface(self.X, self.Y, self.Z)
        
class Superficie_XYZ(Figura):
    """
    Clase que representa superficie representada mediante una ecuacion con x,y,z, solo se guardan los puntos (x, y, z) ya procesados y las opciones de representacion
    """
    X = None
    Y = None
    Z = None

    color_map = False
    color = None
        
    def __init__(self, superficie, x, y, z, limite_inf_x, limite_sup_x, limite_inf_y, limite_sup_y, color_map=False, color=None, resolucion=20):
        """
        Constructor de superficie representada mediante una ecuacion con x,y,z
        No se hacen comprobaciones de tipo

        Argumentos:
        parametrizacion     ecuacion de superficie
        x                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
        y                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
        z                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
        limite_inf_x        limite inferior de la variable x
        limite_sup_x        limite superior de la variable x
        limite_inf_y        limite inferior de la variable y
        limite_sup_y        limite superior de la variable y
        nivel_color         booleano para representar con mapa de calor
        resolucion          resolucion con la que se grafica la superficie (20 significa 20x20 puntos)
        """
        self.color_map = color_map
        self.color = color

        x_values = np.linspace(limite_inf_x, limite_sup_x, resolucion)
        y_values = np.linspace(limite_inf_y, limite_sup_y, resolucion)
        self.X, self.Y = np.meshgrid(x_values, y_values)

        self.Z = np.array([[sp.solve(superficie.subs([[x, x_value],[y,y_value]]), z)[0] for y_value in y_values] for x_value in x_values])

    def grafica(self, fig, ax):
        """
        Graficador de la superficie
        No se hacen comprobaciones de tipo

        Argumentos:
        fig                  resultado de plt.figure()
        ax                   resultado de fig.add_subplot(projection='3d')
        """
        if self.color_map:
            if self.color:
                surf = ax.plot_surface(self.X, self.Y, self.Z, cmap=cm.coolwarm, color=self.color)
                fig.colorbar(surf, shrink=0.5, aspect=5)
            else:
                surf = ax.plot_surface(self.X, self.Y, self.Z, cmap=cm.coolwarm)
                fig.colorbar(surf, shrink=0.5, aspect=5)
        else:
            if self.color:
                surf = ax.plot_surface(self.X, self.Y, self.Z, color=self.color)
            else:
                surf = ax.plot_surface(self.X, self.Y, self.Z)

class Punto_UV(Figura):
    """
    Clase que representa un punto de una superficie parametrizada en el espacio 3d, solo se guardan el punto y las opciones de representacion
    """
    X = None
    Y = None
    Z = None

    marker = 'o'
    color = 'r'
    tam = 50

    def __init__(self, parametrizacion, u, v, u0, v0, color='r', marker='o', tam=50):
        """
        Constructor de un punto en una superficie parametrizada
        No se hacen comprobaciones de tipo

        Argumentos:
        parametrizacion     parametrizacion de superficie (lista de longitud 3 con funciones)
        u                   primera variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
        v                   segunda variable de derivacion ( clase sp.Symbol, resultado de sp.symbols() )
        u0                  valor de la variable u del punto en la superficie parametrizada
        v0                  valor de la variable v del punto en la superficie parametrizada
        marker              opcional, tipo de representacion del punto
        color               opcional, color de la superficie
        tam                 opcional, tamaño del punto
        """
        self.color = color
        self.marker = marker
        self.tam = tam

        self.X, self.Y, self.Z = uv_to_xyz(parametrizacion, u, v, u0, v0)

    def grafica(self, fig, ax):
        """
        Graficador del punto
        No se hacen comprobaciones de tipo

        Argumentos:
        fig                  resultado de plt.figure()
        ax                   resultado de fig.add_subplot(projection='3d')
        """
        ax.scatter(self.X, self.Y, self.Z, c=self.color, marker=self.marker, s=self.tam) 
        
class Punto_XYZ(Figura):
    """
    Clase que representa un punto en el espacio 3d, solo se guardan el punto y las opciones de representacion
    """
    X = None
    Y = None
    Z = None

    marker = 'o'
    color = 'r'
    tam = 50

    def __init__(self, x0, y0, z0, color='r', marker='o', tam=50):
        """
        Constructor de un punto
        No se hacen comprobaciones de tipo

        Argumentos:
        x0                  valor de la variable x
        y0                  valor de la variable y
        z0                  valor de la variable z
        marker              opcional, tipo de representacion del punto
        color               opcional, color de la superficie
        tam                 opcional, tamaño del punto
        """
        self.X = x0
        self.Y = y0
        self.Z = z0
        self.color = color
        self.marker = marker
        self.tam = tam

    def grafica(self, fig, ax):
        """
        Graficador del punto
        No se hacen comprobaciones de tipo

        Argumentos:
        fig                  resultado de plt.figure()
        ax                   resultado de fig.add_subplot(projection='3d')
        """
        ax.scatter(self.X, self.Y, self.Z, c=self.color, marker=self.marker, s=self.tam) 

class Vector(Figura):
    """
    Clase que representa un vector desde un punto y las opciones de representacion
    """
    inicio = None
    vector = None

    color = 'black'

    def __init__(self, x0, y0, z0, vx, vy, vz, color='black'):
        """
        Constructor de un vector desde un punto
        No se hacen comprobaciones de tipo

        Argumentos:
        x0                  valor de la variable x en el punto inicial
        y0                  valor de la variable y en el punto inicial
        z0                  valor de la variable z en el punto inicial
        vx                  componente x del vector
        vy                  componente y del vector
        vz                  componente z del vector
        color               opcional, color de la superficie
        """
        self.inicio = (x0, y0, z0)
        self.vector = (vx, vy, vz)
        self.color = color

    def grafica(self, fig, ax):
        """
        Graficador del vector
        No se hacen comprobaciones de tipo

        Argumentos:
        fig                  resultado de plt.figure()
        ax                   resultado de fig.add_subplot(projection='3d')
        """
        ax.quiver(self.inicio[0],self.inicio[1],self.inicio[2], self.vector[0],self.vector[1],self.vector[2], color=self.color)


def grafica(figuras):
    """
    Representa todas lassuperficies que se pasan como parametros
    No se hacen comprobaciones de tipo

    Argumentos:
    figuras               lista de figuras (clase Figura)
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for figura in figuras:
        if isinstance(figura, Figura):
            figura.grafica(fig, ax)
    ax.set_aspect('equal')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    
