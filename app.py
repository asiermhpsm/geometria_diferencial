from flask import Flask

from blueprints.curvaturas import curvaturas_bp
from blueprints.formas_fundamentales import formas_fundamentales_bp
from blueprints.representacion import representacion_bp
from blueprints.caracteristicas import caracteristicas_bp


app = Flask(__name__)

# Registrar blueprints
app.register_blueprint(curvaturas_bp)
app.register_blueprint(formas_fundamentales_bp)
app.register_blueprint(representacion_bp)
app.register_blueprint(caracteristicas_bp)

if __name__ == '__main__':
    app.run(debug=True)