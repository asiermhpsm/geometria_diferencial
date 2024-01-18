# tests/test_api.py
import unittest
from flask import Flask
from api import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        # Configura el cliente de prueba
        self.app = app.test_client()

    def test_curvatura_Gauss_sin_parametros(self):
        response = self.app.get('/curvatura_Gauss')
        self.assertEqual(response.status_code, 500)  # Cambia esto según tu manejo de errores

    def test_curvatura_Gauss_con_parametros_uv(self):
        response = self.app.get('/curvatura_Gauss?var1=u&var2=v&superficie=u+v')
        self.assertEqual(response.status_code, 200)  # Cambia esto según tu lógica de respuesta

    def test_curvatura_Gauss_con_parametros_xyz(self):
        response = self.app.get('/curvatura_Gauss?var1=x&var2=y&superficie=x+y+z')
        self.assertEqual(response.status_code, 200)  # Cambia esto según tu lógica de respuesta

    # Agrega más pruebas según tus necesidades

if __name__ == "__main__":
    unittest.main()
