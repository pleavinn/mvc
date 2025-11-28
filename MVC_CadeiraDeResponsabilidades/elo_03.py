from elo import Elo

class Elo_03(Elo):
    # Realiza a soma dos valores
    def proc(self, data):
        data = data[0] + data[1]

        print(data)

        return data