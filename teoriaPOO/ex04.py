# Instância VS Classe
class Estudante:
    # Variável de Classe
    id = 1
    
    @classmethod
    def GerarAluno(cls, nome, classe):
        return cls(nome, classe)
    
    @staticmethod
    def nome_curto(nome):
        return True if len(nome) < 5 else False

    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe
        # Variável de Instância
        self.numero = Estudante.id
        Estudante.id += 1
    
    def __str__(self):
        return f"{self.numero}: Estudante {self.nome}, classe {self.classe}"
    
aluno1 = Estudante("Ana", "Primeira")
print(aluno1)
aluno2 = Estudante("João", "Primeira")
print(aluno2)
aluno3 = Estudante("Paula", "Segunda")
print(aluno3)
print(Estudante.GerarAluno("Zé", "Terceira"))
