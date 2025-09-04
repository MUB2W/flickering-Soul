from .config import pg, Image, os

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

class GridDrawer:
    def __init__(self, cols, rows, cell_size=40):
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size

        # Toggle grid visability
        self.grid_draw = False

    def handle_event(self, event):
        # Check for g in the event loop if true or false determins the true or false of self.grid_draw
        if event.type == pg.KEYDOWN and event.key == pg.K_g:
            self.grid_draw = not self.grid_draw

    def draw(self, surf):
        if self.grid_draw:
            # Vertical lines
            for x in range(0, self.cols * self.cell_size, self.cell_size):
                pg.draw.line(surf, 'black', (x, 0), (x, self.rows * self.cell_size), 2)

            # Horizontal lines
            for y in range(0, self.rows * self.cell_size, self.cell_size):
                pg.draw.line(surf, 'black', (0, y), (self.cols * self.cell_size, y), 2)

class MapRenderer:
    def __init__(self, tile_surfaces):
        self.tile_surfaces = tile_surfaces  # list of surfaces, e.g. [None, ground1, red_tile]

    def render(self, surf, rows, columns, map_data, cell_size):
        # Loop through each row, columns
        for y in range(rows):
            for x in range(columns):
                # Convert 2D grid position into a 1D list index
                index = map_data[y * columns + x]

                # Calculate the pixel position on the surface (top-left corner of cell)
                pos = (x * cell_size, y * cell_size)

                # Check if index is valid:
                if index > 0 and index < len(self.tile_surfaces) and self.tile_surfaces[index]:
                    # Draw the tile image onto the surface at the calculated position
                    surf.blit(self.tile_surfaces[index], pos)
    
    def give_index(self, surf, rows, columns, map_data, cell_size):
        # Loop through each row, columns
        for y in range(rows):
            for x in range(columns):
                # Convert 2D grid position into a 1D list index
                index = map_data[y * columns + x]

                # Calculate the pixel position on the surface (top-left corner of cell)
                pos = (x * cell_size, y * cell_size)

        return index

    def get_solid_rects(self, rows, columns, map_data, cell_size, solid_tiles):
        # List to hold rects of solid tiles
        solid_rects = []

        # Loop through each row, columns
        for y in range(rows):
            for x in range(columns):
                # Convert 2D grid position into a 1D list index
                index = map_data[y * columns + x]

                # If this tile is solid
                if index in solid_tiles:
                    # Calculate the pixel position on the surface (top-left corner of cell)
                    pos = (x * cell_size, y * cell_size)

                    # Create rect for this tile
                    tile_rect = pg.Rect(pos[0], pos[1], cell_size, cell_size)

                    # Add to list
                    solid_rects.append(tile_rect)

        return solid_rects

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

class ScenePlayer:
    def __init__(self, scene_path, x, y, w, h):
        # Position and size
        self.scene_path = scene_path
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # Detect file type and load frames
        ext = os.path.splitext(scene_path)[1].lower()
        if ext == '.gif':
            self.frames = self.load_gif(scene_path)
            self.frame_delay = 100  # ms per frame
        elif ext == '.mp4':
            self.frames = self.load_mp4(scene_path)
            self.frame_delay = 1000 / self.fps if self.fps else 100
        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported: .gif, .mp4")

        self.frame_count = len(self.frames)
        self.current_frame = 0
        self.playing = False

        # Timing
        self.last_update = pg.time.get_ticks()

        # Track completion
        self.done = False

    def load_gif(self, path):
        pil_img = Image.open(path)
        frames = []

        try:
            while True:
                frame = pil_img.copy().convert("RGBA")
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()

                pg_img = pg.image.fromstring(data, size, mode)
                pg_img = pg.transform.scale(pg_img, (self.w, self.h))
                frames.append(pg_img)

                pil_img.seek(pil_img.tell() + 1)
        except EOFError:
            pass

        return frames

    def load_mp4(self, path):
        # check if moviepy is available
        if not MOVIEPY_AVAILABLE:
            raise ImportError("moviepy is required for MP4 support. Install with: pip install moviepy")

        # load the video clip
        clip = VideoFileClip(path)

        # set fps
        self.fps = clip.fps

        # list to hold frames
        frames = []

        # loop through each frame
        for frame in clip.iter_frames():
            # frame is numpy array (height, width, 3) or 4
            if frame.shape[2] == 4:
                frame = frame[:, :, :3]  # remove alpha if present

            # transpose to (width, height, 3) for pygame
            frame = np.transpose(frame, (1, 0, 2))

            # create pygame surface
            surf = pg.image.frombuffer(frame.tobytes(), (frame.shape[0], frame.shape[1]), 'RGB')

            # scale to the desired size
            surf = pg.transform.scale(surf, (self.w, self.h))

            # add to frames
            frames.append(surf)

        # close the clip
        clip.close()

        # return the frames
        return frames

    def update(self, loop=True):
        if self.playing and self.frame_count > 1:
            now = pg.time.get_ticks()
            if now - self.last_update > self.frame_delay:
                self.last_update = now

                if loop:
                    self.current_frame = (self.current_frame + 1) % self.frame_count
                else:
                    if self.current_frame < self.frame_count - 1:
                        self.current_frame += 1
                    else:
                        self.done = True
                        self.playing = False

    def draw(self, surface):
        if self.frames:
            surface.blit(self.frames[self.current_frame], (self.x, self.y))

    def play(self):
        self.playing = True
        self.done = False

    def pause(self):
        self.playing = False

    def reset(self):
        self.current_frame = 0
        self.done = False

    def is_done(self):
        return self.done
