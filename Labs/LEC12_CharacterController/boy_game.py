from pico2d import *
from auto_run import AutoRun


# Game object class here

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

    def update(self):
        pass


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
        boy.draw_frame()


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

    def draw_frame(self, size=100):
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y, size, size)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y, size, size)


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)


def reset_world():
    global world
    global boy

    world = []

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
