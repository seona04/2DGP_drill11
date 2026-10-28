from pico2d import *
from auto_run import AutoRun


class Idle:
    def handle_event(self, boy, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            boy.change_state(AutoRun())

    def update(self, boy):
        boy.update_animation()

    def draw(self, boy):
        boy.draw_frame()


class Run:
    def __init__(self, direction):
        self.direction = direction

    def update(self, boy):
        boy.update_animation()
        boy.x = min(max(boy.x + self.direction * 5, 50), 750)
        boy.face_dir = self.direction

    def draw(self, boy):
        boy.draw_frame(running=True)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.state = Idle()
        self.pressed_directions = []

    def update(self):
        self.state.update(self)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            if event.key not in self.pressed_directions:
                self.pressed_directions.append(event.key)
            self.change_state(Run(-1 if event.key == SDLK_LEFT else 1))
        elif event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            if event.key in self.pressed_directions:
                self.pressed_directions.remove(event.key)
            if self.pressed_directions:
                direction = -1 if self.pressed_directions[-1] == SDLK_LEFT else 1
                self.change_state(Run(direction))
            else:
                self.change_state(Idle())
        elif isinstance(self.state, Idle):
            self.state.handle_event(self, event)

    def change_state(self, state):
        self.state = state

    def return_to_idle(self):
        self.change_state(Idle())

    def update_animation(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        self.state.draw(self)

    def draw_frame(self, size=100, running=False):
        if running:
            row = 100 if self.face_dir == 1 else 0
        else:
            row = 300 if self.face_dir == 1 else 200
        self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y, size, size)
