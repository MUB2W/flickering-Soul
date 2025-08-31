from src.essentials.config import pg, PINK
from src.essentials.tools import Spritesheet

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # vel
        self.vel = 5

        # Sprite initialize
        self.player_spritesheet = Spritesheet("assets/player_spritesheet.png", 44, 61, 5, color=PINK)
        self.idle_frames_list = self.player_spritesheet.make_animation(3, 0)

        # animation 
        self.last_update = 0
        self.animation_delay = 250
        self.current_frame = 0
        self.current_animation = self.idle_frames_list

        # Hitbox for controling where img is and collosion
        self.hitbox = pg.Rect(self.x, self.y, 24, 20)

    def movement(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.hitbox.x -= self.vel
        if key[pg.K_d]:
            self.hitbox.x += self.vel
        if key[pg.K_w]:
            self.hitbox.y -= self.vel
        if key[pg.K_s]:
            self.hitbox.y += self.vel
        else:
            self.current_animation = self.idle_frames_list
            self.animaiton_handler()
            
    def animaiton_handler(self):
        # loop through list of frames
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.last_update = current_time
        
        return self.current_frame

    def draw(self, surf):

        rect = self.idle_frames_list[self.current_frame].get_rect(center = (self.hitbox.center))
        surf.blit(self.idle_frames_list[self.current_frame], (rect.x, rect.y))
        pg.draw.rect(surf, 'red', self.hitbox, 1)