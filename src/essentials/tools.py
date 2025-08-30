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
            return True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
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

        # Hold the other animation list in this list
        self.animation_list = {}
        self.last_update = 0
        self.animation_delay = 250
        self.current_frame = 0
        self.current_animation = None # Used to track wat animation to play from the dic -> self.animation_list

    def extract_frame(self, frame_x, frame_y=0):
        # use a surface a cut out for the spirte w, h
        img = pg.Surface((self.sprite_w, self.sprite_h)).convert_alpha()

        # Blit the image ontop of the spritesheet and tell pygame to only get a specific one 
        # use frame_w * sprite_w to get the x one for ex : 1 x 62 = x = 62 same for y
        img.blit(self.sprtiesheet, (0,0), (frame_x * self.sprite_w, frame_y  * self.sprite_h, self.sprite_w, self.sprite_h))

        # Resize by the scale amount if a scale was given
        if self.scale != 1:
            img = pg.transform.scale(img, (self.sprite_w * self.scale, self.sprite_h * self.scale))

        # remvoe bg color if given
        if self.color is not None:
            img.set_colorkey(self.color)

        # give that img 
        return img
    
    def load_animation(self, name, row, number_of_frames):
        # Take  multiple frames from a row for a animation
        # Hold the frames in this list
        frames = []

        # give the x as a number for ex 0, (1, 2, 3, 4) -> number_of_frames
        for x in range(number_of_frames):
            # Using self.get_img(x, y) sense this is a for loop it dose it for number_of_fremase 
            # Then hold those frames insdie the frames list
            frames.append(self.extract_frame(x, row))
        
        # store it inside animations dict so we can call it later by name
        self.animation_list[name] = frames
        return frames

    def animate(self, name):
        # If another name is given t
        if name != self.current_animation:
            self.current_animation = name
            self.current_frame = 0
            self.last_update = pg.time.get_ticks()

        # Grap the frames for this animation
        frames = self.animation_list[name]
        current_time = pg.time.get_ticks()
        
        # Update the frame if enough time has passed
        if current_time - self.last_update >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.last_update = current_time

        # give back the current frame img
        return frames[self.current_frame]