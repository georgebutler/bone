from settings import *
from shader import Shader
from world import World
import moderngl as mgl
import pygame as pg
import sys


class FemurEngine:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

        pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        self.shader = None
        self.world = None

        self.is_running = True
        self.on_init()

    def on_init(self):
        self.shader = Shader(self)
        self.world = World(self)

    def update(self):
        self.shader.update()
        self.world.update()
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption(f'{self.clock.get_fps():.0f}')

    def render(self):
        self.ctx.clear()
        self.world.render()
        pg.display.flip()

    def input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

    def run(self):
        while self.is_running:
            self.input()
            self.update()
            self.render()
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    app = FemurEngine()
    app.run()
