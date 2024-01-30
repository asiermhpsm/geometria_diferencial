"""from io import BytesIO
import sympy as sp
from sympy.plotting import plot3d_parametric_surface
import matplotlib.pyplot as plt


u, v = sp.symbols('u v')
surface = (sp.cos(u + v), sp.sin(u - v), u - v)
plot = plot3d_parametric_surface(*surface, show=False)
"""

import base64
from io import BytesIO
from flask import Flask
from matplotlib.figure import Figure
import sympy as sp
from sympy.plotting import plot3d_parametric_surface
import matplotlib.pyplot as plt

u, v = sp.symbols('u v')


expr = (sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v) , sp.sin(u))
plot3d_parametric_surface(*expr)


app = Flask(__name__)


@app.route("/")
def hello():
    u, v = sp.symbols('u v')
    surface = (sp.cos(u + v), sp.sin(u - v), u - v)
    plot = plot3d_parametric_surface(*surface, show=False)
    fig = plot._backend.fig
    ax = fig.gca()
    ax.set_box_aspect([1, 1, 1])
    
    buf = BytesIO()
    plot.save(buf)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

"""if __name__ == '__main__':
    app.run(debug=True)"""