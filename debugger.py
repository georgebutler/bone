from pyrr import Matrix44


class Debugger:
    enabled = True
    draw_wireframe = False
    draw_bbox = False

    engine = None

    def __init__(self, engine):
        self.engine = engine

    def render(self, time: float, frame_time: float):
        translation = Matrix44.from_translation((0, 0, 0), dtype='f4')
        camera_matrix = self.engine.camera.matrix * translation

        if self.draw_bbox:
            self.engine.scene.scene.draw_bbox(
                projection_matrix=self.engine.camera.projection.matrix,
                camera_matrix=camera_matrix,
                children=True,
                color=(0.75, 0.75, 0.75),
            )

        if self.draw_wireframe:
            self.engine.scene.scene.draw_wireframe(
                projection_matrix=self.engine.camera.projection.matrix,
                camera_matrix=camera_matrix,
                color=(1, 1, 1, 1),
            )
