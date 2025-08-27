from src.config import WID, HIT, WIN, BLACK, WHITE, CLOCK, FPS
import pygame as pg
import sys
from src.tools import Button

# Main function 
def main_menu():
    # Initialize
    play_btn = Button(WID/2 - 112, HIT/2 - 62, 224, 124, "PLAY", 45, WHITE, (0, 150, 255), (0, 122, 204))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            # Add ESC key to exit
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

            # Change scenes if button is clicked
            if play_btn.is_clicked(event):
                print("PLAY button clicked!")


        # Bg
        WIN.fill(BLACK)

        # Button
        play_btn.draw(WIN)

        pg.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    main_menu()