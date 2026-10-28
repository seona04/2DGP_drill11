import time


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
        if boy.x >= 710:
            boy.x = 710
            self.direction = -1
        elif boy.x <= 90:
            boy.x = 90
            self.direction = 1
        boy.face_dir = self.direction

    def draw(self, boy):
        boy.draw_frame(size=180)
