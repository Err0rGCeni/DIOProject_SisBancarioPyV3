#Abstracts
from abc import ABC, abstractmethod

class Controle(ABC):
    @abstractmethod
    def ligar(self):
        pass

    @abstractmethod
    def desligar(self):
        pass

    @property
    @abstractmethod
    def marca(self):
        pass

class ControleTV(Controle):
    def ligar(self):
        self.ligado = True
        print("!")
    
    def desligar(self):
        self.ligado = False
        print("!")
    
    @property
    def marca(self):
        return "LG"

class ControleAr(Controle):
    def ligar(self):
        self.ligado = True
        print("Pliiim!")
    
    def desligar(self):
        self.ligado = False
        print("Plum!")

    @property
    def marca(self):
        return "SONY"

'''class ControleTemporal(Controle):
    pass
'''
controleA = ControleTV()
controleB = ControleAr()
#controleC = ControleTemporal()
controleA.ligar()
controleB.desligar()
print(controleB.marca)
