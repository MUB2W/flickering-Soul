# essentials init file
# import commonly used essentials modules here

from .config import *
from .tools import *

# load assets
opening_scene = ScenePlayer("assets/scenes/untitled_soul_opening.gif", 0, 0, WID, HIT) # load opening gif
ground1 = pg.transform.scale(pg.image.load("assets/tiles/ground1.png"), (CELL_SIZE, CELL_SIZE)).convert_alpha() # load ground tile
