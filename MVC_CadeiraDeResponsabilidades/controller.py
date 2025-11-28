class Controller:
    def __init__(self):
        self.model = None
        self.view = None

    def set_view(self, view):
        self.view = view

    def set_model(self, model):
        self.model = model

    def sum(self, event):
        # Recebe os dados da interface
        x, y = self.view.get_val()

        # Envia para o model processar a soma
        # e retornar o resultado
        z = self.model.start([x, y])

        # Atualiza a interface com o resultado
        self.view.set_val(z)
