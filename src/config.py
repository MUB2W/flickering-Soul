import pygame as pg, sys
pg.init()

# Window resolution
WID, HIT = 2000, 1200
WIN = pg.display.set_mode((WID, HIT))
pg.display.set_caption("Untitled Soul")

# Grid
CELL_SIZE = 32
ROWS = HIT // CELL_SIZE # y
COLUMNS = WID // CELL_SIZE # x
print(int(ROWS), int(COLUMNS))

# Color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (150,150,150)

# Clock
CLOCK = pg.time.Clock()
FPS = 60