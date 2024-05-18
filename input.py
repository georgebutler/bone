class Input:
    engine = None

    def __init__(self, engine):
        self.engine = engine
        self.engine.wnd.mouse_exclusivity = True
        self.engine.wnd.cursor = False

    def key_event(self, key, action, modifiers):
        keys = self.engine.wnd.keys

        if action == keys.ACTION_PRESS:
            if key == keys.F1:
                self.engine.wnd.mouse_exclusivity = not self.engine.wnd.mouse_exclusivity
                self.engine.wnd.cursor = not self.engine.wnd.cursor
                self.engine.timer.toggle_pause()
            if key == keys.F2:
                self.engine.debugger.draw_wireframe = not self.engine.debugger.draw_wireframe
            if key == keys.F3:
                self.engine.debugger.draw_bbox = not self.engine.debugger.draw_bbox
