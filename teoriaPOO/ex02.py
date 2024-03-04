# Herança

class Animal:
    def __init__(self, n_patas):
        self.n_patas = n_patas
        print("Sou um Animal!")

    pass

class Mamifero(Animal):
    def __init__(self, cor_pelo, **kwargs):
        print("Sou um Mamifero!")
        super().__init__(**kwargs)
    pass

class Cachorro(Mamifero):
    pass

class Gato(Mamifero):
    pass

class Ave(Animal):
    def __init__(self, cor_bico, **kwargs):
        print("Sou uma Ave!")
        super().__init__(**kwargs)
    
class Ornitorrinco(Mamifero, Ave):
    pass

perry = Ornitorrinco(n_patas=4, cor_pelo="verde", cor_bico="amarelo")
