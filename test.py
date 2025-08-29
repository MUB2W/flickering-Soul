import pygame as pg, sys
from src.tools import Spritesheet
pg.init()

# Window resolution
WID, HIT = 2000, 1200
WIN = pg.display.set_mode((WID, HIT))
pg.display.set_caption("Untitled Soul")

# Clock
CLOCK = pg.time.Clock()
FPS = 60

# Color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (150,150,150)


def main_test():
    # Initialize
    player_spritesheet = Spritesheet("assets/player_spritesheet.png", 64, 64)
    frame0 = player_spritesheet.get_img()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Bg
        WIN.fill(BLACK)

        # Sprite 
        WIN.blit(frame0 , (WID/2, HIT/2))

        pg.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    main_test()