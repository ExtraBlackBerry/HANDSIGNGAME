from gui.host_screen import HostScreen
from gui.main_menu_screen import MainMenu
from gui.login_screen import LoginScreen
from gui.join_screen import JoinScreen
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
        self._network_join_function = lambda ip, port=5678: None
        self._network_close_function = lambda: None
        
    def run(self):
        # Main loop
        while self._running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit button
                    self._running = False
                
                # Login Screen event handling
                if isinstance(self._current_screen, LoginScreen):
                    # Handle name input
                    name_result = self._current_screen.handle_event(event)
                    if name_result is not None and name_result.strip() != "":
                        self._player_name = name_result
                        self._current_screen = MainMenu(self._screen, self._player_name)
                        continue
                
                # Main menu event handling
                elif isinstance(self._current_screen, MainMenu):
                    # Handle buttons
                    result = self._current_screen.handle_event(event)
                    if result == "Host":
                        self._current_screen = HostScreen(self._screen, self._network_host_function, self._network_close_function, self._player_name)
                    elif result == "Join":
                        self._current_screen = JoinScreen(self._screen, self._network_join_function, self._player_name)
                    elif result == "Exit":
                        self._running = False
                        
                # Host screen event handling
                elif isinstance(self._current_screen, HostScreen):
                    result = self._current_screen.handle_event(event)
                    # Check if game can be started
                    if self._current_screen._joined_name is not None:
                        self._game_ready = True
                    else:
                        self._game_ready = False
                        
                    if result == "Start" and self._game_ready:
                        # TODO: Start game
                        # Dont close host socket, just transition to game screen
                        print("Start Game - Not implemented")
                        
                    # Close socket and return to main menu
                    elif result == "Close":
                        self._network_close_function()
                        self._current_screen = MainMenu(self._screen, self._player_name)
        
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
    manager._network_join_function = network.join
    manager.run()