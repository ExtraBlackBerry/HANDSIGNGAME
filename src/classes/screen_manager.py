from gui.host_screen import HostScreen
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
        self._game_ready = False # TODO: Set to true when enough players have joined
        
        # Network function slots
        self._network_host_function = lambda: None
        self._network_join_function = lambda: None
        self._network_close_function = lambda: None
        
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
                    if result == "Host":
                        self._current_screen = HostScreen(self._screen, self._network_host_function, self._network_close_function, self._player_name)
                    if result == "Join":
                        print("Switch to Join Screen")
                    if result == "Exit":
                        self._running = False
                        
                # Host screen event handling
                if self._current_screen._screen_name == "HostScreen":
                    result = self._current_screen.handle_event(event)
                    # Close socket and return to main menu
                    if result == "Close":
                        self._network_close_function()
                        self._current_screen = MainMenu(self._screen, self._player_name)
                    if result == "Start" and self._game_ready:
                        # TODO: Start game
                        # Dont close host socket, just transition to game screen
                        print("Start Game - Not implemented")
                        pass
        
            # Display
            self._current_screen.show()
            pygame.display.flip()
        
# Test code
if __name__ == "__main__":
    from network import NetPeer
    network = NetPeer()
    manager = ScreenManager()
    manager._network_close_function = network.close
    manager._network_host_function = network.host
    manager.run()