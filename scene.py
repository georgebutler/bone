import moderngl
from pyrr import Matrix44


class Scene:
    engine = None
    instance = None

    def __init__(self, engine, file):
        self.engine = engine
        self.instance = self.engine.load_scene(file)

    def render(self, time: float, frame_time: float):
        self.engine.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        translation = Matrix44.from_translation((0, 0, 0), dtype='f4')
        camera_matrix = self.engine.camera.matrix * translation

        self.instance.draw(
            projection_matrix=self.engine.camera.projection.matrix,
            camera_matrix=camera_matrix,
            time=time,
        )
