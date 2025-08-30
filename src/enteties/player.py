from src.essentials.config import pg, BLACK
from src.essentials.tools import Spritesheet
pg.init()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Sprite
        self.player_sprite = Spritesheet("assets/player_spritesheet.png", 62, 62, color=BLACK)
        self.frames = self.player_sprite.load_animation("idle", 0, 6)

    def draw(self, surf):
        # Look for the right animation / blit
        frames = self.player_sprite.animate("idle")
        surf.blit(frames, (self.x, self.y))
