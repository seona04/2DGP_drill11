import time


CANVAS_WIDTH = 800
EDGE_OVERSHOOT = 20


class AutoRun:
    def __init__(self):
        self.direction = 1
        self.started_at = time.monotonic()

    def update(self, boy):
        if time.monotonic() - self.started_at >= 5:
            boy.return_to_idle()
            return

        boy.update_animation()
        boy.x += self.direction * 8
        if boy.x >= CANVAS_WIDTH + EDGE_OVERSHOOT:
            boy.x = CANVAS_WIDTH + EDGE_OVERSHOOT
            self.direction = -1
        elif boy.x <= -EDGE_OVERSHOOT:
            boy.x = -EDGE_OVERSHOOT
            self.direction = 1
        boy.face_dir = self.direction

    def draw(self, boy):
        boy.draw_frame(size=180, running=True)
