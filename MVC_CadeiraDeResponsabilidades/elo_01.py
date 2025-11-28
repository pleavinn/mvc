from elo import Elo

class Elo_01(Elo):
    # Converte o primeiro valor em inteiro
    def proc(self, data):
        data[0] = int(data[0])

        print(data)

        return data