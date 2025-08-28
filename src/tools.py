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
        pg.draw.rect(surf, self.border_color, self.rect, 2)

        # Hover effect, if mouse touches rect
        mouse = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pg.draw.rect(surf, self.hover_color, self.rect)

        # Draw text
        surf.blit(self.txt, self.txt_r)
