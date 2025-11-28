from elo import Elo

class Elo_02(Elo):
    # Converte o segundo valor em inteiro
    def proc(self, data):
        data[1] = int(data[1])

        print(data)

        return data