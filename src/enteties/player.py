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

        # Gravity 
        self.gravity = 10

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
            # find the current_frame / index and keep adding 1 index to animation list and loop if it reaches the end
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.last_update = current_time

        # give it so can use it for animation
        return self.current_frame 

    def apply_gravity(self):
        self.hitbox.y += self.gravity

        if self.hitbox.bottom >= HIT:
            self.hitbox.bottom = HIT

    def collision(self, tile_index, solid_tiles, rows, columns):
        # Loop through each row, columns
        for y in range(rows):
            for x in range(columns):
                
                # Check if player is toucheing the index inside the solid_tiles
                # Ex index 
                if self.hitbox in tile_index:
                    print(f"collision with {tile_index}, at {self.hitbox.x, self.hitbox.y}")

    def draw(self, surf):
        # Get the wat number should the frame be
        self.animaiton_handler()
        
        # Use the index / self.current_frame  to make a surface
        # Get the rect of that surface and center it to hibox for collision and moving
        frame = self.current_animation[self.current_frame]
        rect = frame.get_rect(topright = self.hitbox.topright)

        # Draw that frame from that animation list based on movement / action
        surf.blit(frame, rect)

        # debug draw hitboxes
        pg.draw.rect(surf, 'yellow', rect, 1)
        pg.draw.rect(surf, 'red', self.hitbox, 1) 