from gui.main_menu_screen import MainMenu
from gui.login_screen import LoginScreen
import pygame

class ScreenManager:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))
        self._player_name = "none"
        self._current_screen = LoginScreen(self._screen)
        self._running = True
        
    def run(self):
        # Main loop
        while self._running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit button
                    self._running = False
                
                # Login Screen event handling
                if self._current_screen._screen_name == "LoginScreen":
                    # Handle name input
                    name_result = self._current_screen.handle_event(event)
                    if name_result is not None and name_result.strip() != "":
                        self._player_name = name_result
                        self._current_screen = MainMenu(self._screen, self._player_name)
                        continue
                
                # Main menu event handling
                if self._current_screen._screen_name == "MainMenu":
                    # Handle buttons
                    result = self._current_screen.handle_event(event)
                    if result == "host":
                        print("Switch to Host Screen") # TODO: Replace with actual HostScreen
                    if result == "join":
                        print("Switch to Join Screen")
                    if result == "exit":
                        self._running = False
        
            # Display
            self._current_screen.show()
            pygame.display.flip()
        
# Test code
if __name__ == "__main__":
    manager = ScreenManager()
    manager.run()