import pygame as pg, sys
from src.essentials.tools import FadingRect
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
    # Create a fading rectangle (example: red box, fades by 5 every 50ms)
    fade_rect = FadingRect((0,0, WID, HIT), BLACK, fade_by=3, delay=50)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Background
        WIN.fill(WHITE)

        # Draw fading rectangle
        fade_rect.draw(WIN)

        # Optional: check when fade is done
        if fade_rect.is_done():
            print("Fade finished!")

        pg.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    main_test()