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

        # Collision flags
        self.on_ground = False

    def movement(self, solid_rects):
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

        # Calculate new position rects for collision checking
        new_hitbox_x = self.hitbox.move(dx * self.vel, 0)
        new_hitbox_y = self.hitbox.move(0, dy * self.vel)

        # Check horizontal collisions
        for tile_rect in solid_rects:
            if new_hitbox_x.colliderect(tile_rect):
                dx = 0
                break

        # Check vertical collisions
        for tile_rect in solid_rects:
            if new_hitbox_y.colliderect(tile_rect):
                dy = 0
                break

        # Apply velocity after collision checks
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

    def apply_gravity(self, solid_rects):
        # Reset on_ground flag
        self.on_ground = False

        # Calculate new position after gravity
        new_hitbox = self.hitbox.move(0, self.gravity)

        # Check for collision with solid tiles below
        for tile_rect in solid_rects:
            if new_hitbox.colliderect(tile_rect):
                # If colliding, set player on top of the tile
                self.hitbox.bottom = tile_rect.top
                self.on_ground = True
                return  # Don't apply gravity if on ground

        # Apply gravity if no collision
        self.hitbox.y += self.gravity

        # Check screen bottom
        if self.hitbox.bottom >= HIT:
            self.hitbox.bottom = HIT
            self.on_ground = True

    def collision(self, solid_rects):
        # Check for collision with solid tiles
        for tile_rect in solid_rects:
            if self.hitbox.colliderect(tile_rect):
                # Handle collision - for now just print
                print(f"Collision with tile at {tile_rect.x, tile_rect.y}")

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