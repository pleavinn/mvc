from elo_01 import Elo_01
from elo_02 import Elo_02
from elo_03 import Elo_03

class Model:
    def __init__(self):
        self.controller = None

        # Criação da corrente de responsabilidades
        # Criação de cada elo
        self.e0 = Elo_01(self)
        self.e1 = Elo_02(self)
        self.e2 = Elo_03(self)

        # Ligação dos elos para formar a corrente
        self.e0.set_next(self.e1)
        self.e1.set_next(self.e2)

    def set_controller(self, controller):
        self.controller = controller

    # Roda a corrente passando o dado para o primeiro elo
    def start(self, data):
        x = self.e0.run(data)
        return x

