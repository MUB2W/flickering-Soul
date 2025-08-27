from .config import pg

class Button:
    def __init__(self, x, y, width, height, text="", font_size=24, text_color=(255, 255, 255),  color=(0, 122, 204), hover_color=(0, 150, 255), border_radius=12):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font = pg.font.Font(None, font_size)
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color
        self.border_radius = border_radius

    def draw(self, surface):
        # Draw button with hover effect
        # Detect mouse hover
        mouse_pos = pg.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        # Change color on hover
        current_color = self.hover_color if is_hovered else self.color

        # Draw smooth rectangle with rounded edges
        pg.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)

        # Render and center text on button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # Return "True" if button is clicked
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False