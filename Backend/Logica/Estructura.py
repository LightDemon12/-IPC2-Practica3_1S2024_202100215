class Animal:
    def __init__(self, tipo, edad, raza):
        self.tipo = tipo
        self.edad = edad
        self.raza = raza

    def __str__(self):
        return f'Tipo: {self.tipo}, Edad: {self.edad}, Raza: {self.raza}'