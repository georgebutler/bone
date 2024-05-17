from settings import *
from meshes.quad import Quad


class World:
    def __init__(self, app):
        self.app = app
        self.quad = Quad(self.app)

    def update(self):
        pass

    def render(self):
        self.quad.render()


