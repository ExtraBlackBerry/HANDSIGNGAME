from gui.main_menu import MainMenu
import pygame

class ScreenManager:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))
        self._player_name = "player"
        self._current_screen = MainMenu(self._screen, self._player_name) # Start with main menu
        self._running = True
        
    def run(self):
        # Main loop
        while self._running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit button
                    self._running = False
                result = self._current_screen.handle_event(event) # Let screen handle event
                if result == "host":
                    print("Switch to Host Screen") # TODO: Replace with actual HostScreen
                if result == "join":
                    print("Switch to Join Screen")
                if result == "exit":
                    self._running = False
        
            # Display update
            self._current_screen.show()
            pygame.display.flip()
        
# Test code
if __name__ == "__main__":
    manager = ScreenManager()
    manager.run()