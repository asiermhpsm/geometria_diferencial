from flask import Blueprint

representacion_bp = Blueprint('representacion', __name__)

@representacion_bp.route('/representacion')
def representar():
    # Lógica para generar gráficos
    return 'Resultado de generación de gráficos'