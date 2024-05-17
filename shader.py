from settings import *


class Shader:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        # -- shaders -- #
        self.quad = self.get_shader(shader_name='quad')
        # ------------- #
        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        pass

    def update(self):
        pass

    def get_shader(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        return self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
