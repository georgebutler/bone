import imgui
import moderngl
import moderngl_window as mglw
from pathlib import Path
from moderngl_window.integrations.imgui import ModernglWindowRenderer
from pyrr import Matrix44
from moderngl_window.scene.camera import KeyboardCamera


class FemurEngine(mglw.WindowConfig):
    title = 'FemurEngine'
    window_size = 1280, 720
    aspect_ratio = None
    resource_dir = (Path(__file__).parent / 'resources').resolve()

    debug_wireframe = False
    debug_bbox = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        imgui.create_context()

        self.camera_enabled = True
        self.imgui = ModernglWindowRenderer(self.wnd)

        self.wnd.mouse_exclusivity = True
        self.wnd.cursor = not self.camera_enabled

        self.scene = self.load_scene('gltf/sponza/Sponza.gltf')
        self.camera = KeyboardCamera(self.wnd.keys, fov=90.0, aspect_ratio=self.wnd.aspect_ratio, near=0.1, far=1000.0)

        if self.scene.diagonal_size > 0:
            self.camera.velocity = self.scene.diagonal_size / 5.0

    def render(self, time: float, frame_time: float):
        """Render the scene"""
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        translation = Matrix44.from_translation((0, 0, 0), dtype='f4')
        camera_matrix = self.camera.matrix * translation

        self.scene.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=camera_matrix,
            time=time,
        )

        if self.debug_bbox:
            self.scene.draw_bbox(
               projection_matrix=self.camera.projection.matrix,
               camera_matrix=camera_matrix,
               children=True,
               color=(0.75, 0.75, 0.75),
            )

        if self.debug_wireframe:
            self.scene.draw_wireframe(
                projection_matrix=self.camera.projection.matrix,
                camera_matrix=camera_matrix,
                color=(1, 1, 1, 1),
            )

        # Render UI
        imgui.new_frame()
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                clicked_quit, selected_quit = imgui.menu_item("Quit", 'Cmd+Q', False, True)

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        # imgui.show_test_window()

        # imgui.begin("Custom window", True)
        # imgui.text("Bar")
        # imgui.text_colored("Eggs", 0.2, 1., 0.)
        # imgui.end()

        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)
        self.imgui.resize(width, height)

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if self.camera_enabled:
            self.camera.key_input(key, action, modifiers)

        if action == keys.ACTION_PRESS:
            if key == keys.F1:
                self.camera_enabled = not self.camera_enabled
                self.wnd.mouse_exclusivity = self.camera_enabled
                self.wnd.cursor = not self.camera_enabled
                self.timer.toggle_pause()
            if key == keys.F2:
                self.debug_wireframe = not self.debug_wireframe
            if key == keys.F3:
                self.debug_bbox = not self.debug_bbox

        self.imgui.key_event(key, action, modifiers)

    def mouse_position_event(self, x, y, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(-dx, -dy)

        self.imgui.mouse_position_event(x, y, dx, dy)

    def mouse_drag_event(self, x, y, dx, dy):
        super().mouse_drag_event(x, y, dx, dy)
        self.imgui.mouse_drag_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset, y_offset):
        super().mouse_scroll_event(x_offset, y_offset)
        self.imgui.mouse_scroll_event(x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        super().mouse_press_event(x, y, button)
        self.imgui.mouse_press_event(x, y, button)

    def mouse_release_event(self, x: int, y: int, button: int):
        super().mouse_release_event(x, y, button)
        self.imgui.mouse_release_event(x, y, button)

    def unicode_char_entered(self, char):
        super().unicode_char_entered(char)
        self.imgui.unicode_char_entered(char)


if __name__ == '__main__':
    mglw.run_window_config(FemurEngine)
