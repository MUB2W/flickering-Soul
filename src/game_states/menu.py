from src.config import WID, HIT, WIN, BLACK, WHITE, CLOCK, FPS, GRAY
import pygame as pg
import sys
from src.tools import Button

# Main function 
def main_menu():
    # Initialize
    play_btn =Button(WID/2, HIT/2, 224, 124, "PLAY", BLACK, 44, WHITE, BLACK, GRAY)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            # Change scene
            if play_btn.is_clicked(event):
                pass
            
        # Bg
        WIN.fill(WHITE)

        # Button
        play_btn.draw(WIN)

        pg.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    main_menu()