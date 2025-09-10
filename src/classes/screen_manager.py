from gui.main_menu import MainMenu
import pygame

class ScreenManager:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))
        self._current_screen = MainMenu(self._screen) # Start with main menu
        self._running = True
        
    def run(self):
        # Main loop
        while self._running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit button
                    self._running = False
                self._current_screen.handle_event(event) # Let screen handle event
        
        # Display update
        self._current_screen.show()
        pygame.display.flip()
        
# Test code
if __name__ == "__main__":
    manager = ScreenManager()
    manager.run()