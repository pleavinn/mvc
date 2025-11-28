from view import View
from controller import Controller
from model import Model

v = View()
c = Controller()
m = Model()

c.set_view(v)
c.set_model(m)

v.set_controller(c)
v.set_command()

m.set_controller(c)

v.run()
