from abc import ABC, abstractmethod

class ClaseBase(ABC):
    @abstractmethod
    def __init__(self, valor1):
        self.valor1 = valor1

class ClaseHija(ClaseBase):
    def __init__(self, valor1, valor2):
        super().__init__(valor1)
        self.valor2 = valor2

# Intentar crear una instancia de ClaseBase generará un TypeError
try:
    instancia_base = ClaseBase(1)
except TypeError as e:
    print(e)  # Imprime el mensaje de error

# Crear una instancia de ClaseHija es posible
instancia_hija = ClaseHija(1,2)
print(instancia_hija.valor1)
print(instancia_hija.valor2)
