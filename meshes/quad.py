import numpy as np
from meshes.mesh import Mesh


class Quad(Mesh):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.shader = app.shader.quad

        self.vbo_format = '2u1 3u1'
        self.attrs = ('in_tex_coord', 'in_position')
        self.vao = self.get_vao()

    def get_vertex_data(self) -> np.array:
        vertices = np.array([
            (0, 0, 0), (1, 0, 1), (1, 0, 0),
            (0, 0, 0), (0, 0, 1), (1, 0, 1)
        ], dtype='uint8')

        tex_coordinates = np.array([
            (0, 0), (1, 1), (1, 0),
            (0, 0), (0, 1), (1, 1)
        ], dtype='uint8')

        vertex_data = np.hstack([tex_coordinates, vertices])
        return vertex_data

