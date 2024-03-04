# Classes
class Exemplo:
    def __init__(self, min, max, /, *, nome, familia, cor) -> None:
        self.min = min
        self.max = max
        self.nome = nome
        self.familia = familia
        self.cor = cor
    
    def __str__(self) -> str:
        return f"{self.min}~{self.max}: {self.nome} {self.cor} da familia {self.familia}"

class Bicicleta:
    def __init__(self, cor, modelo, ano, valor):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano
        self.valor = valor
    
    def __str__(self) -> str:
        return f"Bicicleta do modelo {self.modelo}, {self.ano}, da cor {self.cor}, custando R${self.valor}"
    
    def buzinar(self):
        print("Pliiiiiim!")
    
    def correr(self):
        print("Vruuuum!")

class Voltorb:
    def __init__(self, name):
        self.name = name
        print(f"Voltorb {self.name} criado!")
    
    def __del__(self):
        print(f"Voltorb {self.name} explode!")

teste = Exemplo(20,100,cor="red", nome="Yo", familia="Silva")
print(teste)

bike1 = Bicicleta("vermelha", "caloi", 2022, 600)
print(bike1.__dict__)

voltorb1 = Voltorb("Bolino")
del voltorb1
