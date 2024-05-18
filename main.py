import imgui
import moderngl_window as mglw
from pathlib import Path
from moderngl_window.integrations.imgui import ModernglWindowRenderer
from moderngl_window.scene.camera import KeyboardCamera

from debugger import Debugger
from input import Input
from scene import Scene


class Window(mglw.WindowConfig):
    title = 'FemurEngine'
    window_size = 1280, 720
    resource_dir = (Path(__file__).parent / 'resources').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debugger = Debugger(self)
        self.input = Input(self)
        self.scene = Scene(self, 'gltf/sponza/Sponza.gltf')
        self.camera = KeyboardCamera(self.wnd.keys, fov=90.0, aspect_ratio=self.wnd.aspect_ratio, near=0.1, far=1000.0)

        if self.scene.instance.diagonal_size > 0:
            self.camera.velocity = self.scene.instance.diagonal_size / 5.0

        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)

    def render(self, time: float, frame_time: float):
        self.scene.render(time, frame_time)
        self.debugger.render(time, frame_time)

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
        self.input.key_event(key, action, modifiers)
        keys = self.wnd.keys

        self.camera.key_input(key, action, modifiers)
        self.imgui.key_event(key, action, modifiers)

    def mouse_position_event(self, x, y, dx, dy):
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
    mglw.run_window_config(Window)
