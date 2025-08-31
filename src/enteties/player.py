from src.essentials.config import pg, PINK, WID, HIT
from src.essentials.tools import Spritesheet

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # vel
        self.vel = 5

        # Sprite initialize
        self.player_spritesheet = Spritesheet("assets/player_spritesheet_idle.png", 44, 61, color=PINK)
        self.idle_frames_list = self.player_spritesheet.make_animation(3, 0)

        # animation 
        self.last_update = 0
        self.animation_delay = 250
        self.current_frame = 0
        self.current_animation = self.idle_frames_list

        # Hitbox for controling where img is and collosion
        self.hitbox = pg.Rect(self.x, self.y, 25, 57)

    def movement(self):
        # velocity components used for checking when player is moving or nto
        dx, dy = 0, 0

        key = pg.key.get_pressed()
        if key[pg.K_a] and self.hitbox.x >= 0:
            dx -= 1
            #self.current_animation = None
        if key[pg.K_d] and self.hitbox.x <= WID - self.hitbox.width:
            dx += 1
            #self.current_animation = None
        if key[pg.K_w] and self.hitbox.y >= 0:
            dy -= 1
            #self.current_animation = None
        if key[pg.K_s] and self.hitbox.y <= HIT - self.hitbox.height:
            dy += 1
            #self.current_animation = None
            
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        # Apply velocity
        self.hitbox.x += dx * self.vel
        self.hitbox.y += dy * self.vel

        # No moving / no vel paly idle animation
        if dx == 0 and dy == 0:
            self.current_animation = self.idle_frames_list

    def animaiton_handler(self):
        # loop through list of frames
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.last_update = current_time
        return self.current_frame 

    def draw(self, surf):
        # Get the wat number should the frame be
        self.animaiton_handler()
        
        # USe the index / self.current_frame  to make a surface
        # Get the rect of that surface and center it to hibox for collision and moving
        frame = self.current_animation[self.current_frame]
        rect = frame.get_rect(topright = self.hitbox.topright)

        # Draw that frame from that animation list based on movement / action
        surf.blit(frame, rect)

        # debug draw hitboxes
        pg.draw.rect(surf, 'yellow', rect, 1)
        pg.draw.rect(surf, 'red', self.hitbox, 1) 