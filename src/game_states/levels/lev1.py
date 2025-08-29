from src.config import pg, sys, WID, HIT, COLUMNS, ROWS, WHITE, WIN, CLOCK, FPS, CELL_SIZE
from src.tools import draw_grid
pg.init()

def main_lev1():
    # Initialize

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Bg
        WIN.fill(WHITE)

        # Grid
        draw_grid(WIN, COLUMNS, ROWS, CELL_SIZE)

        pg.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    main_lev1()