from src.essentials.config import pg, BLACK
from src.essentials.tools import Spritesheet
pg.init()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # vel
        self.vel = 5

        # Sprite
        self.player_spritesheet = Spritesheet("assets/player_spritesheet.png", 62, 62, color=BLACK)
        self.idle_frames_list = self.player_spritesheet.make_animation(6, 0)

        # animation 
        self.last_update = 0
        self.animation_delay = 250
        self.current_frame = 0

    def movement(self):
        key = pg.key.get_pressed()
        if key[pg.K_d]:
            pass
        if key[pg.K_d]:
            pass
        if key[pg.K_d]:
            pass
        if key[pg.K_d]:
            pass

    def idle_animation(self, surf):
        # loop through list of frames
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames_list)
            self.last_update = current_time

        surf.blit(self.idle_frames_list[self.current_frame], (self.x, self.y))

    def draw(self, surf):
        pass