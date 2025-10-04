from gui.host_screen import HostScreen
from gui.main_menu_screen import MainMenu
from gui.login_screen import LoginScreen
from gui.join_screen import JoinScreen
from gui.joined_screen import JoinedScreen
from player import Player
import pygame

class ScreenManager:
    def __init__(self):
        pygame.init()
        self._display = pygame.display.set_mode((1280, 720))
        self.player1 = None
        self.player2 = None
        self._current_screen = LoginScreen(self._display)
        self._running = True
        self._game_ready = False
        self._network = None
        
        # Network function slots
        self._network_host_function = lambda: None
        self._network_join_function = lambda ip, port=5432: None
        self._network_close_function = lambda: None
        self._network_send_function = lambda obj: None
        self._network_receive_player2 = lambda: None
        
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
                    name_result = self._current_screen.handle_event(event) # Get name from input box
                    if name_result is not None and name_result.strip() != "":
                        # Update player name and go to main menu
                        self.player1 = Player(name_result)
                        self._current_screen = MainMenu(self._display, self.player1)
                        continue
                
                # Main menu event handling
                elif isinstance(self._current_screen, MainMenu):
                    # Handle buttons
                    result = self._current_screen.handle_event(event)
                    if result == "Host":
                        self._current_screen = HostScreen(self._display, self._network_host_function, self._network_close_function, self.player1)
                    elif result == "Join":
                        self._current_screen = JoinScreen(self._display, self._network_join_function, self.player1)
                    elif result == "Exit":
                        self._running = False
                        
                # Host screen event handling
                elif isinstance(self._current_screen, HostScreen):
                    joined_player = network.player_join_event
                    if joined_player is not None and self.player1 is not None and self.player2 is None:
                        print(f"Player 2 joined: {joined_player}")
                        self.player2 = Player(joined_player)
                        self._current_screen._joined_player = self.player2
                        self._current_screen._joined_box_text_surface = self._current_screen._font.render(self.player2.name, True, 'black')
                        self._network_send_function({"type": "host_name", "content": self.player1.name})
                        
                        print("Sent host name to player 2")

                    # Check if game can be started
                    if self._current_screen._joined_player is not None:
                        self._game_ready = True
                    else:
                        self._game_ready = False
                    
                    # Handle buttons
                    result = self._current_screen.handle_event(event)
                    if result == "Start" and self._game_ready:
                        # TODO: Start game
                        # Dont close host socket, just transition to game screen
                        print("Start Game - Not implemented")
                    # Close socket and return to main menu
                    elif result == "Close":
                        self._network_close_function()
                        self._current_screen = MainMenu(self._display, self.player1)
                        # TODO: Tell joined player to close if host leaves
                        # if joined_player is not None:
                        #    self._network_send_function({"type": "player_left", "content": "Host has quit."})
        
                # Join screen event handling
                elif isinstance(self._current_screen, JoinScreen):
                    # Handle buttons
                    result = self._current_screen.handle_event(event) # Also handles input box updates
                    if result == "Close":
                        # Close socket and return to main menu
                        self._network_close_function()
                        self._current_screen = MainMenu(self._display, self.player1)
                    elif result == "Joined":
                        # If join was successful, go to waiting screen
                        self._current_screen = JoinedScreen(self._display, self.player1)
                        if self.player1 is None: return # Make sure name exists
                        self._network_send_function({"type": "join", "content": self.player1.name})
                    elif result == "JoinFailed":
                        # TODO: Add error message display instead of just print
                        self._network_close_function()
                        self._current_screen = MainMenu(self._display, self.player1)
                        print("Join failed")
                        
                # Joined Screen Event Handling
                elif isinstance(self._current_screen, JoinedScreen):
                # Create object to track host player and update display name
                    host_player = network.player_join_event
                    if host_player is not None and self.player1 is not None and self.player2 is None:
                        self.player2 = Player(host_player)
                        self._current_screen.host_player = self.player2
                        self._current_screen._host_box_text_surface = self._current_screen._font.render(self.player2.name, True, 'black')
            # Display
            self._current_screen.show()
            pygame.display.flip()
        
# Test code
if __name__ == "__main__":
    from network import NetPeer
    network = NetPeer()
    manager = ScreenManager()
    manager._network = network
    manager._network_close_function = network.close
    manager._network_host_function = network.host
    manager._network_join_function = network.join
    manager._network_send_function = network.send
    manager._network_receive_player2 = network.get_player_join_event
    manager.run()