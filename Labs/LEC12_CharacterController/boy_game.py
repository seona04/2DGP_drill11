from pico2d import *


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


class AutoRun:
    def __init__(self):
        self.direction = 1

    def handle_event(self, boy, event):
        pass

    def update(self, boy):
        boy.update_animation()
        boy.x += self.direction * 5
        if boy.x >= 750:
            boy.x = 750
            self.direction = -1
        elif boy.x <= 50:
            boy.x = 50
            self.direction = 1
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

    def update(self):
        self.state.update(self)

    def handle_event(self, event):
        self.state.handle_event(self, event)

    def change_state(self, state):
        self.state = state

    def update_animation(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        self.state.draw(self)

    def draw_frame(self):
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)


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
