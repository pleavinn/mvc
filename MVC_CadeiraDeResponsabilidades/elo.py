from abc import ABC, abstractmethod

class Elo:
    def __init__(self, model):
        self.next = None

    def set_next(self, next):
        self.next = next

    # Realiza o processamento do dado
    # Necessário retornar o dado para
    # que quem chamou o primeiro elo
    # consiga obter o resultado do
    # processamento
    #
    # Este metodo será sobrescrito para
    # cada novo elo que herdar desta
    # classe
    #
    # Este metodo é abstrato para forçar
    # a sua implementação nos filhos
    @abstractmethod
    def proc(self, data):
        pass

    # Roda o elo passando o dado para o próximo
    # elo e assim sucessivamente até que todos
    # os elos processem os dados e então retornem
    # o valor final para quem chamou o start
    def run(self, data):
        data = self.proc(data)

        if self.next is not None:
            return self.next.run(data)
        else:
            return data
