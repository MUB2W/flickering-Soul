from .config import pg

class Button:
    def __init__(self, x, y, w, h, text, text_color, text_size, bg_color, border_color, hover_color):
        self.x = x - w // 2 # Center x for positioning 
        self.y = y - w // 2 # Center y for positioning
        self.w = w
        self.h = h
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.bg_color = bg_color
        self.border_color = border_color
        self.hover_color = hover_color

        # Rect
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)

        # Text
        self.font = pg.font.SysFont("arial", self.text_size)
        self.txt = self.font.render(self.text, True, self.text_color)
        self.txt_r = self.txt.get_rect(center = self.rect.center)

    def is_clicked(self, event) -> bool:
        # (True) if right click (False) if right click is not being clicked
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return False
        
    def draw(self, surf):
        # Draw button and border
        pg.draw.rect(surf, self.bg_color, self.rect)

        # Hover effect, if mouse touches rect
        mouse = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pg.draw.rect(surf, self.hover_color, self.rect)
        
        # Draw border
        pg.draw.rect(surf, self.border_color, self.rect, 2)

        # Draw text
        surf.blit(self.txt, self.txt_r)

def draw_grid(surf, cols, rows, cell_size=40):
    # Vertical lines
    for x in range(0, cols * cell_size, cell_size):
        pg.draw.line(surf, 'black', (x, 0), (x, rows * cell_size), 2)

    # Horizontal lines
    for y in range(0, rows * cell_size, cell_size):
        pg.draw.line(surf, 'black', (0, y), (cols * cell_size, y), 2)

def map_reader(surf, rows, columns, map_data, cell_size):
    for y in range(rows):
        for x in range(columns):
            index = map_data[y * columns + x]

            # Now set a number as a tile
            pass

class Spritesheet:
    def __init__(self, spritesheet_path, sprite_w, sprite_h, scale=1, color=None):
        self.sprtiesheet = pg.image.load(spritesheet_path).convert_alpha()
        self.sprite_w = sprite_w
        self.sprite_h = sprite_h
        self.scale = scale
        self.color = color

        # Hold the other animation list in this dic
        self.animation_list = []
        self.last_update = 0
        self.animation_delay = 250
        self.current_frame = 0

    def extract_frame(self, frame_x, frame_y=0):
        # use a surface a cut out for the spirte w, h
        img = pg.Surface((self.sprite_w, self.sprite_h)).convert_alpha()

        # Blit the image ontop of the spritesheet and tell pygame to only get a specific one 
        # use frame_w * sprite_w to get the x one for ex : 1 x 62 = x = 62 same for y
        img.blit(self.sprtiesheet, (0,0), (frame_x * self.sprite_w, frame_y  * self.sprite_h, self.sprite_w, self.sprite_h))

        # Resize by the scale amount if a scale was given
        if self.scale != 1:
            width = int(self.scale * self.sprite_w)
            height = int(self.scale * self.sprite_h)
            img = pg.transform.scale(img,( width, height))

        # remvoe bg color if given
        if self.color is not None:
            img.set_colorkey(self.color)

        # give that img 
        return img
    
    def make_animation(self, num_of_frames, row=0):
        # Make a list that holds the frames inside of it
        frames_list = []

        # give 0,1,2,3, etc based on num_of_frames
        for x in range(num_of_frames):

            # In extract frame it needs the x of the spritesheet and the row x is the 0,1,2,3,4 etc and row is u can give manualy
            frames_list.append(self.extract_frame(x, row))

        # give back the list
        return frames_list

# Used after a level is reached to start the scene
class FadingRect:
    def __init__(self, rect, color, fade_by=5, delay=50):
        self.rect = pg.Rect(rect)
        self.base_color = color
        self.opacity = 255
        self.fade_by = fade_by
        self.delay = delay
        self.last_updated = pg.time.get_ticks()

        # Surface for drawing with alpha
        self.surface = pg.Surface(self.rect.size, pg.SRCALPHA) # RCALPHA supposets / makes alpha possible

    def is_done(self):
        if self.opacity <= 0:
            return True

    def update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_updated >= self.delay:
            self.opacity = max(0, self.opacity - self.fade_by)  # clamp at 0
            self.last_updated = current_time

    def draw(self, surf):
        self.update()
        self.surface.fill((0, 0, 0, 0))  # clear with transparent
        pg.draw.rect(self.surface, (*self.base_color, self.opacity), self.surface.get_rect())
        surf.blit(self.surface, self.rect.topleft)
